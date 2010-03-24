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
from core.state  import State
from core.input  import key
from core        import task
from model.world import create_game, cardset_value

from ui.world     import WorldComponent, map_op
from ui.player    import PlayerComponent
from ui.game_menu import GameMenuComponent, GameHudComponent
from ui           import widget
from ui           import theme

from util import QuittableState

from tf.gfx import ui
from functools import partial

class GameSubstate (QuittableState):

    @lazyprop
    def game (self):
        result = self.manager.current
        while result and not isinstance (result, GameState):
            result = result.parent_state
        return result


test_profile = ConfNode (
    { 'player-0' :
      { 'name'     : 'jp',
        'color'    : sf.Color (255, 0, 0),
        'position' : 3,
        'enabled'  : True },
      'player-2' :
      { 'name'     : 'pj',
        'color'    : sf.Color (0, 255, 0),
        'position' : 4,
        'enabled'  : True },
      'player-3' :
      { 'name'     : 'pjj',
        'color'    : sf.Color (0, 0, 255),
        'position' : 5,
        'enabled'  : True },
      'map' : 'doc/map/worldmap.xml' })

class GameState (State):

    def __init__ (self, test_phase = None, *a, **k):
        super (GameState, self).__init__ (*a, **k)
        self.test_phase = test_phase
        
    def do_setup (self, profile = None, *a, **k):
        super (GameState, self).do_setup (*a, **k)
        self._setup_state (profile)
        self._setup_ui ()
        self._setup_logic ()
        self.manager.enter_state ('init_game')

    def do_release (self):
        for x in self.ui_player.itervalues ():
            x.remove_myself ()
        self.ui_world.remove_myself ()
        self.ui_bg.remove_myself ()
        self.ui_menu.remove_myself ()
        
    def do_unsink (self, *a, **k):
        if self.parent_state: # We are not running in test mode, go to menu
            self.manager.change_state ('main_menu')
        else:
            self.manager.leave_state ()
    
    def _setup_state (self, profile):
        self.world = create_game (profile or test_profile)

    def _setup_ui (self):
        system = self.manager.system

        self.map_layer = ui.Layer (system.view)
        self.ui_layer = ui.Layer (system.view)

        self.ui_world  = WorldComponent (self.map_layer, self.world,
                                         self.manager.system.audio)
        self.ui_player = dict ((p, PlayerComponent (self.ui_layer, p))
                               for p in self.world.players.itervalues ())
        for p in self.ui_player.itervalues ():
            p.on_exchange_cards += partial (self.exchange_cards, p.player)
            p.on_drop_cards     += partial (self.drop_cards, p.player)
        self.ui_menu   = GameMenuComponent (self.ui_layer)
        self.ui_hud    = GameHudComponent (parent = self.ui_layer,
                                           world = self.world)
        
        self.ui_bg = widget.Background (self.ui_layer)
        self._ui_bg_disabled = []

    def exchange_cards (self, player, cards):
        value = cardset_value (cards)
        if value > 0:
            player.troops += value
            map (player.del_card, cards)
            self.manager.system.audio.play_sound (
                'data/sfx/drums/drum_march_short.wav')
        else:
            self.manager.system.audio.play_sound (theme.bad_click)
    
    def drop_cards (self, player, cards):
        map (player.del_card, cards)
        if cards:
            self.manager.system.audio.play_sound (theme.ok_click)
        else:
            self.manager.system.audio.play_sound (theme.bad_click)
    
    def _setup_logic (self):
        # system = self.manager.system
        # system.keys.get_key (key.escape).connect (self.toggle_menu)
        self.ui_menu.but_menu.on_click += self.enter_menu
        for op in self.ui_menu.map_ops:
            op.on_unselect += self.stop_map_operation
        self.ui_menu.but_move.on_select   += self.start_map_move
        self.ui_menu.but_zoom.on_select   += self.start_map_zoom
        self.ui_menu.but_rot.on_select    += self.start_map_rot
        self.ui_menu.but_restore.on_click += self.restore_map

    @weak_slot
    def restore_map (self, ev = None):
        self.tasks.add (self.ui_world.restore_transforms ())
        
    @weak_slot
    def stop_map_operation (self, but = None):
        self.ui_world.operation = map_op.none

    @weak_slot
    def start_map_move (self, but = None):
        self.ui_world.operation = map_op.move

    @weak_slot
    def start_map_zoom (self, but = None):
        self.ui_world.operation = map_op.zoom

    @weak_slot
    def start_map_rot (self, but = None):
        self.ui_world.operation = map_op.rotate

    @weak_slot
    def enter_menu (self, ev):
        self.manager.enter_state ('ingame_menu')
    
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
