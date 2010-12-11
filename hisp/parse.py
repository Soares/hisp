from ply import yacc
import nodes
from hisp.tokenize import Tokenizer
tokens = Tokenizer.tokens

# Helper Functions :::1

def parser(regex):
    def decorate(fn):
        def parse(p):
            p[0] = fn(*p[1:])
        parse.__doc__ = '\n|'.join(regex.split('|'))
        return parse
    return decorate

def plist(p):
    try:
        elem, lst = p
    except ValueError:
        return []
    lst.insert(0, elem)
    return lst

def p_error(p):
    from hisp.exceptions import ConversionError
    raise ConversionError('Error parsing at %s' % yacc.token())

# Top Level Elements :::1

@parser('element : OP tag body CP')
def p_element_open(o, tag, body, c):
    return nodes.Elem(tag.name, tag.attrs + body.attrs, body.children)

@parser('element : OP_CLOSER tag attributes CP')
def p_element_closed(o, tag, attrs, c):
    return nodes.Elem(tag.name, tag.attrs + attrs)

@parser('block : OB_BLOCK NAME django_text EXTEND tokens CB')
def p_block_open(o, name, words, e, children, c):
    return nodes.Block(name, words, children)

@parser('block : OB_BLOCK NAME django_text CB')
def p_block_closed(o, name, words, c):
    return nodes.Block(name, words)

@parser('macro : OP_MACRO NAME css_attrs body CP')
def p_macro(o, name, attrs, params, c):
    return nodes.Macro(name, params.children, params.attrs, attrs)

@parser('macro : OP_MACRO NAME css_attrs body EXTEND body CP')
def p_macro_extended(o, name, attrs, params, e, body, c):
    return nodes.Macro(name, params.children, params.attrs,
            attrs + body.attrs, body.children)


# Specific Helpers :::1

@parser('name : NAME | block | VARIABLE')
def p_name(part):
    return part

@parser('tag : name css_attrs')
def p_tag_named(name, attrs):
    return nodes.Tag(name, attrs)

@parser('tag : css_attr css_attrs')
def p_tag_unnamed(attr, attrs):
    attrs.add(*attr)
    return nodes.Tag(None, attrs)

@parser('css_attr : CLASS')
def p_class(part):
    return ('class', part)

@parser('css_attr : ID')
def p_id(part):
    return ('id', part)

@parser('attribute : OP_ATTR name text CP')
def p_attribute(o, name, text, c):
    return (name, text)

@parser('body : token body')
def p_body_child(token, body):
    body.add_child(token)
    return body

@parser('body : attribute body')
def p_body_attr(attr, body):
    body.add_attr(*attr)
    return body

@parser('body :')
def p_body_empty():
    return nodes.Body()

# Object Groups :::1

@parser('django : DJANGO_COMMENT | block | VARIABLE')
def p_django(tag):
    return tag

@parser('expression : DOCTYPE | HTML_COMMENT | element | macro | django')
def p_expression(expr):
    return expr

@parser('django_part : macro | SYMBOLS | NAME | STRING | dothash_name')
def p_tagexpression(part):
    return part

@parser('text_part : django_part | django')
def p_texpression(text):
    return text

@parser('token : NAME | SYMBOLS | STRING | expression | dothash_name')
def p_token(token):
    return token

@parser('dothash_name : CLASS')
def p_dot_name(cls):
    return '.' + cls

@parser('dothash_name : ID')
def p_hash_name(id):
    return '#' + id

# Object Lists :::1

@parser('expressions : expression expressions |')
def p_expressions(*parts):
    return plist(parts)

@parser('tokens : token tokens |')
def p_tokens(*parts):
    return plist(parts)

@parser('css_attrs : css_attr css_attrs |')
def p_css_attrs(*parts):
    try:
        (name, value), attrs = parts
    except ValueError:
        return nodes.Attributes()
    attrs.add(name, value)
    return attrs

@parser('attributes : attribute attribute |')
def p_attrs(*parts):
    return plist(parts)

@parser('django_text : django_part django_text |')
def p_django_text(*parts):
    return plist(parts)

@parser('text : text_part text |')
def p_text(*parts):
    try:
        new, text = parts
    except ValueError:
        return nodes.Text()
    text.add(new)
    return text

# Parser Object :::1

class Parser:
    def __init__(self, debug=False):
        self.debug = debug
        self.parser = yacc.yacc(
                start='expressions', optimize=not debug, debug=False,
                tabmodule='hisp.tables.parsetab', write_tables=False)

    def parse(self, data):
        lexer = Tokenizer(self.debug).lexer()
        return self.parser.parse(data, lexer, debug=self.debug)


def generate_tables():
    Tokenizer(False).lexer(
        outputdir='tables',
        lextab='lextab',
        optimize=True)
    yacc.yacc(
        start='expressions',
        outputdir='tables',
        optimize=True,
        debug=False)


if __name__ == '__main__':
    generate_tables()
