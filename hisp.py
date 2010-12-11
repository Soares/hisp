from doctypes import HTML

class ConversionError(SyntaxError):
    pass


class Hisp:
    def __init__(self):
        from macros import macros, django
        self.libraries = [macros, django]
        self.filetype = HTML

    def setf(self, filetype):
        self.filetype = filetype

    def separate(self, *nodes):
        return u' '.join(map(self.eval, nodes))

    def close(self, head):
        if self.filetype == HTML:
            return head
        return '%s/' % head

    def indent(self, body):
        return body

    def join(self, *nodes):
        return u''.join(map(self.eval, nodes))

    def combine(self, *nodes):
        return u''.join(map(self.eval, nodes))

    def flag(self, value):
        if self.filetype == 'HTML':
            return self.eval(value)
        return '{0}="{0}"'.format(self.eval(value))

    def eval(self, value):
        from nodes import Node
        if isinstance(value, unicode):
            return value
        if isinstance(value, basestring):
            return unicode(value)
        if isinstance(value, Node):
            return value.eval(self)
        return self.combine(*map(self.eval, value))

    def render(self, tag, attrs, children=None):
        from nodes import Elem
        return Elem.render(self, tag, attrs, children)

    def macro(self, name):
        for library in self.libraries:
            if name in library:
                return library[name]
        raise ConversionError('Unrecognized Macro: %s' % name)


if __name__ == '__main__':
    from parse import Parser
    data = open('examples/main.hisp').read()
    print data

    parser = Parser()
    output = parser.parse(data)
    print Hisp().eval(output)


'''
if __name__ == '__main__':
    lexer = Tokenizer().lexer()
    data = open('../base.html').read()
    lexer.input(data)
    while True:
         tok = lexer.token()
         if not tok: break
         print tok


if __name__ == '__main__':
    data = open('examples/test.hisp').read()
    print data
    tokenizer = Tokenizer()

    parser = Parser(tokenizer)
    output = parser.parse(data)
    print ''.join(map(unicode, output))
'''
