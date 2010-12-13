from ply.lex import TOKEN as token, lex
import nodes
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
        'BLOCK':            'block',                # Statement, Head
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

    # Lex Constants ####################################################{{{1
    # Ignored Characters, Line Counting, and Error Handling

    @token(r'\n+')
    def t_newline(self, t):
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        raise SyntaxError(t)

    t_ignore = ' \t'

    # Comments #########################################################{{{1
    # Hisp, Django, and HTML style

    # HISP COMMENT: Contained Comment
    # Hisp comments are pre-processed out
    @token(r"""
    \{!              # Braket Bang
    ([^}\\]|\\.)*    # Anything but unescaped brackets or slashes
    \}               # Closing Bracket""")
    def t_ignore_COMMENT(self, t):
        pass


    # DJANGO COMMENT: Contained Comment
    # Django comments will be converted to {# django comments #}
    @token(r"""
    \{\#             # Bracket Hash
    ([^}\\]|\\.)*    # Anything but unescaped brackets or slashes
    \}               # Closing Bracket""")
    def t_DJANGO_COMMENT(self, t):
        t.value = nodes.DjangoComment(t.value[2:-1])
        return t


    # HTML COMMENT: Contained Comment
    # These will be converted to <!-- HTML Comments -->
    @token(r"""
    \(!              # Paren Bang
    ([^)\\]|\\.)*    # Anything but unescaped parens or slashes
    \)               # Closing Paren""")
    def t_HTML_COMMENT(self, t):
        t.value = nodes.HtmlComment(t.value[2:-1])
        return t

    # Statements ########################################################}}}{{{1
    # Doctypes, Elements, Closing Elements, Blocks, and Macros

    # DOCTYPE: Contained Statement
    @token(r"""
    \(~             # Paren Tilda
    ([^)\\]|\\.)    # Anything but unescaped parens or slashes
    \)              # Closing Paren""")
    def t_DOCTYPE(self, t):
        t.value = nodes.Doctype(t.value[2:-1])
        return t


    # ELEMENT: Statement Head
    @token(r"""     # Nameless elements are allowed, as in (#id.class)
    \(\s*           # Open Paren, whitespace
    [\w-]*          # Maybe a tag name, hyphens allowed""")
    def t_ELEM(self, t):
        t.value = nodes.Elem(t.value[1:], t.lexer.lineno)
        return t


    # CLOSING ELEMENT: Statement Head
    @token(r'\(/\s*[\w-]*')
    @token(r"""     # Nameless elements are allowed, as in (#id.class)
    \(/\s*          # Open Paren frontslash, whitespace
    [\w-]*          # Maybe a tag name, hyphens allowed""")
    def t_CLOSER(self, t):
        t.value = nodes.Elem(t.value[2:], t.lexer.lineno)
        return t


    # DJANGO BLOCK: Statement Head
    # We do not enforce that string literals be closed within the block
    @token(r"""
    \{%             # Bracket Percent
    ([^~}\\]|\\.)+  # Anything except unescaped ~}\ characters
    [~}]            # Either a ~ or a }""")
    def t_BLOCK(self, t):
        closed = t.value.endswith('}')
        t.value = nodes.Block(t.value[2:-1], closed, t.lexer.lineno)
        return t


    # MACRO: Statement Head
    # A macro name can consist of any non-whitespace characters except one of:
    # {}()[].#~
    _macro = r"""
    \(%\s*                  # Paren, Percent, Whitespace
      ([^\s{}()\[\].#~]+)   # Match 1: Macro Name
      (\[                   # Match 2: Macro Arg
        (?:                 # Unbound Group
          [^\]\\]|\\.)+     # Anything except unescaped ] or \
       \])?                 # Arg is optional"""
    _macro_regex = re.compile(_macro, re.VERBOSE | re.DOTALL)
    @token(_macro)
    def t_MACRO(self, t):
        name, arg = self._macro_regex.match(t.value).groups()
        t.value = nodes.Macro(name[2:], arg, t.lexer.lineno)
        return t

    # Constants #########################################################}}}{{{1
    # String Literals, Strings, Variables, and CDATA

    # STRING LITERAL: Contained Constant
    # String literals will be passed untouched to output
    @token(r"""
    '               # Opening Single Quote
    ([^'\\]|\\.)*   # Anything except unescaped ' or \
    '               # Closing Single Quote""")
    def t_LITERAL(self, t):
        t.value = nodes.Literal(t.value[1:-1])
        return t


    # STRING: Contained Constant
    # Strings will convert django variables from {hisp} form to
    # {{django}} form for output
    @token(r"""
    "               # Opening Quote
    ([^"\\]|\\.)*   # Anything except unescaped " or \
    "               # Closing Quote""")
    def t_STRING(self, t):
        t.value = nodes.String(t.value[1:-1])
        return t


    # VARIABLE: Contained Constant
    # No evaluation is done on the contents of {django variables}
    @token(r"""
    \{              # Open Bracket
    ([^}\\]|\\.)*   # Anything except unescaped } or \
    \}              # Close Bracket""")
    def t_VARIABLE(self, t):
        t.value = nodes.Variable(t.value[1:-1])
        return t


    # CDATA: Contained Constant
    @token(r"""
    <               # Opening Angle Bracket
    ([^>\\]|\\.)*   # Anything except unescaped > or \
    >               # Closing angle bracket""")
    def t_CDATA(self, t):
        t.value = nodes.CData(t.value[1:-1])
        return t

    # SubExpressions ####################################################}}}{{{1
    # Attributes, Classes, IDs, Words

    # ATTRIBUTE: Subexpression Head
    # Allowed in elements and macros
    @token(r"""
    \(:              # Paren Colin
    \s*[\w-:]+       # A word, including hyphens and colins""")
    def t_ATTR(self, t):
        t.value = nodes.Attribute(t.value[2:])
        return t


    # CLASS ATTRIBUTE: Contained Subexpression
    # Only allowed when not preceeded by whitespace.
    # Will be out-matched by 'WORD' in almost all situations,
    # except when preceded by a statement head
    @token(r"""
    (?<!\s)         # Not preceeded by whitespace
    \.              # A dot
    [\w-:]+         # A word, hyphens and colins allowed""")
    @token(r'(?<!\s)\.([\w-]+)')
    def t_CLASS(self, t):
        attr = nodes.Attribute('class')
        attr.set_value(t.value[1:])
        t.value = attr
        return t


    # ID ATTRIBUTE: Contained Subexpression
    # Only allowed when not preceeded by whitespace.
    # Will be out-matched by 'WORD' in almost all situations,
    # except when preceded by a statement head
    @token(r"""
    (?<!\s)         # Not preceeded by whitespace
    \#              # A hash
    [\w-:]+         # A word, hyphens and colins allowed""")
    def t_ID(self, t):
        attr = nodes.Attribute('id')
        attr.set_value(t.value[1:])
        t.value = attr
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

    # Literals ##########################################################}}}{{{1
    # Closing Parenthesis ')' or Brackets '}'

    @token(r'\)')
    def t_CP(self, t):
        return t

    @token(r'\}')
    def t_CB(self, t):
        return t

    # Tokenizer Methods #################################################}}}{{{1

    def __init__(self, debug=False):
        self.debug = debug

    def lexer(self, **kwargs):
        kwargs.setdefault('optimize', not self.debug)
        kwargs.setdefault('lextab', 'hisp.tables.lextab')
        #kwargs.setdefault('reflags', re.DOTALL)
        return lex(module=self, **kwargs)
