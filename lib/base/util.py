#
#  Copyright (C) 2009 Juan Pedro Bolivar Puente, Alberto Villegas Erce
#  
#  This file is part of Pidgeoncide.
#
#  Pidgeoncide is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  
#  Pidgeoncide is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
