from django.conf import settings
from hisp.doctypes import DJANGO
from hisp import Hisp

def load(library):
    dot = library.rindex('.')
    module, name = library[:dot], library[dot+1:]
    try:
        module = __import__(module, fromlist=[name])
    except ImportError:
        raise ValueError("Can't find macro library %s" % library)
    return getattr(module, name)


def hisper(filetype=None, debug=False, libraries=None):
    if filetype is None and 'django_html' in settings.INSTALLED_APPS:
        filetype = DJANGO
    if libraries is None:
        libraries = settings.get('HISP_LIBRARIES', (
            'hisp.libraries.shortcuts.macros',
            'hisp.libraries.django.macros',
        ))
    macros = map(load, libraries)
    return Hisp(filetype=filetype, debug=debug, macros=macros)
