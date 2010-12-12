from ply import yacc
import nodes
from hisp.tokenize import Tokenizer, ERROR_MAP
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
    if not p:
        raise SyntaxError('Unexpected end of file.')
    value = p.value
    err = "Unexpected %s at line %s: '%s'" % (ERROR_MAP[p.type], p.lineno, value)
    raise SyntaxError(err)

# Top Level Elements :::1

@parser('element : ELEM css_attrs body CP')
def p_element_open(elem, css_attrs, body, c):
    elem.set_css_attrs(css_attrs)
    elem.set_attrs(body.attrs)
    elem.set_children(body.children)
    return elem

@parser('element : CLOSER css_attrs attributes CP')
def p_element_closed(elem, css_attrs, attrs, c):
    elem.set_css_attrs(css_attrs)
    elem.set_attrs(attrs)
    return elem

@parser('block : BLOCK words EXTEND tokens CB')
def p_block_open(block, words, e, children, c):
    block.set_head(words)
    block.set_children(children)
    return block

@parser('block : BLOCK words CB')
def p_block_closed(block, words, c):
    block.set_head(words)
    return block

@parser('macro : MACRO css_attrs body CP')
def p_macro(macro, css_attrs, params, c):
    macro.set_css_attrs(css_attrs)
    macro.set_args(params.children)
    macro.set_kwargs(params.attrs)
    return macro

@parser('macro : MACRO css_attrs body EXTEND body CP')
def p_macro_extended(macro, css_attrs, params, e, body, c):
    macro.set_css_attrs(css_attrs)
    macro.set_args(params.children)
    macro.set_kwargs(params.attrs)
    macro.set_attrs(body.attrs)
    macro.set_children(body.children)
    return macro


# Specific Helpers :::1

@parser('attribute : ATTR text CP')
def p_attribute(attr, text, c):
    attr.set_value(text)
    return attr

@parser('body : token body')
def p_body_child(token, body):
    body.add_child(token)
    return body

@parser('body : attribute body')
def p_body_attr(attr, body):
    body.add_attr(attr)
    return body

@parser('body :')
def p_body_empty():
    return nodes.Body()

# Object Groups :::1

@parser('word : WORD | STRING | LITERAL')
def p_word(part):
    return part

@parser('django : DJANGO_COMMENT | block | VARIABLE')
def p_django(tag):
    return tag

@parser('statement : DOCTYPE | HTML_COMMENT | element | macro | django')
def p_statement(expr):
    return expr

@parser('token : statement | word')
def p_token(token):
    return token

# Object Lists :::1

@parser('statements : statement statements |')
def p_statements(*parts):
    return plist(parts)

@parser('tokens : token tokens |')
def p_tokens(*parts):
    return plist(parts)

@parser('css_attrs : CLASS css_attrs | ID css_attrs |')
def p_css_attrs(attr=None, attrs=None):
    if attr is None and attrs is None:
        return nodes.Attributes()
    attrs.add(attr)
    return attrs

@parser('attributes : attribute attribute |')
def p_attrs(attr=None, attrs=None):
    if attr is None and attrs is None:
        return nodes.Attributes()
    attrs.add(attr)
    return attrs

@parser('words : word words |')
def p_words(*parts):
    return plist(parts)

@parser('text : word text | django text |')
def p_text(text=None, value=None):
    if text is None and value is None:
        return nodes.Value()
    value.add(text)
    return value

# Parser Object :::1

class Parser:
    def __init__(self, debug=False):
        self.debug = debug
        self.parser = yacc.yacc(
                start='tokens', optimize=not debug, debug=False,
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
        start='tokens',
        outputdir='tables',
        optimize=True,
        debug=False)


if __name__ == '__main__':
    generate_tables()
