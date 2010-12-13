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
        self[name.upper()] = BoundMacro(fn)


class BoundMacro:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, hisp, name, arg, attrs, children):
        for proxy in ['join', 'separate', 'chain', 'close', 'flag']:
            setattr(self, proxy, getattr(hisp, proxy))
        self.hisp = hisp
        self.name = name
        self.attrs = attrs
        self.children = children
        return self.fn(self) if arg is None else self.fn(self, arg)

    def append(self, child):
        self.children.append(child)

    def prepend(self, child):
        self.children.insert(0, child)

    def render(self, tag=None, attrs=None, children=None):
        from .nodes import Elem
        tag = self.name if tag is None else tag
        attrs = self.attrs if attrs is None else attrs
        children = self.children if children is None else children
        return Elem.render(self.hisp, tag, attrs, children)
