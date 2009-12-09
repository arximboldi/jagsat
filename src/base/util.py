#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#


_multimethod_registry = {}


class MultiMethod (object):

    def __init__ (self, name):
        self.name = name
        self.typemap = {}

    def __call__ (self, *args):
        types = tuple (arg.__class__ for arg in args)
        function = self.typemap.get (types)
        if function is None:
            raise TypeError ("no match")
        return function(*args)

    def register(self, types, function):
        if types in self.typemap:
            raise TypeError ("duplicate registration")
        self.typemap[types] = function


def multimethod (*types):
    """
    http://www.artima.com/weblogs/viewpost.jsp?thread=101605
    """
    
    def register (function):
        function = getattr (function, "__lastreg__", function)
        name = function.__name__
        mm = _multimethod_registry.get (name)
        if mm is None:
            mm = _multimethod_registry[name] = MultiMethod (name)
        mm.register (types, function)
        mm.__lastreg__ = function
        return mm
    return register

class memoize:
    """
    http://avinashv.net/2008/04/python-decorators-syntactic-sugar/
    """

    def __init__(self, function):
        self.function = function
        self.memoized = {}

    def __call__(self, *args):
        try:
            ret = self.memoized[args]
        except KeyError:
            ret = self.memoized[args] = self.function(*args)
        return ret


def printfn (message):
    print message


def remove_if (predicate, lst):
    return [elem for elem in lst if not predicate (elem)]


def flip_dict (dct):
    new_dct = {}
    for k, v in dct.items ():
        new_dct [v] = k
    return new_dct


def read_file (fname):
    fh = open (fname, 'r')
    content = fh.read ()
    fh.close ()
    return content
