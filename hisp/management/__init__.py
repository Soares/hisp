from django.conf import settings
from hisp.doctypes import DJANGO
from hisp import Hisp


def hisper(filetype=None, debug=False, libraries=None):
    if filetype is None and 'django_html' in settings.INSTALLED_APPS:
        filetype = DJANGO
    if libraries is None:
        libraries = settings.get('HISP_LIBRARIES', (
            'hisp.libraries.django.macros',
        ))
    return Hisp(filetype=filetype, debug=debug, libraries=libraries)
