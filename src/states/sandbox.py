#
#  Copyright (C) 2009, 2010 JAGSAT Development Team (see below)
#  
#  This file is part of JAGSAT.
#  
#  JAGSAT is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  
#  JAGSAT is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  
#  JAGSAT Development Team is:
#    - Juan Pedro Bolivar Puente
#    - Alberto Villegas Erce
#    - Guillem Medina
#    - Sarah Lindstrom
#    - Aksel Junkkila
#    - Thomas Forss
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
