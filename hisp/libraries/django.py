from ..macros import Library
macros = Library()

@macros.register
def internal(node, *args, **kwargs):
    node.use(args, kwargs)
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
    head = '{%%block %s%%}{{block.super}}' % name
    body = node.join(node.children)
    tail = '{%endblock%}'
    return node.chain(head, body, tail)