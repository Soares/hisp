from itertools import chain
from django.core.management.base import BaseCommand
from django.template.loaders.app_directories import app_template_dirs
from django.conf import settings
from optparse import make_option
import os


class Command(BaseCommand):
    help = """Clean all .hisp.html files from TEMPLATE_DIRS and APP_DIRECTORIES."""

    option_list = BaseCommand.option_list + (
        make_option('-a', '--apps',
            action='store_true', dest='apps', default=False,
            help='Clean the .hisp.html files in APP_DIRECTORIES as well'),
        make_option('--nofs',
            action='store_false', dest='fs', default=True,
            help='Prevent the cleaning of .hisp.html files in TEMPLATE_DIRS'),
    )

    def handle(self, *args, **kwargs):
        directories = chain(*filter(bool, (
            kwargs['fs'] and settings.TEMPLATE_DIRS,
            kwargs['apps'] and app_template_dirs)))
        for dir in directories:
            for (root, _, files) in os.walk(dir):
                for filename in files:
                    if filename.endswith('.hisp.html'):
                        path = os.path.join(root, filename)
                        print 'removing %s' % path
                        os.remove(path)
