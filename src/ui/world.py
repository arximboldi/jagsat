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

from model.world import RegionListener

_log = get_log (__name__)

_REGION_RADIUS     = 17
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

        self.on_click_region = signal.Signal ()
        
        self._world  = world
        self._regions = []
        
        for r in world.regions.itervalues ():
            comp = RegionComponent (self, r)
            pos  = r.definition.shape.center
            comp.set_position (pos.x, pos.y)
            comp.on_click += self.on_click_region
            self._regions.append (comp)

    @property
    def regions (self):
        return self._regions
    
    def toggle_used (self):
        for r in self._regions:
            r.toggle_used ()
    

class RegionComponent (RegionListener, ui.Circle, object):

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
        self.signal_click.add (lambda ev: self.on_click (self))
        self.on_click += lambda _: _log.debug ("Region clicked: " +
                                               self.model.definition.name)
        self.set_enable_hitting (True)
        
        self.model = model
        model.connect (self)

        self._outline_color = sf.Color (0, 0, 0)
        self._fill_color    = _REGION_FREE_COLOR
        self._rebuild_sprite ()

        self._txt_troops = ui.String (self, u"0")
        self._txt_used   = ui.String (self, u"0/0")
        
        self._txt_troops.set_size (25)
        self._txt_troops.set_center_rel (0.5, 0.5)
        self._txt_troops.set_position_rel (0.5, 0.45)
        self._txt_troops.set_color (sf.Color (255, 255, 255))
        self._txt_troops._sprite.SetStyle (sf.String.Bold)
        
        self._txt_used.set_size (20)
        self._txt_used.set_center_rel (0.5, 0.5)
        self._txt_used.set_position_rel (0.5, 0.45)
        self._txt_used.set_color (sf.Color (255, 255, 255))
        self._txt_used.set_visible (False)
        
    def disable_used (self):
        self.set_show_used (False)

    def enable_used (self):
        self.set_show_used (True)
        
    def set_show_used (self, val):
        self._txt_troops.set_visible (not val)
        self._txt_used.set_visible (val)
        
    def on_set_region_troops (self, region, troops):
        self._txt_troops.set_string (unicode (troops))
        self._txt_used.set_string (unicode (troops) + '/' +
                                   unicode (region.used))

    def on_set_region_used (self, region, troops):
        self._txt_used.set_string (unicode (region.troops) + '/' +
                                   unicode (used))

    def on_set_region_owner (self, region, owner):
        self._fill_color = sf.Color (*(
            _REGION_FREE_COLOR if owner is None else owner.color))
        self._rebuild_sprite ()

    def _rebuild_sprite (self):
        self._sprite = sf.Shape.Circle (
            _REGION_RADIUS,
            _REGION_RADIUS,
            _REGION_RADIUS,
            self._fill_color,
            2.0,
            self._outline_color)
    
