from django.core.management.base import BaseCommand
from optparse import make_option
from hisp.doctypes import HTML, XHTML, DJANGO
from hisp.management import hisper


class Command(BaseCommand):
    help = """
    Convert hisp files into html files.
    Given no args, convert hisp files found by the hisp template loaders.
    Given args, will convert all named files.
    filename.hisp will be converted to filename.hisp.html
    See --help for other options.
    """

    option_list = BaseCommand.option_list + (
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
        make_option('-p', '--print',
            action='store_true', dest='show', default=False,
            help='Write the output to stdout. '
                 'Only valid when a single arg is given.'),
        make_option('-o',
            action='store', type='string', dest='outfile', default=False,
            help='The destination for output. '
                 'Only valid when a single arg is given.'),
    )

    def locate(self, filename):
        pass

    def destination(self, path):
        return path + '.hisp'

    def convert_file(self, hisp, filename, outfile=False, show=False):
        path = self.locate(filename)
        outfile = outfile and self.destination(path)
        with open(path) as file:
            output = hisp.convert(file.read())
        if show:
            print output
        if outfile:
            with open(outfile, 'w') as dest:
                dest.write(output)

    def convert_all(self, hisp):
        pass

    def handle(self, *args, **kwargs):
        filetype = dict(
                html=HTML,
                xhtml=XHTML,
                django=DJANGO
        )[kwargs.pop('filetype')]
        libraries = kwargs.pop('libraries') or None
        debug = kwargs.pop('debug')
        hisp = hisper(filetype=filetype, debug=debug, libraries=libraries)

        if len(args) == 1:
            return self.convert_file(hisp, args[0], **kwargs)
        if kwargs['show']:
            raise ValueError("Can't print to stdout when converting multiple files.")
        if kwargs['outfile']:
            raise ValueError("Can't output to one file when converting multiple files.")
        if len(args) == 0:
            return self.convert_all(hisp)

        kwargs['outfile'] = True
        for arg in args:
            self.convert_file(hisp, arg, **kwargs)
