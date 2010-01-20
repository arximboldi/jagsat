#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evaluators in Abo Akademy is
#  completely forbidden without explicit permission of their authors.
#


from state import State
from tf.gfx import ui
from ui.menu import MenuComponent

class Main_menu (State):
    
    def do_enter (self, *a, **k):
        sfview = self.system._window.window.GetDefaultView ()
        view  = ui.View (self.system._window, sfview)
        layer = ui.Layer (view)
    
        menu_comp = MenuComponent(layer)
        
        