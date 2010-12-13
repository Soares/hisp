from .doctypes import HTML, XHTML, DJANGO
from .libraries.core import macros as core
from .libraries import load
from .parse import Parser


class Hisp:
    def __init__(self, filetype=None, debug=False, libraries=None):
        self.filetype = filetype
        self.libraries = tuple(map(load, libraries or ())) + (core,)
        self.parse = Parser(debug).parse

    def setf(self, filetype):
        self.filetype = filetype

    def close(self, head):
        if self.filetype == DJANGO:
            return '%s{%%slash%%}' % head
        elif self.filetype == XHTML:
            return '%s/' % head
        return head

    def flag(self, value):
        if self.filetype == HTML:
            return self.eval(value)
        return '{0}="{0}"'.format(self.eval(value))

    def separate(self, *nodes):
        return u' '.join(map(self.eval, nodes))

    def chain(self, *nodes):
        return u'\n'.join(map(self.eval, nodes))

    def eval(self, value):
        from .nodes import Node
        from .exceptions import reraise
        if isinstance(value, unicode):
            return value
        if isinstance(value, basestring):
            return unicode(value)
        if isinstance(value, Node):
            return value.eval(self)
        try:
            return ''.join(map(self.eval, value))
        except TypeError:
            reraise("Can't evaluate unrecognized element '%s' % value")

    def indent(self, nodes, tab='\t'):
        if not nodes:
            return ''
        body = self.chain(*nodes)
        return tab + ('\n' + tab).join(body.split('\n'))

    def macro(self, name):
        for library in self.libraries:
            if name in library:
                return library[name]
        raise KeyError

    def convert(self, input):
        return self.chain(*self.parse(input))
