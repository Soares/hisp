from ..macros import Library
macros = Library()

@macros.register('if')
def conditional(node, arg):
    head = '<!--[if %s]>' % arg
    body = node.join(node.children)
    tail = '<![endif]-->'
    return node.chain(head, body, tail)

@macros.register
def javascript(node):
    node.attrs.add('type', 'text/javascript')
    return node.render('script')


@macros.register
def css(node):
    node.attrs.add('type', 'text/css')
    return node.render('script')


def input(type):
    def input(node, name=None):
        name and node.attrs.add('name', name)
        node.attrs.add('type', type)
        return node.render('input')
    return input


for type in ('checkbox', 'file', 'hidden',
             'image', 'password', 'radio',
             'reset', 'submit', 'text', 'button'):
    macros.register(type, input(type))
