#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from util import memoize


@memoize
def mixin (one, two):
    class Mixin (one, two):
        def __init__ (self, *args, **kws):
            super (Mixin, self).__init__ (*args, **kws)

    return Mixin


def monkeypatch (target, name = None):
    def patcher (func):
        patchname = func.__name__ if name is None else name
        setattr (target, patchname, func)
        return func
    return patcher


def monkeypatch_extend (target, name = None):
    def patcher (func):
        newfunc = func
        patchname = func.__name__ if name is None else name
        if hasattr (target, patchname):
            oldfunc = getattr (target, patchname)
            if not callable (oldfunc):
                raise AttributeError ('Can not extend non callable attribute')
            def extended (*a, **k):
                ret = oldfunc (*a, **k)
                func (*a, **k)
                return ret
            newfunc = extended
        setattr (target, patchname, newfunc)
        return func
    return patcher


def instance_decorator (decorator):
    class Decorator (object):
        def __init__ (self, func, *args, **kws):
            self.__name__ = func.__name__
            self.__doc__ = func.__doc__
            self._func = func
            self._args = args
            self._kws = kws
            
        def __get__ (self, obj, cls = None):
            if obj is None:
                return None
            decorated = decorator (obj, self._func, *self._args, **self._kws)
            obj.__dict__[self.__name__] = decorated
            return decorated

    return Decorator


def extend_methods (cls, **kws):
    for name, new_method in kws.items ():
        if hasattr (cls, name):
            old_method = getattr (cls, name)
            if not callable (old_method):
                raise AttributeError ("Can not extend a non callable attribute")
            def extended (*args, **kw):
                new_method (*args, **kw)
                return old_method (*args, **kw)
            method = extended
        else:
            method = new_method
        setattr (cls, name, method)
    
    return cls 
