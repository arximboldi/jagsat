#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evaluators in Abo Akademy is
#  completely forbidden without explicit permission of their authors.
#

from base import signal

from root import RootSubstate
from tf.gfx import ui
from ui.menu import *

class MainMenuState (RootSubstate):
    
    def do_setup (self, *a, **k):
	
	system = self.manager.system 
        self.ui_layer = ui.Layer (system.view)
        self.ui_layer.zorder = -1
        self._menu = MainMenu (self.ui_layer)
        
        self._menu.actions.quit.on_click += self.manager.leave_state
        self._menu.actions.play.on_click += self._on_click_play
        
    @signal.weak_slot
    def _on_click_play (self, ev = None):
        self.manager.change_state ('game', profile = self._menu.options.config)
        
    def do_release (self):
        self._menu.remove_myself ()
