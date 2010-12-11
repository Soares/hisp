from hisp.macros import Library

def load(library):
    """
    Attempts to find a macro library.
    Given a macro library, returns that libary.
    Given a string, treat it as an import path to a macro Library.
    Failing that, treat it as an import path to a module, and see if
    it has a 'macros' attribute. If it does, use that as the Library.
    """
    if isinstance(library, Library):
        return library
    err = ValueError("Can't find macro library %s" % library)
    dot = library.rindex('.')
    module, name = library[:dot], library[dot+1:]
    try:
        module = __import__(module, fromlist=[name])
    except ImportError:
        raise err
    try:
        macros = getattr(module, name)
    except AttributeError:
        raise err
    if isinstance(macros, Library):
        return macros
    try:
        module = __import__(library, fromlist=['macros'])
    except ImportError:
        raise err
    try:
        macros = getattr(module, 'macros')
    except AttributeError:
        raise err
    if isinstance(macros, Library):
        return macros
    raise err
