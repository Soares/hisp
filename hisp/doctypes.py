HTML, XHTML, XML, DJANGO = 'HTML', 'XHTML', 'XML', 'DJANGO'
import re

def compile(filetype_dict):
    return dict((re.compile('^%s$' % k), v) for (k, v) in filetype_dict.items())


DOCTYPES = {
    HTML: compile({
        r'(html)?\s*(5?)': '<!DOCTYPE HTML>',

        r'(html)?\s*4\s*(t(ransitional)?)?': '<!DOCTYPE html PUBLIC '
            '"-//W3C//DTD HTML 4.01 Transitional//EN" '
            '"http://www.w3.org/TR/html4/loose.dtd">',
        r'(html)?\s*4\s*s(strict)?': '<!DOCTYPE html PUBLIC '
            '"-//W3C//DTD HTML 4.01//EN" '
            '"http://www.w3.org/TR/html4/strict.dtd">',
        r'(html)?\s*4\s*f(rameset)?': '<!DOCTYPE html PUBLIC '
            '"-//W3C//DTD HTML 4.01 Frameset//EN" '
            '"http://www.w3.org/TR/html4/frameset.dtd">',

        r'(html)?\s*3': '<!DOCTYPE HTML PUBLIC '
            '"-//W3C//DTD HTML 3.2 Final//EN">',
        r'(html)?\s*2': '<!DOCTYPE HTML PUBLIC '
            '"-//IETF//DTD HTML//EN">',

        r'h(tml)? silent': '',
    }),
    XHTML: compile({
        r'x(html)?\s*5': '<!DOCTYPE HTML>',
        r'x(html)?\s*(t(ransitional)?)?': '<!DOCTYPE html PUBLIC '
            '"-//W3C//DTD XHTML 1.0 Transitional//EN" '
            '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">',
        r'x(html)?\s*s(trict)?': '<!DOCTYPE html PUBLIC '
            '"-//W3C//DTD XHTML 1.0 Strict//EN" '
            '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">',
        r'x(html)?\s*r(dfa)?': '<!DOCTYPE html PUBLIC '
            '"-//W3C//DTD XHTML+RDFa 1.0//EN" '
            '"http://www.w3.org/MarkUp/DTD/xhtml-rdfa-1.dtd">',

        r'x?(html)?\s*1\.1': '<!DOCTYPE html PUBLIC '
            '"-//W3C//DTD XHTML 1.1//EN" '
            '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">',
        r'x(html)?\s*f(rameset)?': '<!DOCTYPE html PUBLIC '
            '"-//W3C//DTD XHTML 1.0 Frameset//EN" '
            '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">',
        r'x(html)?\s*b(basic)?': '<!DOCTYPE html PUBLIC '
            '"-//W3C//DTD XHTML Basic 1.1//EN" '
            '"http://www.w3.org/TR/xhtml-basic/xhtml-basic11.dtd">',
        r'x(html)?\s*m(mobile)?': '<!DOCTYPE html PUBLIC '
            '"-//WAPFORUM//DTD XHTML Mobile 1.2//EN" '
            '"http://www.openmobilealliance.org/tech/DTD/xhtml-mobile12.dtd">',

        r'x(html)? silent': '',
    }),
    XML: compile({
        r'xml': '<?xml version="1.0" encoding="utf-8" ?>',
        r'xml\s+(\S+)': r'<?xml version="1.0" encoding="\1" ?>',
    }),
    DJANGO: compile({
        r'(html4|html4trans|xhtml1|xhtml1trans|html5)( silent|)':
            r'{% doctype \1\2 %}',
    }),
}

FILETYPES = {
    None: (HTML, XHTML, XML),
    HTML: (HTML, XML),
    XHTML: (XHTML, XML),
    DJANGO: (DJANGO, XML),
}
