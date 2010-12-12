from django.conf import settings
from django.core.excepctions import ImproperlyConfigured
from hisp.doctypes import DJANGO, FILETYPES
from hisp import Hisp


def hisper(filetype=None, debug=False, libraries=None):
    if filetype is None and 'django_html' in settings.INSTALLED_APPS:
        filetype = DJANGO
    if filetype is None:
        filetype = settings.get('HISP_FILETYPE', None)
        filetype = filetype and filetype.upper()
        if filetype not in FILETYPES:
            raise ImproperlyConfigured("HISP_FILETYPE must be one of "
                "'html', 'xhtml', 'django', or None")
    if libraries is None:
        libraries = settings.get('HISP_LIBRARIES', (
            'hisp.libraries.django.macros',
        ))
    return Hisp(filetype=filetype, debug=debug, libraries=libraries)
