from ply.lex import TOKEN, lex
import nodes

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
        'COMMENT',
        'DOCTYPE',
        'OP_ATTR',
        'OP_CLOSER',
        'OP_MACRO',
        'OP',
        'OB_BLOCK',
        'EXTEND',
        'CB',
        'CP',
        'VARIABLE',
        'CLASS',
        'ID',
        'NAME',
        'WORD',
        'STRING',
    )

    def t_COMMENT(self, t):
        r'\(\s*!([^)\\]*(?:\\.[^)\\]*)*)\)'
        t.value = nodes.Comment(t.value[2:-1])
        return t

    def t_DOCTYPE(self, t):
        r'\(\s*~([^)\\]*(?:\\.[^)\\]*)*)\)'
        t.value = nodes.Doctype(t.value[2:-1])
        return t

    def t_OP_ATTR(self, t):
        r'\(\s*:'
        return t

    def t_OP_MACRO(self, t):
        r'\(\s*%'
        return t

    def t_OP_CLOSER(self, t):
        r'\(\s*/'
        return t

    def t_OP(self, t):
        r'\('
        return t

    def t_OB_BLOCK(self, t):
        r'\{\s*%'
        return t

    def t_EXTEND(self, t):
        r'~'
        return t

    def t_VARIABLE(self, t):
        r'\{([^}\\]*(?:\\.[^}\\]*)*)\}'
        t.value = nodes.Variable(t.value[1:-1])
        return t

    def t_CP(self, t):
        r'\)'
        return t

    def t_CB(self, t):
        r'\}'
        return t

    def t_CLASS(self, t):
        r'\.([\w-]+)'
        t.value = t.value[1:]
        return t

    def t_ID(self, t):
        r'\#([\w-]+)'
        t.value = t.value[1:]
        return t

    def t_NAME(self, t):
        r'[\w-]+'
        return t

    def t_WORD(self, t):
        r'[^({~"\s})]*[^({~"\s\w})][^({~"\s})]*'
        return t

    def t_STRING(self, t):
        r'"([^"\\]*(?:\\.[^"\\]*)*)"'
        t.value = nodes.Atom(t.value[1:-1])
        return t

    def t_error(self, t):
        from .exceptions import ConversionError
        raise ConversionError("Illegal Character '%s'" % t.value[0])

    t_ignore = ' \t\n'

    def __init__(self, debug=False):
        self.debug = debug

    def lexer(self):
        return lex(module=self, optimize=not self.debug)
