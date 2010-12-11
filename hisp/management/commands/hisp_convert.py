from itertools import chain
from django.core.management.base import BaseCommand
from django.template import TemplateDoesNotExist
from django.template.loaders.app_directories import app_template_dirs
from django.template.loaders.app_directories import Loader as Apps
from django.template.loaders.filesystem import Loader as Fs
from django.conf import settings
from optparse import make_option
from hisp.management import hisper
from hisp.loaders.convert import Loader
import os


class Command(BaseCommand):
    help = """
    Convert all hisp files found in TEMPLATE_DIRS and APP_DIRECTORIES.
    "filename.hisp" will be converted and saved to "filename.hisp.html".
    This is where the hisp.loaders.compiled.loader will look for complied
    hisp files, so don't rename them if you're using that loader.
    """

    option_list = BaseCommand.option_list + (
        make_option('--noapps',
            type='store_false', dest='apps', default=True,
            help="Prevents the conversion of hisp templates found in APP_DIRECTORIES"),
        make_option('--nofs',
            type='store_false', dest='fs', default=True,
            help="Prevents the conversion of hisp templates found in TEMPLATE_DIRS"),
    )

    def handle(self, *args, **kwargs):
        loader = Loader(filter(bool, (
            kwargs['fs'] and Fs,
            kwargs['apps'] and Apps)))
        directories = chain(filter(bool, (
            kwargs['fs'] and settings.TEMPLATE_DIRS,
            kwargs['apps'] and app_template_dirs)))
        hisp = hisper()

        for dir in directories:
            for (root, _, files) in os.path.walk(dir):
                for filename in files:
                    try:
                        source, name = loader.load_template_source(filename, root)
                    except TemplateDoesNotExist:
                        continue
                    print 'Converting....', name
                    output = hisp.convert(source)
                    dest = os.path.join(root, filename + '.html')
                    with open(dest, 'w') as outfile:
                        outfile.write(output)
