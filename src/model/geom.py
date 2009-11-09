#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

class Point (object):

    def __init__ (self, x = 0, y = 0, *a, **k):
        super (Point, self).__init__ (*a, **k)
        self.x = x
        self.y = y

class Circle (object):

    def __init__ (self, center = None, radius = 1, *a, **k):
        super (Circle, self).__init__ (*a, **k)
        self.center = Point() if center is None else center
        self.radius = radius

class Polygon (object):

    def __init__ (self, points = None, *a, **k):
        super (Polygon, self).__init__ (*a, **k)
        self.points = points

