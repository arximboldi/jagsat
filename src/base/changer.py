#
#  Copyright (C) 2009, 2010 JAGSAT Development Team (see below)
#  
#  This file is part of TF.
#  
#  TF is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  
#  TF is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  
#  JAGSAT Development Team is:
#    - Juan Pedro Bolivar Puente
#    - Alberto Villegas Erce
#    - Guillem Medina
#    - Sarah Lindstrom
#    - Aksel Junkkila
#    - Thomas Forss
#
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

class Changer (object):
    """
    Data descriptor that allows you to have a value that executes a
    function or function-like object (i.e. a signal) whenever it is
    modified. The function object will be called with two parameters,
    the first one being the object whose this descriptor belongs to,
    and then the new value that is asigned to it.
    """
    
    def __init__ (self,
                  func = None,
                  name = None,
                  value = None,
                  *a, **k):
        """
        Constructor.

        Parameters:
          - signal: The function object.
          - value:  Initial value, None by default.
        """
        assert func
        super (Changer, self).__init__ (*a, **k)
        
        self._signal  = func
        self._name    = '__Changer_' + (name or str (id (self)))
        self._default = value

    def __get__ (self, obj, cls):
        return getattr (obj, self._name, self._default)

    def __set__ (self, obj, value):
        setattr (obj, self._name, value)
        self._signal (obj, value)


class InstChanger (Changer):

    def __init__ (self,
                  func_name = None,
                  name = None,
                  value = None,
                  *a, **k):
        super (InstChanger, self).__init__ (
            func  = lambda obj, val: getattr (obj, func_name) (obj, val),
            name  = name,
            value = value,
            *a, **k)
