from .doctypes import HTML, XHTML, DJANGO
from .libraries.shortcuts import macros as shortcuts
from .exceptions import ConversionError
from .parse import Parser


class Hisp:
    def __init__(self, filetype=None, debug=False,
            libraries=(shortcuts,)):
        self.filetype = filetype
        self.libraries = libraries
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
        return self.join(nodes)

    def join(self, nodes):
        return u''.join(map(self.eval, nodes))

    def eval(self, value):
        from nodes import Node
        if isinstance(value, unicode):
            return value
        if isinstance(value, basestring):
            return unicode(value)
        if isinstance(value, Node):
            return value.eval(self)
        try:
            return self.combine(*map(self.eval, value))
        except TypeError:
            raise ConversionError("Can't evaluate unrecognized element '%s'" % value)

    def macro(self, name):
        for library in self.libraries:
            if name in library:
                return library[name]
        raise ConversionError('Unrecognized Macro: %s' % name)

    def convert(self, input):
        return self.eval(self.parse(input))