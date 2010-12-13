from ply.lex import TOKEN as token, lex
from .exceptions import HispError
from . import nodes
import re


class Tokenizer:
    # Tokens ###########################################################{{{1
    token_names = {
        'DJANGO_COMMENT':   'django comment',       # Comment, Contained
        'HTML_COMMENT':     'html comment',         # Comment, Contained
        'DOCTYPE':          'doctype',              # Statement, Contained
        'ATTR':             'attribute',            # Subexpression, Head
        'CLOSER':           'self-closing element', # Statement, Head
        'MACRO':            'macro',                # Statement, Head
        'ELEM':             'tag',                  # Statement, Head
        'OPEN_BLOCK':       'block',                # Statement, Head
        'CLOSED_BLOCK':     'block',                # Statement, Contained
        'CB':               "'}'",                  # Literal
        'CP':               "')'",                  # Literal
        'VARIABLE':         'django variable',      # Constant, Contained
        'CLASS':            'class attribute',      # Subexpression, Contained
        'ID':               'id attribute',         # Subexpression, Contained
        'STRING':           'string',               # Constant, Contained
        'LITERAL':          'literal',              # Constant, Contained
        'CDATA':            'CDATA',                # Constant, Contained
        'WORD':             'text',                 # Subexpression, Contained
    }
    tokens = tuple(token_names)

    # Lex Constants #####################################################}}}{{{1
    # Ignored Characters, Line Counting, and Error Handling

    @token(r'\n+')
    def t_newline(self, t):
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        raise SyntaxError(t)

    t_ignore = ' \t'

    FLAGS = 0

    # Comments ##########################################################}}}{{{1
    # Hisp, Django, and HTML style

    # HISP COMMENT: Contained Comment
    # Hisp comments are pre-processed out
    @token(r"""
    \{!              (?# Bracket Bang)
    ([^}\\]|\\.)*    (?# Anything but unescaped brackets or slashes)
    \}               (?# Closing Bracket)""")
    def t_ignore_COMMENT(self, t):
        pass


    # DJANGO COMMENT: Contained Comment
    # Django comments will be converted to {# django comments #}
    @token(r"""
    \{\#             (?# Bracket Hash)
    ([^}\\]|\\.)*    (?# Anything but unescaped brackets or slashes)
    \}               (?# Closing Bracket)""")
    def t_DJANGO_COMMENT(self, t):
        t.value = nodes.DjangoComment(t.value[2:-1])
        return t


    # HTML COMMENT: Contained Comment
    # These will be converted to <!-- HTML Comments -->
    @token(r"""
    \(!              (?# Paren Bang)
    ([^)\\]|\\.)*    (?# Anything but unescaped parens or slashes)
    \)               (?# Closing Paren)""")
    def t_HTML_COMMENT(self, t):
        t.value = nodes.HtmlComment(t.value[2:-1])
        return t

   # Statements ########################################################}}}{{{1
    # Doctypes, Closing Elements, Blocks, and Macros
    # Note that Element is a statement but is ambigous, so is found below

    # DOCTYPE: Contained Statement
    @token(r"""
    \(~             (?# Paren Tilda)
    ([^)\\]|\\.)    (?# Anything but unescaped parens or slashes)
    \)              (?# Closing Paren)""")
    def t_DOCTYPE(self, t):
        t.value = nodes.Doctype(t.value[2:-1])
        return t


    # CLOSING ELEMENT: Statement Head
    @token(r'\(/\s*[\w-]*')
    @token(r"""     (?# Nameless elements are allowed, as in #id.class)
    \(/\s*          (?# Open Paren frontslash, whitespace)
    [\w-]*          (?# Maybe a tag name, hyphens allowed)""")
    def t_CLOSER(self, t):
        t.value = nodes.Elem(t.value[2:], t.lexer.lineno)
        return t


    _block = r"""
    \{\s*%              (?# Bracket Percent)
    (
      [^~"}\\]|         (?# Normal characters)
      \\.|              (?# Escaped characters)
      "([^"\\]|\\.)*"   (?# Full strings)
    )*"""
    # DJANGO BLOCK, OPEN: Statement Head
    # We enforce that strings be closed before block ending.
    # Escape string characters if you want unbalanced strings.
    @token(_block + r'~')
    def t_OPEN_BLOCK(self, t):
        t.value = nodes.Block(t.value[2:-1], t.lexer.lineno)
        return t


    # DJANGO BLOCK, CLOSED: Contained Statement
    # We enforce that strings be closed before block ending.
    # Escape string characters if you want unbalanced strings.
    @token(_block + r'\}')
    def t_CLOSED_BLOCK(self, t):
        t.value = nodes.Block(t.value[2:-1], t.lexer.lineno)
        return t


    # MACRO: Statement Head
    # A macro name can consist of any non-whitespace characters except one of:
    # {}()[].#
    _macro = r"""
    \(%\s*                  (?# Paren, Percent, Whitespace)
      ([^\s{}()\[\].#]+)    (?# Match 1: Macro Name)
      (?:\[(                (?# Match 2: Argument)
        (?:[^\]\\]|\\.)*    (?# The arg can contain all but unescaped ]s or \s)
      )\])?                 (?# The argument is optional)"""
    _macro_regex = re.compile(_macro, re.VERBOSE | FLAGS)
    @token(_macro)
    def t_MACRO(self, t):
        name, arg = self._macro_regex.match(t.value).groups()
        t.value = nodes.Macro(name, arg, t.lexer.lineno)
        return t

    # Constants #########################################################}}}{{{1
    # Literal Strings, Strings, Variables, and CDATA

    # LITERAL STRING: Contained Constant
    # Literal strings will be passed untouched to output
    @token(r"""
    '               (?# Opening Single Quote)
    ([^'\\]|\\.)*   (?# Anything except unescaped \ or ')
    '               (?# Closing Single Quote)""")
    def t_LITERAL(self, t):
        t.value = nodes.Literal(t.value[1:-1])
        return t


    # STRING: Contained Constant
    # Strings will convert django variables from {hisp} form to
    # {{django}} form for output
    @token(r"""
    "               (?# Opening Quote)
    ([^"\\]|\\.)*   (?# Anything except unescaped \ or ")
    "               (?# Closing Quote)""")
    def t_STRING(self, t):
        t.value = nodes.String(t.value[1:-1])
        return t


    # VARIABLE: Contained Constant
    # No evaluation is done on the contents of {django variables},
    # except that escaped characters (\\ and \}) will be unescaped.
    @token(r"""
    \{(?!\s*%)      (?# Open Bracket without following percent)
    ([^}\\]|\\.)*   (?# Anything except unescaped \ or })
    \}              (?# Close Bracket)""")
    def t_VARIABLE(self, t):
        t.value = nodes.Variable(t.value[1:-1])
        return t


    # CDATA: Contained Constant
    @token(r"""
    <               (?# Opening Angle Bracket)
    ([^>\\]|\\.)*   (?# Anything except unescaped \ or >)
    >               (?# Closing angle bracket)""")
    def t_CDATA(self, t):
        t.value = nodes.CData(t.value[1:-1])
        return t

    # SubExpressions ####################################################}}}{{{1
    # Attributes, Classes, IDs, Words
    # Note that Words are subexpressions but are ambiguous,
    # and can thus be found below.

    # ATTRIBUTE: Subexpression Head
    # Allowed in elements and macros
    @token(r"""
    \(:              (?# Paren Colin)
    \s*[\w:-]+       (?# A word, including hyphens and colins)""")
    def t_ATTR(self, t):
        t.value = t.value[2:]
        return t


    # CLASS ATTRIBUTE: Contained Subexpression
    # Only allowed when not preceeded by whitespace.
    # Will be out-matched by 'WORD' in almost all situations,
    # except when preceded by a statement head
    @token(r"""
    (?<!\s)         (?# Not preceeded by whitespace)
    \.              (?# A dot)
    [\w:-]+         (?# A word, hyphens and colins allowed)""")
    @token(r'(?<!\s)\.([\w-]+)')
    def t_CLASS(self, t):
        t.value = ('class', t.value[1:])
        return t


    # ID ATTRIBUTE: Contained Subexpression
    # Only allowed when not preceeded by whitespace.
    # Will be out-matched by 'WORD' in almost all situations,
    # except when preceded by a statement head
    @token(r"""
    (?<!\s)         (?# Not preceeded by whitespace)
    \#              (?# A hash)
    [\w:-]+         (?# A word, hyphens and colins allowed)""")
    def t_ID(self, t):
        t.value = ('id', t.value[1:])
        return t

    # Literals ##########################################################}}}{{{1
    # Closing Parenthesis ')' or Brackets '}'

    @token(r'\)')
    def t_CP(self, t):
        return t

    @token(r'\}')
    def t_CB(self, t):
        return t

    # Ambiguous Tokens ##################################################}}}{{{1
    # Tokens that out-match other tokens if given the chance

    # ELEMENT: Statement Head
    # Could be made unambigous by adding a lookahead, but there's no need
    # to incur that speed penalty.
    # For the record, the lookahead necessary is below, and would go between
    # the whitespace matching and the name matching
    # (?![:%/!])      (?# Don't match attributes, macros, closers, or comments)
    @token(r"""     (?# Nameless elements are allowed, as in #id.class)
    \(\s*           (?# Open Paren, whitespace)
    [\w:-]*         (?# Maybe a tag name, hyphens and colins allowed)""")
    def t_ELEM(self, t):
        t.value = nodes.Elem(t.value[1:], t.lexer.lineno)
        return t


    # WORD: Unbroken text
    # Words match any unbroken text except literals or constants
    # Words have no concept of 'escaping' but 
    # word"<>"word will be parsed as WORD, STRING, WORD which will
    # be rendered as word<>word, so you can use strings like a
    # poor man's escape characters
    @token(r"""[^\s"'<>)}]+""")
    def t_WORD(self, t):
        return t

    # Tokenizer Methods #################################################}}}{{{1

    def __init__(self, debug=False):
        self.debug = debug

    def lexer(self, **kwargs):
        if 'lextab' not in kwargs:
            try:
                from .tables import lextab
            except ImportError as e:
                raise HispError('Lexer tables not found. Try regenerating them.')
            kwargs['lextab'] = lextab
        kwargs.setdefault('optimize', not self.debug)
        kwargs.setdefault('reflags', self.FLAGS)
        return lex(module=self, **kwargs)

    def generate_tables(self):
        self.lexer(outputdir='tables', lextab='lextab', optimize=True)
