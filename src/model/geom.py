#
#  Copyright (C) 2009, 2010 JAGSAT Development Team (see below)
#  
#  This file is part of JAGSAT.
#  
#  JAGSAT is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  
#  JAGSAT is distributed in the hope that it will be useful,
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

from base.util import multimethod
from exceptions import NotImplementedError

class Point (object):

    def __init__ (self, x = 0, y = 0, *a, **k):
        super (Point, self).__init__ (*a, **k)
        self.x = x
        self.y = y

    def sqr_distance (self, b):
        return (self.x-b.x)**2 + (self.y-b.y)**2

    @property
    def center (self):
        return self


class Circle (object):

    def __init__ (self, center = None, radius = 1, *a, **k):
        super (Circle, self).__init__ (*a, **k)
        self.center = Point() if center is None else center
        self.radius = radius


class Polygon (object):

    def __init__ (self, points = None, *a, **k):
        super (Polygon, self).__init__ (*a, **k)
        self.points = points

    @property
    def center (self):
        raise NotImplementedError

    
class Line (object):

    def __init__ (self, pa = None, pb = None, *a, **k):
        super (Line, self).__init__ (*a, **k)
        self.pa = Point () if pa is None else pa
        self.pb = Point () if pb is None else pb

    @property
    def center (self):
        raise NotImplementedError
    

@multimethod (Point, Circle)
def intersects (a, b):
    return a.sqr_distance (b.center) < b.radius**2

@multimethod (Circle, Point)
def intersects (a, b):
    return intersects (b, a)
