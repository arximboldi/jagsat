#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base.signal import weak_slot
from base.conf   import ConfNode
from base.util   import lazyprop
from core.state  import State
from core.input  import key
from model.world import create_game

from ui.world    import WorldComponent
from ui.player   import PlayerComponent

from quit import QuittableState

from tf.gfx import ui

class GameSubstate (QuittableState):

    @lazyprop
    def game (self):
        result = self.manager.current
        while result and not isinstance (result, GameState):
            result = result.parent_state
        return result


class GameState (QuittableState):

    def do_setup (self, *a, **k):
        super (GameState, self).do_setup (*a, **k)
        self._setup_state ()
        self._setup_ui ()
        self._setup_logic ()
        self.manager.enter_state ('init_game')

    def _setup_state (self):
        # TODO: Get the configuration as a parameter
        cfg = ConfNode (
            { 'player-0' :
              { 'name'     : 'jp',
                'color'    : (255, 0, 0),
                'position' : 3,
                'enabled'  : True },
              'player-2' :
              { 'name'     : 'pj',
                'color'    : (0, 255, 0),
                'position' : 4,
                'enabled'  : True },
              'map' : 'doc/map/worldmap.xml' })

        self.world = create_game (cfg)

    def _setup_ui (self):
        system = self.manager.system

        self.map_layer = ui.Layer (system.view)
        self.ui_layer = ui.Layer (system.view)

        
        self.ui_world  = WorldComponent (self.map_layer, self.world)
        self.ui_player = dict ((p, PlayerComponent (self.ui_layer, p))
                               for p in self.world.players.itervalues ())
        
    def _setup_logic (self):
        system = self.manager.system
        
        system.keys.get_key (key.escape).connect (self.toggle_menu)

    @weak_slot
    def toggle_menu (self, k, m):
        current = self.manager.current
        if current.state_name == 'ingame_menu':
            self.manager.leave_state ()
        else:
            self.manager.enter_state ('ingame_menu')
