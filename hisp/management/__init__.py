from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from hisp.doctypes import DJANGO, FILETYPES
from hisp import Hisp


def hisper(filetype=None, debug=False, compress=False, libraries=None):
    if filetype is None and 'django_html' in settings.INSTALLED_APPS:
        filetype = DJANGO
    elif filetype is None:
        filetype = getattr(settings, 'HISP_FILETYPE', None)
        filetype = filetype and filetype.upper()
        if filetype not in FILETYPES:
            raise ImproperlyConfigured("HISP_FILETYPE must be one of "
                "'html', 'xhtml', 'django', or None.")
    if libraries is None:
        libraries = getattr(settings, 'HISP_LIBRARIES', (
            'hisp.libraries.django.macros',
        ))
    return Hisp(filetype=filetype,
            debug=debug,
            compress=compress,
            libraries=libraries)
