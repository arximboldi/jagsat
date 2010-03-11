#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base.log import get_log
from base import signal

from tf.gfx import ui
from tf.gfx.uiactions import *

import widget
import theme

from PySFML import sf

_log = get_log (__name__)

rotation = [ 180, 135, 45, 0, 315, 225 ]
position = [ (.5, .01), (.95, .05), (.95, .95),
             (0.5, .99), (.05, .95), (.05, .05) ]

def move_to_player_position (comp, player):
    comp.set_center_rel (0.5, 1.0)
    comp.set_position_rel (* position [player.position])
    comp.set_rotation (rotation [player.position])    

class PlayerComponent (widget.VBox, object):

    def __init__ (self, parent = None, player = None, *a, **k):
        super (PlayerComponent, self).__init__ (parent, *a, **k)
        
        self.player = player
        self.menu_enabled = False
        move_to_player_position (self, player)

        self._but_theme = theme.copy_button_theme (theme.small_button)
        pr, pg, pb = player.color
        self._but_theme.active.color  = sf.Color (* player.color)
        self._but_theme.active.border = sf.Color (pr*.5, pg*.5, pb*.5)

        # The main menu
        self._box_main = widget.VBox (self)
        self._but_pass = widget.SmallButton (
            self._box_main, None, 'data/icon/next-small.png')
        self._but_troops = widget.SmallButton (
            self._box_main, None, 'data/icon/troops-small.png')
        self._but_mission = widget.SmallButton (
            self._box_main, None, 'data/icon/world-small.png')
        self._but_undo = widget.SmallButton (
            self._box_main, None, 'data/icon/undo-small.png')

        # The player button
        self._but_main = widget.Button (
            self, None, 'data/icon/small.png', theme = self._but_theme)
        self._but_main.on_click += lambda ev: self.on_toggle_menu (self)

        self._txt_troops = ui.String (self._but_main, u"0")
        self._txt_troops.set_center_rel (0.5, 0.5)
        self._txt_troops.set_position (28, 26)
        self._txt_troops.set_size (20)
        self._txt_troops._sprite.SetStyle (sf.String.Bold)
        player.on_set_player_troops += self.on_set_player_troops
        
        self.padding_bottom = 0
        self._box_main.padding_bottom = 6
        self._box_main.set_visible (self.menu_enabled)

        self._but_troops.deactivate ()
        self._but_mission.deactivate ()
        self._but_undo.deactivate ()
        self._but_pass.deactivate ()

    @property
    def but_pass (self):
        return self._but_pass

    @signal.signal
    def on_toggle_menu (self, _):
        _log.debug ('Toggle menu for player: ' + str (self.player))
        self.menu_enabled = not self.menu_enabled
        self._box_main.set_visible (self.menu_enabled)
    
    @signal.weak_slot
    def on_set_player_troops (self, player, troops):
        if troops > 0:
            self._txt_troops.set_visible (True)
            self._txt_troops.set_string (unicode (troops))
        else:
            self._txt_troops.set_visible (False)

    def enable_undo (self):
        pass # TODO

    def disable_undo (self):
        pass # TODO

