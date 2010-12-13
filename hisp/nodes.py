from hisp.exceptions import ParseError
import re

class Node:
    def eval(self, hisp):
        return u''

# Atoms :::1

class Atom(Node):
    render = u'%s'

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return u'%s (%s)' % (self.__class__.__name__, self.value)

    def eval(self, hisp):
        return unicode(self.render) % self.value


class Literal(Atom):
    @classmethod
    def escape(cls, value, char):
        search = re.compile(r'((?<!\\)(?:\\\\)*)(\\%s)' % char)
        return search.sub(r'\1' + char, value)

    @classmethod
    def deslash(cls, value):
        return value.replace(r'\\', '\\')

    @classmethod
    def render(cls, value, special):
        return cls.deslash(reduce(cls.escape, special, value))

    def __repr__(self):
        return u"'%s'" % self.value

    def eval(self, hisp):
        return self.render(self.value, "'")


class String(Literal):
    variable = re.compile(r'\{((?:[^}\\]|\\.)*)\}')

    def __repr__(self):
        return u'"%s"' % self.value

    def eval(self, hisp):
        return self.render(self.variable.sub(r'{{\1}}', self.value), '"{')


class CData(Literal):
    def __repr__(self):
        return "<%s>" % self.value

    def eval(self, hisp):
        return '<[CDATA[%s]]>' % self.render(self.value, '>')


class HtmlComment(Atom):
    render = u'<!--%s-->'


class DjangoComment(Atom):
    render = u'{#%s#}'


class Variable(Atom):
    render = u'{{%s}}'


class Doctype(Atom):
    def __init__(self, value):
        self.value = value.strip().lower()

    def eval(self, hisp):
        from hisp.doctypes import DOCTYPES, FILETYPES
        import re
        consider = FILETYPES[hisp.filetype]
        for filetype in consider:
            for (regex, doctype) in DOCTYPES[filetype].items():
                regex = r'^%s$' % regex
                if re.match(regex, self.value):
                    if filetype in FILETYPES:
                        hisp.setf(filetype)
                    return re.sub(regex, doctype, self.value)
        raise ParseError(u'Unrecognized Doctype: "%s"' % self.value)



# Statements :::1

class Elem(Node):
    DEFAULT = u'div'

    @classmethod
    def render(cls, hisp, tag, attrs, children=None):
        tag = tag or cls.DEFAULT
        head = hisp.separate(tag, attrs) if attrs else tag
        if children is None:
            return u'<%s>' % hisp.close(head)
        body = hisp.join(children)
        return hisp.chain(u'<%s>' % head, body, u'</%s>' % tag)

    def __init__(self, tag, lineno):
        self.tag = tag.strip() or None
        self.lineno = lineno
        self.children = None
        self.attrs = None

    def set_css_attrs(self, attrs):
        if not (self.tag or attrs):
            raise ParseError(u'Error: empty tag on line %s' % self.lineno)
        self.attrs = attrs

    def set_attrs(self, attrs):
        self.attrs.update(attrs)

    def set_children(self, children):
        self.children = children

    def __repr__(self):
        return (self.tag or '') + (self.attrs.clsids() if self.attrs else '')

    def eval(self, hisp):
        return self.render(hisp, self.tag, self.attrs, self.children)


class Macro(Node):
    def __init__(self, name, lineno):
        self.name = name.upper()
        self.lineno = lineno
        self.args, self.kwargs, self.attrs = None, None, None
        self.children = []

    def set_css_attrs(self, attrs):
        self.attrs = attrs

    def set_args(self, args):
        self.args = args

    def set_kwargs(self, attrs):
        self.kwargs = attrs

    def set_attrs(self, attrs):
        self.attrs.update(attrs)

    def set_children(self, children):
        self.children = list(children)

    def __repr__(self):
        return u'Macro(%s)' % self.name

    def eval(self, hisp):
        from hisp.macros import BoundMacro
        from hisp.exceptions import MacroNotFound
        try:
            macro = hisp.macro(self.name)
        except KeyError:
            raise MacroNotFound(u"Can not find macro '%s' on line %d" % (self.name, self.lineno))
        return BoundMacro(self, hisp, macro).rendered


class Block(Node):
    def __init__(self, head, lineno):
        self.name = head.strip().split()[0]
        self.head = Literal.render(head, "~}")
        self.children = None

    def set_children(self, children):
        self.children = children

    def __repr__(self):
        return u'Block(%s)' % self.name

    def eval(self, hisp):
        if self.children is None:
            return u'{%%%s%%}' % self.head
        body = hisp.join(self.children)
        return u'{%%%s%%}%s{%%end%s%%}' % (self.head, body, self.name)


# Items :::1

class Attribute:
    def __init__(self, name):
        self.name = name

    def set_value(self, value):
        self.value = value

    def __repr__(self):
        return u'Attr(%s)' % self.name


class Value(Node):
    def __init__(self):
        self.text = []

    def __repr__(self):
        return ''.join(map(repr, self.text))

    def __len__(self):
        return len(self.text)

    def add(self, text):
        self.text.insert(0, text)

    def eval(self, hisp):
        return hisp.join(self.text)

# Item Sets :::1

class Attributes(Node, dict):
    def add(self, *args):
        if len(args) not in (1, 2):
            raise TypeError('Attributes.add must be given either an attribute or a (name, value) pair')
        if len(args) is 1:
            attribute, = args
            attr, val = attribute.name, attribute.value
        else:
            attr, val = args
        self.setdefault(attr, set()).add(val)

    def merge(self, key, values):
        self.setdefault(key, set()).update(values)

    def update(self, other):
        for (key, values) in other.items():
            self.merge(key, values)

    def clsids(self):
        result = u''
        for (key, value) in self.items():
            if key == u'class':
                result += '.%s' % repr(value)
            if key == u'id':
                result += '#%s' % repr(value)
        return result

    def eval(self, hisp):
        attrs = [u'%s="%s"' % (name, hisp.separate(*values))
            if any(values) else hisp.flag(name)
            for (name, values) in self.items()]
        return hisp.separate(*attrs)

class Body:
    def __init__(self):
        self.attrs = Attributes()
        self.children = []

    def add_child(self, child):
        self.children.insert(0, child)

    def add_attr(self, attr):
        self.attrs.add(attr)

    def __repr__(self):
        return u'Body'
