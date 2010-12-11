#!/usr/bin/env python
from optparse import OptionParser, make_option
from hisp.doctypes import HTML, XHTML, DJANGO
from hisp import Hisp

option_list = (
    make_option('-t', '--filetype',
        type='choice', action='store', dest='filetype',
        choices=['xhtml', 'html', 'django'], default=None,
        help='Set the output file type'),
    make_option('-d', '--debug',
        action='store_true', dest='debug', default=False,
        help='Run the parser in debug mode'),
    make_option('-l', '--link',
        action='append', dest='libraries',
        help='Macro libraries to link into hisp'),
    make_option('-o',
        action='store', type='string', dest='outfile', default=False,
        help='The destination for output'),
)


def main():
    parser = OptionParser(option_list=option_list)
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error('Please give a single file for converson.')
    filename, = args

    filetype = {
        'html': HTML,
        'xhtml': XHTML,
        'django': DJANGO,
    }.get(options.pop('filetype'))
    libraries = options.pop('libraries') or None
    debug = options.pop('debug')
    hisp = Hisp(filetype=filetype, debug=debug, libraries=libraries)

    with open(filename) as source:
        input = source.read()
    output = hisp.convert(input)

    if options['outfile']:
        with open(options['outfile'], 'w') as dest:
            dest.write(output)
    else:
        print output

if __name__ == '__main__':
    main()
