from ply import yacc
import nodes
from hisp.tokenize import Tokenizer, ERROR_MAP
tokens = Tokenizer.tokens

# Parser Functions #################################################{{{1
# Parser Decorator, List Maker, Error Handling

def parser(regex):
    def decorate(fn):
        def parse(p):
            p[0] = fn(*p[1:])
        parse.__doc__ = '\n|'.join(regex.split('|'))
        return parse
    return decorate


def p_error(p):
    if not p:
        raise SyntaxError('Unexpected end of file.')
    value = p.value
    err = "Unexpected %s at line %s: '%s'" % (ERROR_MAP[p.type], p.lineno, value)
    raise SyntaxError(err)

# Statements ########################################################}}}{{{1
# Elements, Closing Elements, Blocks, and Macros

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

@parser('block : OPEN_BLOCK tokens CB')
def p_block_open(block, children, c):
    block.set_children(children)
    return block

@parser('block : CLOSED_BLOCK')
def p_block_closed(block):
    return block

@parser('macro : MACRO css_attrs body CP')
def p_macro(macro, css_attrs, params, c):
    macro.set_css_attrs(css_attrs)
    macro.set_attrs(params.attrs)
    macro.set_children(params.children)
    return macro

# SubExpressions ####################################################}}}{{{1
# CSS Attributes, Attributes, Tokens, Body

@parser('css_attrs : CLASS css_attrs | ID css_attrs |')
def p_css_attrs(attr=None, attrs=None):
    if attr is None and attrs is None:
        return nodes.Attributes()
    attrs.add(*attr)
    return attrs

@parser('attributes : attribute attributes |')
def p_attrs(attr=None, attrs=None):
    if attr is None and attrs is None:
        return nodes.Attributes()
    attrs.add(*attr)
    return attrs

@parser('tokens : token tokens |')
def p_tokens(token=None, tokens=None):
    if token is None and tokens is None:
        return []
    tokens.insert(0, token)
    return tokens

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

# SubExpression Components ##########################################}}}{{{1
# Attribute, Token

@parser('attribute : ATTR value CP')
def p_attribute(attr, value, c):
    return (attr, value)

@parser('token : DOCTYPE | HTML_COMMENT | element | macro | django | word')
def p_token(token):
    return token

# Object Groups #####################################################}}}{{{1
# Django, Value, Word

@parser('django : block | VARIABLE | DJANGO_COMMENT')
def p_django(tag):
    return tag

@parser('value : word value | django value |')
def p_value(new=None, value=None):
    if new is None and value is None:
        return nodes.Value()
    value.add(new)
    return value

@parser('word : WORD | STRING | LITERAL | CDATA')
def p_word(part):
    return part

# Parser Object #####################################################}}}{{{1

class Parser:
    def __init__(self, debug=False):
        self.debug = debug
        self.parser = yacc.yacc(
                start='tokens', optimize=not debug, debug=False,
                tabmodule='hisp.tables.parsetab', write_tables=False)

    def parse(self, data):
        lexer = Tokenizer(self.debug).lexer()
        return self.parser.parse(data, lexer, debug=self.debug)

# Table Regeneration ################################################}}}{{{1
# Remove tables from the python path and call this to regenerate them

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
