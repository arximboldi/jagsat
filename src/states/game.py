#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

import random
from PySFML import sf

from base.signal import weak_slot
from base.conf   import ConfNode
from base.util   import lazyprop
from core.input  import key
from core.state  import State
from core        import task
from model.world import create_game

from ui.world    import WorldComponent
from ui.player   import PlayerComponent
from ui.attack   import AttackComponent
from ui          import widget
from ui          import theme

from util import QuittableState

from tf.gfx import ui


class GameSubstate (QuittableState):

    @lazyprop
    def game (self):
        result = self.manager.current
        while result and not isinstance (result, GameState):
            result = result.parent_state
        return result


def make_test_game ():
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
    return create_game (cfg)


class GameState (QuittableState):

    def __init__ (self, test_phase = None, *a, **k):
        super (GameState, self).__init__ (*a, **k)
        self.test_phase = test_phase
        
    def do_setup (self, *a, **k):
        super (GameState, self).do_setup (*a, **k)
        self._setup_state ()
        self._setup_ui ()
        self._setup_logic ()
        self.manager.enter_state ('init_game')
        
    def _setup_state (self):
        # TODO: Get world as a parameter
        self.world = make_test_game ()

    def _setup_ui (self):
        system = self.manager.system

        self.map_layer = ui.Layer (system.view)
        self.ui_layer = ui.Layer (system.view)

        self.ui_world  = WorldComponent (self.map_layer, self.world,
                                         self.manager.system.audio)
        self.ui_player = dict ((p, PlayerComponent (self.ui_layer, p))
                               for p in self.world.players.itervalues ())

        self.ui_bg = widget.Background (self.ui_layer)
        self._ui_bg_disabled = []
        
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

    def enable_map (self):
        self._ui_bg_disabled.pop ()
        if not self._ui_bg_disabled:
            self.ui_bg.set_enable_hitting (False)
            return self.tasks.add (self.ui_bg.fade_out ())
        return self.tasks.add (lambda t: None)

    def disable_map (self):
        # self._ui_bg_disabled.append (True)
        if len (self._ui_bg_disabled) == 0:
            self._ui_bg_disabled.append (True)
            self.ui_bg.set_enable_hitting (True)
            return self.tasks.add (self.ui_bg.fade_in ())
        return self.tasks.add (lambda t: None)
    

class GameMessageState (GameSubstate):

    def do_setup (self, message = '', *a, **k):
        super (GameMessageState, self).do_setup (*a, **k)
        
        self.ui_text = ui.MultiLineString (self.game.ui_layer,
                                           unicode (message))
        self.ui_text.set_center_rel (.5, .5)
        self.ui_text.set_position_rel (.5, .5)
        self.ui_text.set_size (50)

        self.game.disable_map ()
        self.tasks.add (task.sequence (
            self.make_fade_task (task.fade),
            task.run (lambda: self.game.ui_bg.on_click.connect (
                self.on_click_bg))))
    
    @weak_slot
    def on_click_bg (self):
        self.game.enable_map ()
        self.tasks.add (task.sequence (
            self.make_fade_task (task.invfade),
            task.run (self.manager.leave_state)))

    def make_fade_task (self, fade_task):
        return fade_task (lambda x:
                          self.ui_text.set_color (sf.Color (255,255,255,x*255)),
                          init = True, duration = .75)
