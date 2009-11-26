#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from PySFML import sf
from tf.gfx import ui
from base.util import printfn
from base import signal
from base.log import get_log

_log = get_log (__name__)

_REGION_RADIUS     = 10
_REGION_FREE_COLOR = sf.Color (128, 128, 128)

class WorldComponent (ui.Image, object):

    def __init__ (self,
                  parent = None,
                  world  = None,
                  *a, **k):
        assert parent
        assert world
        
        super (WorldComponent, self).__init__ (
            parent = parent,
            fname  = world.map.background,
            *a, **k)
        
        self._world  = world
        self._regions = []
        
        for r in world.iterregions ():
            comp = RegionComponent (self, r)
            pos  = r.definition.shape.center
            comp.set_position (pos.x, pos.y)
            self._regions.append (comp)
            
    def toggle_used (self):
        for r in self._regions:
            r.toggle_used ()
    
        
class RegionComponent (ui.Circle, object):

    def __init__ (self,
                  parent = None,
                  model  = None,
                  *a, **k):
        assert parent
        assert model
        super (RegionComponent, self).__init__ (parent = parent,
                                                radius = _REGION_RADIUS,
                                                *a, **k)

        self.on_click = signal.Signal ()
        self.signal_click.add (self.on_click)
        self.on_click += lambda _: _log.debug ("REGION CLICKED: " +
                                               self._region.definition.name)
        self.set_enable_hitting (True)
        
        self._region = model

        model.on_set_region_owner  += self.on_set_region_owner
        model.on_set_region_troops += self.on_set_region_troops
        model.on_set_region_used   += self.on_set_region_used

        self._outline_color = sf.Color (255, 255, 255)
        self._fill_color    = _REGION_FREE_COLOR
        self._rebuild_sprite ()
        
    def toggle_used (self):
        pass

    def on_set_region_owner (self):
        self._fill_color = sf.Color (*(
            _REGION_FREE_COLOR if self._region.owner is None
            else self._region.owner.color))

    def _rebuild_sprite (self):
        self._sprite = sf.Shape.Circle (
            _REGION_RADIUS,
            _REGION_RADIUS,
            _REGION_RADIUS,
            self._fill_color,
            2.0,
            self._outline_color)

    def on_set_region_troops (self):
        pass

    def on_set_region_used (self):
        pass
    
