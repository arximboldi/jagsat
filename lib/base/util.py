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


def printf (message):
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
