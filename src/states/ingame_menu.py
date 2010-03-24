#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base.log import get_log

from ui.ingame_menu import IngameMenu
from game import GameSubstate

_log = get_log (__name__)


class IngameMenuState (GameSubstate):

    def do_release (self):
        super (IngameMenuState, self).do_release ()
        self._ingame_menu.remove_myself ()
        self.root.disable_bg ()
    
    def do_setup (self, *a, **k):
        super (IngameMenuState, self).do_setup (*a, **k)
        self._ingame_menu = IngameMenu (self.root.ui_layer)

        self._ingame_menu.on_quit_game  += self.quit_state
        self._ingame_menu.on_close_menu += self.manager.leave_state
        
        self.root.enable_bg ()

