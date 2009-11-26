#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from state import State
import model.world
from tf.gfx import ui
from model.world import create_game
from base.conf import ConfNode
from ui.world import WorldComponent

class Sandbox (State):
    
    def do_enter (self, *a, **k):
        sfview = self.system._window.window.GetDefaultView ()
        view  = ui.View (self.system._window, sfview)
        layer = ui.Layer (view)
        
        cfg = ConfNode (
            { 'player-0' :
              { 'name'     : 'jp',
                'color'    : 1,
                'position' : 2,
                'enabled'  : True },
              'player-2' :
              { 'name'     : 'pj',
                'color'    : 3,
                'position' : 4,
                'enabled'  : True },
              'map' : 'doc/map/worldmap.xml' })

        world = create_game (cfg)
        comp = WorldComponent (layer, world)

