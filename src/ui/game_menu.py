#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base import signal
from widget import VBox, SmallButton, SelectButton, Frame
from model.world import WorldListener

from tf.gfx import ui

class GameHudComponent (WorldListener, Frame):

    def __init__ (self, world = None, *a, **k):
        super (GameHudComponent, self).__init__ (*a, **k)
        
        self.set_margin (7)
        self.margin_top= 48
        self.text = ui.MultiLineString (
            self, [u"Player: ", u"Round: "])
        self.text.set_size (18)
        self.text.set_position (14, 7)
        self.set_enable_hitting (False)
        self.deactivate ()
        self.set_rotation (-90)
        self.set_center_rel (.5, 0.)
        self.set_position (54., 768./2) # hack
        self._do_update (world)
        world.connect (self)
        
    def on_set_world_round (self, world, round):
        self._do_update (world)

    def on_set_world_current_player (self, world, player):
        self._do_update (world)

    def _do_update (self, world):
        self.text.set_strings ([
            u"Player: %s" % (world.current_player and
                             world.current_player.name) or "<None>",
            u"Round: %i"  % world.round ])

class GameMenuComponent (VBox, object):

    def __init__ (self, parent = None, *a, **k):
        super (GameMenuComponent, self).__init__ (parent, *a, **k)

        self.but_menu = SmallButton (self, None, 'data/icon/home-small.png')
        self.but_move = SelectButton (self, None, 'data/icon/move-small.png')
        self.but_zoom = SelectButton (self, None, 'data/icon/zoom-small.png')
        self.but_rot  = SelectButton (self, None, 'data/icon/rotate-small.png')
        self.but_restore = SmallButton (self, None, 'data/icon/undo-small.png')
        
        self.but_menu.margin_right = 52
        self.but_move.margin_right = 52
        self.but_zoom.margin_right = 52
        self.but_rot.margin_right  = 52
        self.but_restore.margin_right  = 52

        self.padding_bottom = 10
        
        self.set_center_rel (.5, .5)
        self.set_position_rel (1., .5)

        self.map_ops = [self.but_move, self.but_zoom, self.but_rot]
        for op in self.map_ops:
            op.on_select += self._unselect_ops
    
    @signal.weak_slot
    def _unselect_ops (self):
        for x in self.map_ops:
            x.unselect ()

