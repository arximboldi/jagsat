#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base import signal
from widget import HBox, VBox, SmallButton, SelectButton, Frame
from model.world import WorldListener

from tf.gfx import ui

def game_hud_text (parent, string):
    frame = Frame (parent)
    frame.set_margin (7)
    frame.margin_top = 48
    text = ui.String (frame, unicode (string))
    text.set_size (18)
    text.set_position (14, 7)
    return text

class GameHudComponent (WorldListener, HBox):

    def __init__ (self, world = None, *a, **k):
        super (GameHudComponent, self).__init__ (*a, **k)
        
        self.separation = 10
        
        self.text_player = game_hud_text (self, "Player: ")
        self.text_round  = game_hud_text (self, "Round: ")
        self.text_phase  = game_hud_text (self, "Phase: ")

        self.set_rotation (-90)
        self.set_center_rel (.5, 0.)
        self.set_position (36, 768./2) # hack
        self._do_update (world)
        world.connect (self)
        
    def on_set_world_round (self, world, round):
        self.text_round.set_string (u"Round: %i" % round)

    def on_set_world_current_player (self, world, player):
        self.text_player.set_string (u"Player: %s" %
                                     (player and player.name) or "None")

    def on_set_world_phase (self, world, phase):
        self.text_phase.set_string (u"Phase: %s" % phase)

    def _do_update (self, world):
        self.text_player.set_string (
            u"Player: %s" % (world.current_player and
                             world.current_player.name) or "None")
        self.text_round.set_string (u"Round: %i" % world.round)
        self.text_phase.set_string (u"Phase: %s" % world.phase)


class GameMenuComponent (VBox, object):

    def __init__ (self, parent = None, *a, **k):
        super (GameMenuComponent, self).__init__ (parent, *a, **k)

        self.but_menu = SmallButton (self, image='data/icon/home-small.png')
        self.but_move = SelectButton (self, image='data/icon/move-small.png')
        self.but_zoom = SelectButton (self, image='data/icon/zoom-small.png')
        self.but_rot  = SelectButton (self, image='data/icon/rotate-small.png')
        self.but_restore = SmallButton (self, image='data/icon/undo-small.png')
        
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
    def _unselect_ops (self, but):
        for x in self.map_ops:
            if x != but:
                x.unselect ()

