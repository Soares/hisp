from StringIO import StringIO


class MacroNotFound(Exception):
    pass


class HispError(Exception):
    def __init__(self, message, original=None, context=None):
        self.contexts = [context]
        self.original = original
        super(HispError, self).__init__(message)

    def indent(string, tab='\t'):
        return '\n'.join(tab + line for line in string.split('\n'))

    def __str__(self):
        f = StringIO()
        print >> f, ''
        if self.original:
            print >> f, self.original
        else:
            print >> f, ''
        for item in reversed(self.contexts):
            print >> f, 'In %s' % repr(item)
        for arg in self.args:
            print >> f, self.indent(arg).rstrip()
        print >> f, super(HispError, self).__str__()
        return f.getvalue()


def reraise(context):
    """
    Raise an exception as a HispError, saving the original
    traceback, adding new context information
    """
    import traceback
    import sys
    f = StringIO()
    etype, evalue, tb = sys.exc_info()
    if etype == HispError:
        evalue.contexts.append(context)
        raise
    e = traceback.format_exception_only(etype, evalue)[-1]
    t = ''.join(traceback.format_tb(tb))
    raise HispError(e, t, context)
