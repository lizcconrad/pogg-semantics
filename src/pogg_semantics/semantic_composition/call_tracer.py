import sys
import inspect
from functools import wraps

class SemCompTracer:
    fxns_called = {}

    @staticmethod
    def trace(f):
        @wraps(f)
        def fxn_tracker(*args, **kwargs):
            if f.__name__ not in SemCompTracer.fxns_called:
                  SemCompTracer.fxns_called[f.__name__] = 1
            else:
                SemCompTracer.fxns_called[f.__name__] += 1
            return f(*args, **kwargs)
        return fxn_tracker

    @staticmethod
    def reset_fxns_called():
        SemCompTracer.fxns_called = {}

class SemAlgTracer:
    fxns_called = {}

    @staticmethod
    def trace(f):
        @wraps(f)
        def fxn_tracker(*args, **kwargs):
            if f.__name__ not in SemAlgTracer.fxns_called:
                SemAlgTracer.fxns_called[f.__name__] = 1
            else:
                SemAlgTracer.fxns_called[f.__name__] += 1
            return f(*args, **kwargs)
        return fxn_tracker

    @staticmethod
    def reset_fxns_called():
        SemAlgTracer.fxns_called = {}
