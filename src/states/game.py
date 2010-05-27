#
#  Copyright (C) 2009, 2010 JAGSAT Development Team (see below)
#  
#  This file is part of TF.
#  
#  TF is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  
#  TF is distributed in the hope that it will be useful,
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

from PySFML import sf

from base.log      import get_log
from base.error    import LoggableError
from base.signal   import weak_slot
from base.conf     import ConfNode
from base.util     import lazyprop
from core.state    import State
from core.input    import key
from core          import task
from model.world   import create_game, cardset_value
from model.worldio import load_game
from ui.world      import WorldComponent, map_op
from ui.player     import PlayerComponent
from ui.game_menu  import GameMenuComponent, GameHudComponent
from ui            import widget
from ui            import theme

from root import RootSubstate
from util import QuittableState

from tf.gfx import ui
from functools import partial

_log = get_log (__name__)

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
      'map' : 'data/map/world_map.xml' })


class GameState (RootSubstate):

    def __init__ (self, test_phase = None, *a, **k):
        super (GameState, self).__init__ (*a, **k)
        self.test_phase = test_phase
        
    def do_setup (self,
                  profile = None,
                  load_game = None,
                  *a, **k):
        super (GameState, self).do_setup (*a, **k)

        self._profile   = profile
        self._load_game = load_game
        
        self._setup_state ()
        if self.world:
            self._setup_ui ()
            self._setup_logic ()
            self._enter_game ()

    def do_unsink (self, *a, **k):
        if self.parent_state: # We are not running in test mode, go to menu
            self.manager.change_state ('main_menu')

    def do_release (self):
        for x in self.ui_player.itervalues ():
            x.remove_myself ()
        self.ui_world.remove_myself ()
        self.ui_menu.remove_myself ()
        self.ui_hud.remove_myself ()

    def _enter_game (self):
        if self.world.phase == 'init':
            self.manager.enter_state ('init_game')
        else:
            self.manager.enter_state ('game_round')
    
    def _setup_state (self):
        if self._load_game is None:
            _log.debug ('Starting new game.')
            self.world = create_game (self._profile or test_profile)
        else:
            _log.debug ('Loading game: ' + self._load_game)
            try:
                self.world = load_game (self._load_game)
            except LoggableError, e:
                e.log ()
                self.manager.change_state ('message', message =
                                           'Error while loading game :(')
    
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

