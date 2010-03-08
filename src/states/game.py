#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

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

        self.ui_attack = AttackComponent (self.ui_layer, self.world)
        
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


class GameMessageState (GameSubstate):

    def do_setup (self, message = '', *a, **k):
        super (GameMessageState, self).do_setup (*a, **k)
        win = self.manager.system.sfml_window
        self.ui_bg = ui.Rectangle (
            self.game.ui_layer, 0, 0, win.GetWidth (), win.GetHeight (),
            sf.Color.Black, sf.Color.Black, 1.)
        self.ui_text = ui.MultiLineString (self.ui_bg, unicode (message))
        self.ui_text.set_center_rel (.5, .5)
        self.ui_text.set_position_rel (.5, .5)
        self.ui_text.set_size (50)

        self.tasks.add (task.sequence (
            self.make_fade_task (task.fade),
            task.run (lambda :
                      self.ui_bg.set_enable_hitting (True) or
                      self.ui_bg.signal_click.add (self.on_click_bg))))
        
    def on_click_bg (self, ev):
        self.tasks.add (task.sequence (
            self.make_fade_task (task.invfade),
            task.run (self.ui_bg.remove_myself),
            task.run (self.manager.leave_state)))

    def make_fade_task (self, fade_task):
        return task.parallel (
            fade_task (lambda x:
                       self.ui_bg.set_color (sf.Color (0, 0, 0, x*210)),
                       init = True, duration = .75),
            fade_task (lambda x:
                           self.ui_text.set_color (
                               sf.Color (255, 255, 255, x*255)),
                       init = True, duration = .75))
