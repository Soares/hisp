from functools import partial

class Library(dict):
    def register(self, fn=None, name=None, **kwargs):
        if fn is None:
            # @register(name='name')
            return partial(self.register, name=name, **kwargs)
        if name is None and isinstance(fn, str):
            # @register('name')
            return self.register(name=fn, **kwargs)
        elif isinstance(fn, str):
            # register('name', fn)
            name, fn = fn, name
        elif name is None:
            # @register
            name = fn.__name__
        self[name] = fn


class BoundMacro:
    def __init__(self, node, hisp, fn):
        for proxy in ['join', 'separate', 'combine', 'indent', 'close', 'flag']:
            setattr(self, proxy, getattr(hisp, proxy))

        self.hisp, self.fn = hisp, fn
        args = map(hisp.eval, node.args)
        kwargs = dict((name, map(hisp.eval, values))
            for (name, values) in node.kwargs.items())
        self.attrs = node.attrs
        self.children = node.children
        self.rendered = fn(self, *args, **kwargs)

    def use(self, args, kwargs):
        if self.children is None:
            self.children = []
        for arg in reversed(args):
            self.children.insert(0, arg)
        for (key, values) in kwargs.items():
            self.attrs.merge(key, values)

    def append(self, child):
        self.children.append(child)

    def prepend(self, child):
        self.children.insert(0, child)

    def render(self, tag, attrs=None, children=None):
        from nodes import Elem
        attrs = self.attrs if attrs is None else attrs
        children = self.children if children is None else children
        return Elem.render(self.hisp, tag, attrs, children)


django = Library()
macros = Library()


@django.register
def internal(node, *args, **kwargs):
    node.use(args, kwargs)
    node.prepend('{%csrf_token%}')
    return node.render('form')

@django.register
def goto(node, obj):
    node.attrs.add('href', '{{%s.get_absolute_url}}' % obj)
    return node.render('a')

@django.register
def link(node, label):
    node.attrs.add('href', '{%%url %s%%}' % label)
    return node.render('a')


def input(type):
    def input(node, *args, **kwargs):
        node.use(args, kwargs)
        node.attrs.add('type', type)
        return node.render('input')
    return input

for type in ('checkbox', 'file', 'hidden',
             'image', 'password', 'radio',
             'reset', 'submit', 'text'):
    macros.register(type, input(type))

@macros.register('if')
def conditional(node, *args):
    head = '<!--[if %s]>' % node.separate(*args)
    body = node.indent(node.children)
    tail = '<![endif]-->'
    return node.join(head, body, tail)
