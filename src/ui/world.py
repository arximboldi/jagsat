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
from functools import partial

from base.util import printfn
from base import signal
from base.log import get_log

from model.world import RegionListener
import theme

_log = get_log (__name__)

region_radius     = 17
region_free_color = sf.Color (128, 128, 128)

class map_op:
    none, move, rotate, zoom = range (4)

class WorldComponent (ui.Image, object):

    def __init__ (self,
                  parent = None,
                  world  = None,
                  audio  = None, 
                  *a, **k):
        assert parent
        assert world
        
        super (WorldComponent, self).__init__ (
            parent = parent,
            fname  = world.map.background,
            *a, **k)

        self.operation = map_op.none
        self.audio = audio
        self.allow_repick = True
        self.on_click_region = signal.Signal ()
        self.on_pick_regions = signal.Signal ()
        
        self.picked = None
        self.new_picked = None # A bit hackish just to let the
                               # on_pick_regions callback choose a new
                               # pick
        
        self._pick_cond_fst = None
        self._pick_cond_snd = None
        self.click_cond = lambda r: True
        self.set_enable_hitting(True)
        self.model  = world
        self._regions = []
        
        for r in world.regions.itervalues ():
            comp = RegionComponent (self, r)
            pos  = r.definition.shape.center
            comp.set_position (pos.x, pos.y)
            comp.on_click += self._on_click_region
            self._regions.append (comp)

        self._last_move_pos = None
        
    def start_pan (self, ev):
        _log.debug ('Start panning: ' + str (ev))
        if self.operation == map_op.move:
            self._last_move_pos = ev
            
    def end_pan (self, ev):
        _log.debug ('End panning: ' + str (ev))
        
    def do_pan (self, (nx, ny)):
        _log.debug ('Do panning: ' + str ((nx, ny)))
        if self.operation == map_op.move:
            ox, oy = self._last_move_pos
            dx, dy = nx - ox, ny - oy
            self.set_position_delta (dx, dy)
            self._last_move_pos = nx, ny
            
    @signal.weak_slot
    def _on_click_region (self, r):
        if self._pick_cond_fst:
            self.on_click_region (r)
            self._on_pick_one_region (r)
        elif not self.click_cond or self.click_cond (r):
            self.audio.play_sound (theme.ok_click)
            self.on_click_region (r)
        else:
            self.audio.play_sound (theme.bad_click)

    def enable_picking (self,
                        cond_fst = lambda *a, **k: True,
                        cond_snd = lambda *a, **k: True):
        if self._pick_cond_fst is None:
            self._pick_cond_fst = cond_fst
            self._pick_cond_snd = cond_snd
            
    def disable_picking (self):
        if self._pick_cond_fst is not None:
            self._pick_cond_fst = None
            self._pick_cond_snd = None

    @signal.weak_slot
    def _on_pick_one_region (self, region):
        _log.debug ("Trying to pick region: " + str (region.model))
        if not self.picked:
            if self._pick_cond_fst (region):
                self._pick_region (region)
            else:
                self.audio.play_sound (theme.bad_click)
        elif self.picked != region:
            if self._pick_cond_snd (self.picked, region):
                self.new_pick = None
                self.on_pick_regions (self.picked, region)
                self._pick_region (self.new_pick)
            elif self.allow_repick and self._pick_cond_fst (region):
                self._pick_region (region)
            else:
                self.audio.play_sound (theme.bad_click)
                
    def _pick_region (self, region):
        self.audio.play_sound (theme.ok_click)
        if self.picked:
            self.picked.unhighlight ()
            for r in filter (partial (self._pick_cond_snd, self.picked),
                             self._regions):
                r.unhighlight ()
        self.picked = region
        if region:
            region.select ()
            for r in filter (partial (self._pick_cond_snd, self.picked),
                             self._regions):
                r.highlight ()
    
    @property
    def regions (self):
        return self._regions

    def enable_used (self):
        for r in self._regions:
            if r.model.owner == self.model.current_player:
                r.enable_used ()
            else:
                r.disable_used ()

    def disable_used (self):
        for r in self._regions:
            r.disable_used ()


class RegionComponent (RegionListener, ui.Circle, object):

    def __init__ (self,
                  parent = None,
                  model  = None,
                  *a, **k):
        assert parent
        assert model
        super (RegionComponent, self).__init__ (parent = parent,
                                                radius = region_radius,
                                                *a, **k)

        self.on_click = signal.Signal ()
        self.signal_click.add (lambda ev: self.on_click (self))
        self.on_click += lambda ev: _log.debug ("Region clicked: " +
                                                self.model.definition.name)
        self.set_enable_hitting (True)
        
        self.model = model
        model.connect (self)

        self._outline_width = 2.0
        self._outline_color = sf.Color (0, 0, 0)
        self._fill_color    = region_free_color
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

    def highlight (self):
        self._outline_color = sf.Color (255, 255, 128)
        self._outline_width = 4.0
        self._rebuild_sprite ()
        
    def select (self):
        self._outline_color = sf.Color (255, 255, 255)
        self._outline_width = 4.0
        self._rebuild_sprite ()
        
    def unhighlight (self):
        self._outline_color = sf.Color (0, 0, 0)
        self._outline_width = 2.0
        self._rebuild_sprite ()
        
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

    def on_set_region_used (self, region, used):
        self._txt_used.set_string (unicode (region.troops) + '/' +
                                   unicode (used))

    def on_set_region_owner (self, region, owner):
        self._fill_color = (owner and owner.color) or region_free_color
        self._rebuild_sprite ()

    def _rebuild_sprite (self):
        self._sprite = sf.Shape.Circle (
            region_radius,
            region_radius,
            region_radius,
            self._fill_color,
            self._outline_width,
            self._outline_color)
    
