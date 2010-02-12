#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from tf.gfx import ui
from tf.gfx.widget import intermediate as ui2

from base.conf   import ConfNode
from core.state  import State
from core.input  import key
from model.world import create_game
from ui.world    import WorldComponent

from PySFML import sf


THEME = { 'active'    : sf.Color.Blue,
          'inactive'  : sf.Color.Red, 
          'border'    : sf.Color.Green,
          'thickness' : 2 }

class Sandbox (State):
    
    def do_setup (self, *a, **k):
        system = self.manager.system
        
        layer = ui.Layer (system.view)
        system.keys.get_key (key.escape).connect (self.manager.leave_state)
        
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
        but = ui2.Button (layer,
                          ui.String (layer, unicode ('Testttt')),
                          THEME)
        but.activate ()
