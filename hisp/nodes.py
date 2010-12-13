from .exceptions import ParseError
import re

# Base Class #######################################################{{{1
# All evaluatable objects should extend this

class Node(object):
    def eval(self, hisp):
        return u''

# Atoms #############################################################}}}{{{1
# Elements that can be trivially rendered turing tokenization
# They have to handle the escaping of escaped characters
# Comments, Constants

class Atom(Node):
    PATTERN, ESCAPE = u'%s', ''

    @classmethod
    def escape(cls, value, char):
        search = re.compile(r'((?<!\\)(?:\\\\)*)(\\%s)' % char)
        return search.sub(r'\1' + char, value)

    @classmethod
    def deslash(cls, value):
        return value.replace(r'\\', '\\')

    @classmethod
    def render(cls, value, escape=''):
        return cls.deslash(reduce(cls.escape, escape, value))

    def __init__(self, value):
        self.value = value
        self.rendered = self.PATTERN % self.render(self.value, self.ESCAPE)

    def __repr__(self):
        return self.rendered

    def __unicode__(self):
        return unicode(self.rendered)

    def eval(self, hisp):
        return self.rendered

# Comments ##########################################################}}}{{{2
# HTML Commets, Django Comments, and Hisp comments

class HtmlComment(Atom):
    PATTERN, ESCAPE = u'<!--%s-->', ')'


class DjangoComment(Atom):
    PATTERN, ESCAPE = u'{#%s#}', '}'


class Variable(Atom):
    PATTERN, ESCAPE = u'{{%s}}', '}'

# Constants #########################################################}}}{{{2
# Atoms that handle escaping characters
# Strings, Literal Strings, CDATA

class Literal(Atom):
    ESCAPE = "'"

    def __repr__(self):
        return "'%s'" % self.value


class String(Atom):
    ESCAPE = '"{'
    variable = re.compile(r'\{((?:[^}\\]|\\.)*)\}')

    def expand(self, match):
        return '{{%s}}' % unicode(Variable(match.group(1)))

    def __init__(self, value):
        value = self.variable.sub(self.expand, value)
        return super(String, self).__init__(value)

    def __repr__(self):
        return '"%s"' % self.value


class CData(Atom):
    PATTERN, ESCAPE = '<[CDATA[%s]]>', '>'

    def __repr__(self):
        return "<%s>" % self.value

# Statements ########################################################}}}{{{1
# Doctype, Element, Block, Macro

class Doctype(Node):
    def __init__(self, value):
        self.value = value.strip().lower()

    def eval(self, hisp):
        from .doctypes import DOCTYPES, FILETYPES
        consider = FILETYPES[hisp.filetype]
        for filetype in consider:
            for (regex, doctype) in DOCTYPES[filetype].items():
                if regex.match(self.value):
                    if filetype in FILETYPES:
                        hisp.setf(filetype)
                    return regex.sub(doctype, self.value)
        raise ParseError(u'Unrecognized Doctype: "%s"' % self.value)


class Elem(Node):
    DEFAULT = u'div'

    @classmethod
    def render(cls, hisp, tag, attrs, children=None):
        tag = tag or cls.DEFAULT
        head = hisp.separate(tag, attrs) if attrs else tag
        if children is None:
            return u'<%s>' % hisp.close(head)
        body = hisp.indent(children)
        if body:
            return hisp.chain(u'<%s>' % head, body, u'</%s>' % tag)
        return u'<%s></%s>' % (head, tag)

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
        return self.tag or '[no tag]'

    def eval(self, hisp):
        return self.render(hisp, self.tag, self.attrs, self.children)


class Macro(Node):
    def __init__(self, name, arg, lineno):
        self.name = name.upper()
        self.arg, self.lineno = arg, lineno
        self.children, self.attrs = [], None

    def set_css_attrs(self, attrs):
        self.attrs = attrs

    def set_attrs(self, attrs):
        self.attrs.update(attrs)

    def set_children(self, children):
        self.children = list(children)

    def __repr__(self):
        return '(%%%s...)' % self.name

    def eval(self, hisp):
        from .exceptions import MacroNotFound
        try:
            macro = hisp.macro(self.name)
        except KeyError:
            raise MacroNotFound(u"Can not find macro '%s' on line %d" % (
                self.name, self.lineno))
        try:
            return macro(hisp, self.name, self.arg, self.attrs, self.children)
        except Exception as e:
            raise MacroNotFound('Error rendering macro %s: %s' % (self.name, e))


class Block(Node):
    INDENT = False

    def __init__(self, head, lineno):
        self.name = head.strip().split()[0]
        self.head = Atom.render(head, '~}"')
        self.children = None

    def set_children(self, children):
        self.children = children

    def __repr__(self):
        return u'{%%%s...%%}' % self.name

    def eval(self, hisp):
        if self.children is None:
            return u'{%%%s%%}' % self.head
        head = u'{%%%s%%}' % self.head
        if self.INDENT:
            body = hisp.indent(self.children)
        else:
            body = hisp.chain(*self.children)
        end = u'{%%end%s%%}' % self.name
        return hisp.chain(head, body, end)

# SubExpressions ####################################################}}}{{{1
# Attributes, Body

class Attributes(Node, dict):
    def add(self, name, value):
        self.setdefault(name, []).append(value)

    def merge(self, key, values):
        self.setdefault(key, []).extend(values)

    def update(self, other):
        for (key, values) in other.items():
            self.merge(key, values)

    def eval(self, hisp):
        # We must create the attrs as a list first, because any errors
        # created during generation would be incorrectly caught and
        # re-raised as a generator error.
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
        self.attrs.add(*attr)

    def __repr__(self):
        return u'Body'

# Object Groups #####################################################}}}{{{1
# Value (for Attribute)

class Value(Node):
    def __init__(self):
        self.text = []

    def __repr__(self):
        return u''.join(map(repr, self.text))

    def __len__(self):
        return len(self.text)

    def add(self, text):
        self.text.insert(0, text)

    def eval(self, hisp):
        return u''.join(hisp.eval(self.text))
