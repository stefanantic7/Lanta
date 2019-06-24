"""
Exceptions descriptor.
Define all exception that can be thrown during compilation.
"""
import sys


class NoTraceBackWithLineNumber(Exception):
    def __init__(self, msg):
        self.args = "{0.__name__}: {1}".format(type(self), msg),
        sys.exit(self)


class CompileException(NoTraceBackWithLineNumber):
    pass
