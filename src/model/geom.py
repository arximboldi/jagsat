#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
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
