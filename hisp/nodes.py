from itertools import chain

class Node:
    def eval(self, hisp):
        return ''

# Atoms :::1

class Atom(Node):
    render = '%s'

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '%s (%s)' % (self.__class__.__name__, self.value)

    def eval(self, hisp):
        return unicode(self.render) % self.value


class String(Atom):
    def __repr__(self):
        return '"%s"' % self.value


class HtmlComment(Atom):
    render = '<!--%s-->'


class DjangoComment(Atom):
    render = '{#%s#}'


class Variable(Atom):
    render = '{{%s}}'


class Doctype(Atom):
    def __init__(self, value):
        self.value = value.strip().lower()

    def eval(self, hisp):
        from hisp.exceptions import SyntaxError
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
        raise SyntaxError('Unrecognized Doctype: "%s"' % self.value)



# Expressions :::1

class Elem(Node):
    @classmethod
    def render(cls, hisp, tag, attrs, children=None):
        head = hisp.separate(tag, attrs) if attrs else tag
        if children is None:
            return u'<%s>' % hisp.close(head)
        body = hisp.join(children)
        return hisp.chain(u'<%s>' % head, body, u'</%s>' % tag)

    def __init__(self, tag, attrs, children=None):
        self.tag, self.attrs, self.children = tag, attrs, children

    def __repr__(self):
        return 'Elem(%s)' % self.tag

    def eval(self, hisp):
        return self.render(hisp, self.tag, self.attrs, self.children)


class Attributes(Node, dict):
    def add(self, key, value):
        self.setdefault(key, set()).add(value)

    def merge(self, key, values):
        self.setdefault(key, set()).update(values)

    def __add__(self, other):
        new = self.__class__()
        for (key, values) in chain(self.items(), other.items()):
            new.merge(key, values)
        return new

    def eval(self, hisp):
        return hisp.separate(*(
            u'%s="%s"' % (name, hisp.separate(*values))
            if any(values) else hisp.flag(name)
            for (name, values) in self.items()))


class Text(Node):
    def __init__(self, parts=None):
        self.parts = parts or []

    def __repr__(self):
        return 'Text'

    def __len__(self):
        return len(self.parts)

    def add(self, part):
        self.parts.insert(0, part)

    def eval(self, hisp):
        return hisp.join(self.parts)


class Tag:
    DEFAULT = 'div'

    def __init__(self, name, attrs):
        self.name = self.DEFAULT if name is None else name
        self.attrs = attrs

    def __repr__(self):
        return 'Tag(%s)' % self.name


class Body:
    def __init__(self):
        self.attrs = Attributes()
        self.children = []

    def add_child(self, child):
        self.children.insert(0, child)

    def add_attr(self, name, value):
        self.attrs.add(name, value)

    def __repr__(self):
        return u'Body{%s}(%s)' % (len(self.attrs), len(self.children))


class Macro(Node):
    def __init__(self, name, args, kwargs, attrs, children=None, lineno=None):
        self.name, self.args, self.kwargs = name, args, kwargs
        self.attrs, self.children = attrs, children
        self.lineno = lineno

    def __repr__(self):
        return 'Macro(%s)' % self.name

    def eval(self, hisp):
        from hisp.macros import BoundMacro
        from hisp.exceptions import MacroNotFound
        try:
            macro = hisp.macro(self.name)
        except KeyError:
            raise MacroNotFound("Can not find macro '%s' on line %d" % (self.name, self.lineno))
        return BoundMacro(self, hisp, macro).rendered


class Block(Node):
    def __init__(self, name, words, children=None):
        self.name, self.words, self.children = name, words, children

    def __repr__(self):
        return 'Block(%s)' % self.name

    def eval(self, hisp):
        tag = hisp.separate(self.name, *self.words)
        if self.children is None:
            return u'{%%%s%%}' % tag
        body = hisp.join(self.children)
        return u'{%%%s%%}%s{%%end%s%%}' % (tag, body, self.name)
