from ply import yacc
import nodes
from .tokenize import Tokenizer
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
    from .exceptions import ConversionError
    raise ConversionError('Error parsing at %s' % yacc.token())

# Top Level Elements :::1

@parser('element : OP tag body CP')
def p_element_open(o, tag, body, c):
    return nodes.Elem(tag.name, tag.attrs + body.attrs, body.children)

@parser('element : OP_CLOSER tag attributes CP')
def p_element_closed(o, tag, attrs, c):
    return nodes.Elem(tag.name, tag.attrs + attrs)

@parser('block : OB_BLOCK NAME tagtext EXTEND tokens CB')
def p_block_open(o, name, words, e, children, c):
    return nodes.Block(name, words, children)

@parser('block : OB_BLOCK NAME tagtext CB')
def p_block_closed(o, name, words, c):
    return nodes.Block(name, words)

@parser('macro : OP_MACRO NAME cssattrs body CP')
def p_macro(o, name, attrs, params, c):
    return nodes.Macro(name, params.children, params.attrs, attrs)

@parser('macro : OP_MACRO NAME cssattrs body EXTEND body CP')
def p_macro_extended(o, name, attrs, params, e, body, c):
    return nodes.Macro(name, params.children, params.attrs,
            attrs + body.attrs, body.children)


# Specific Helpers :::1

@parser('name : NAME | block | VARIABLE')
def p_name(part):
    return part

@parser('tag : name cssattrs')
def p_tag_named(name, attrs):
    return nodes.Tag(name, attrs)

@parser('tag : cssattr cssattrs')
def p_tag_unnamed(attr, attrs):
    attrs.add(*attr)
    return nodes.Tag(None, attrs)

@parser('cssattr : CLASS')
def p_class(part):
    return ('class', part)

@parser('cssattr : ID')
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

@parser('expression : DOCTYPE | COMMENT | element | block | macro | VARIABLE | STRING')
def p_expression(part):
    return part

@parser('texpression : COMMENT | block | macro | VARIABLE | STRING | WORD | NAME')
def p_texpression(part):
    return part

@parser('tagexpression : macro | WORD | NAME | STRING')
def p_tagexpression(part):
    return part

@parser('token : NAME | WORD | expression')
def p_token(token):
    return token

# Object Lists :::1

@parser('expressions : expression expressions |')
def p_expressions(*parts):
    return plist(parts)

@parser('tokens : token tokens |')
def p_tokens(*parts):
    return plist(parts)

@parser('cssattrs : cssattr cssattrs |')
def p_cssattrs(*parts):
    try:
        (name, value), attrs = parts
    except ValueError:
        return nodes.Attributes()
    attrs.add(name, value)
    return attrs

@parser('attributes : attribute attribute |')
def p_attrs(*parts):
    return plist(parts)

@parser('tagtext : tagexpression tagtext |')
def p_tagtext(*parts):
    return plist(parts)

@parser('text : texpression text |')
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
        self.parser = yacc.yacc(start='expressions')

    def parse(self, data):
        lexer = Tokenizer().lexer()
        return self.parser.parse(data, lexer, debug=self.debug)
