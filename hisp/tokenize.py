from ply.lex import TOKEN, lex
import nodes
import re

def token(regex, front=0, back=0):
    @TOKEN(regex)
    def token(lexer, t):
        if front:
            t.value = t.value[front:]
        if back:
            t.value = t.value[:-back]
        return t
    return token


class Tokenizer:
    tokens = (
        'DJANGO_COMMENT',
        'HTML_COMMENT',
        'DOCTYPE',
        'ATTR',
        'CLOSER',
        'MACRO',
        'ELEM',
        'BLOCK',
        'EXTEND',
        'CB',
        'CP',
        'VARIABLE',
        'CLASS',
        'ID',
        'STRING',
        'LITERAL',
        'CDATA',
        'WORD',
    )

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_ignore_COMMENT(self, t):
        r'\{!([^}\\]|\\.)*\}'
        pass

    def t_HTML_COMMENT(self, t):
        r'\(!([^)\\]|\\.)*\)'
        t.value = nodes.HtmlComment(t.value[2:-1])
        return t

    def t_DJANGO_COMMENT(self, t):
        r'\{\#([^}\\]|\\.)*\}'
        t.value = nodes.DjangoComment(t.value[2:-1])
        return t

    def t_DOCTYPE(self, t):
        r'\(~([^)\\]|\\.)*\)'
        t.value = nodes.Doctype(t.value[2:-1])
        return t

    def t_ATTR(self, t):
        r'\(:\s*[\w-]+'
        t.value = nodes.Attribute(t.value[2:])
        return t

    def t_MACRO(self, t):
        r'\(%\s*[^\s{(.#~)}]+'
        t.value = nodes.Macro(t.value[2:], t.lexer.lineno)
        return t

    def t_CLOSER(self, t):
        r'\(/\s*[\w-]*'
        t.value = nodes.Elem(t.value[2:], t.lexer.lineno)
        return t

    def t_ELEM(self, t):
        r'\(\s*[\w-]*'
        t.value = nodes.Elem(t.value[1:], t.lexer.lineno)
        return t

    def t_BLOCK(self, t):
        r'\{%([^"~}\\]|\\.|"([^"\\]|\\.)*")+(?=[~}])'
        # A block is {% followed by
        # any text except "'s, \'s, }'s, and ~'s
        # any escaped characters
        # any string literals
        # up to but not including a } or a ~
        t.value = nodes.Block(t.value[2:], t.lexer.lineno)
        return t

    def t_EXTEND(self, t):
        r'~'
        return t

    def t_VARIABLE(self, t):
        r'\{([^}\\]|\\.)*\}'
        t.value = nodes.Variable(t.value[1:-1])
        return t

    def t_CP(self, t):
        r'\)'
        return t

    def t_CB(self, t):
        r'\}'
        return t

    def t_CLASS(self, t):
        r'(?<!\s)\.([\w-]+)'
        attr = nodes.Attribute('class')
        attr.set_value(t.value[1:])
        t.value = attr
        return t

    def t_ID(self, t):
        r'(?<!\s)\#([\w-]+)'
        attr = nodes.Attribute('id')
        attr.set_value(t.value[1:])
        t.value = attr
        return t

    def t_STRING(self, t):
        r'"([^"\\]|\\.)*"'
        t.value = nodes.String(t.value[1:-1])
        return t

    def t_LITERAL(self, t):
        r"'([^'\\]|\\.)*'"
        t.value = nodes.Literal(t.value[1:-1])
        return t

    def t_CDATA(self, t):
        r'<([^>\\]|\\.)*>'
        t.value = nodes.CData(t.value[1:-1])
        return t

    def t_WORD(self, t):
        r'[^<\s"\'>)}]+'
        return t

    def t_error(self, t):
        raise SyntaxError(t)

    t_ignore = ' \t'

    def __init__(self, debug=False):
        self.debug = debug

    def lexer(self, **kwargs):
        kwargs.setdefault('optimize', not self.debug)
        kwargs.setdefault('lextab', 'hisp.tables.lextab')
        #kwargs.setdefault('reflags', re.DOTALL)
        return lex(module=self, **kwargs)


ERROR_MAP = {
    'DJANGO_COMMENT': 'django comment',
    'HTML_COMMENT': 'html comment',
    'DOCTYPE': 'doctype declaration',
    'ATTR': 'attribute',
    'CLOSER': ')',
    'MACRO': 'macro',
    'ELEM': 'tag',
    'BLOCK': 'block',
    'EXTEND': '~',
    'CB': '}',
    'CP': '(',
    'VARIABLE': 'django variable',
    'CLASS': 'class attribute',
    'ID': 'id attribute',
    'NAME': 'word',
    'STRING': 'string',
    'WORD': 'text',
}
