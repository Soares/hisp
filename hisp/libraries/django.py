from ..macros import Library
macros = Library()

def url(arg):
    return '{%%url %s%%}' % arg[1:] if arg.startswith('%') else arg

@macros.register
def internal(node, action=None):
    action and node.attrs.add('action', url(action))
    node.attrs.add('method', 'post')
    node.prepend('{%csrf_token%}')
    return node.render('form')

@macros.register
def goto(node, obj):
    node.attrs.add('href', '{{%s.get_absolute_url}}' % obj)
    return node.render('a')

@macros.register
def link(node, label):
    node.attrs.add('href', '{%%url %s%%}' % label)
    return node.render('a')

@macros.register
def addto(node, name):
    head = '{%%block %s%%}' % name
    node.prepend('{{block.super}}')
    from ..nodes import Block
    if Block.INDENT:
        body = node.indent(node.children)
    else:
        body = node.chain(*node.children)
    tail = '{%endblock%}'
    return node.chain(head, body, tail)
