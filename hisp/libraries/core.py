from hisp.macros import Library
macros = Library()

@macros.register('if')
def conditional(node, *args):
    head = '<!--[if %s]>' % node.separate(*args)
    body = node.join(node.children)
    tail = '<![endif]-->'
    return node.chain(head, body, tail)

@macros.register
def javascript(node, cdata, *args, **kwargs):
    node.use(args, kwargs)
    node.attrs.add('type', 'text/javascript')
    node.prepend(cdata)
    return node.render('script')


@macros.register
def css(node, cdata, *args, **kwargs):
    node.use(args, kwargs)
    node.attrs.add('type', 'text/css')
    node.prepend(cdata)
    return node.render('script')


def input(type):
    def input(node, *args, **kwargs):
        node.use(args, kwargs)
        node.attrs.add('type', type)
        return node.render('input')
    return input


for type in ('checkbox', 'file', 'hidden',
             'image', 'password', 'radio',
             'reset', 'submit', 'text', 'button'):
    macros.register(type, input(type))
