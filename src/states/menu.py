#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evaluators in Abo Akademy is
#  completely forbidden without explicit permission of their authors.
#

from core.state import State
from tf.gfx import ui
from ui.menu import MenuComponent

class MainMenuState (State):
    
    def do_setup (self, *a, **k):
	
	system = self.manager.system 
        layer = ui.Layer (system.view)
        menu_comp = MenuComponent(layer)
	menu_comp.on_start_game += lambda p: self.manager.change_state ('game', profile = p)
	menu_comp.on_quit_program += self.manager.leave_state
        self.menu_comp = menu_comp
        
    def do_release (self):
        self.menu_comp.remove_myself ()
