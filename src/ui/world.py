#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from tf.gfx import ui

class WorldComponent (ui.Component, object):

    def __init__ (self, layer, *a, **k):
        super (WorldComponent, self).__init__ (layer, *a, **k)
        self._sprite = None
        ui.String (self, u"Hello World")
        
class RegionComponent (ui.Component, object):

    def __init__ (self, *a, **k):
        super (RegionComponent, self).__init__ (*a, **k)
