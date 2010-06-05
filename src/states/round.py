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

from base.util import printfn
from base.log import get_log
from game import GameSubstate
from model.world import card

from PySFML import sf
from tf.gfx import ui
from itertools import cycle, islice
from random import randint, choice
from itertools import repeat, chain

_log = get_log (__name__)


class GameRoundState (GameSubstate):

    def do_setup (self, *a, **k):
        super (GameRoundState, self).do_setup (*a, **k)
        game = self.game

        for p in game.ui_player.itervalues ():
            p.but_pass.deactivate ()
            p.but_pass.on_click += lambda ev: self.manager.leave_state ()

        self._setup_actions ()
        if game.world.phase != 'init':
            self._setup_loading ()
        self._action_iter.next () ()

    def _setup_loading (self):
        game = self.game
        while self._player_iter.next () != game.world.current_player:
            pass
        skip = ['init', 'reinforce', 'attack', 'move'].index (game.world.phase)
        for i in xrange (skip):
            self._action_iter.next ()
        game.ui_player [game.world.current_player].but_pass.activate ()
        
    def _setup_actions (self):
        game = self.game
        players = game.world.ordered_players ()        
        self._player_iter = islice (cycle (players),
                                    randint (0, len (players)), None)

        if game.test_phase:
            self._action_iter = iter (
                [ lambda: self._next_turn (),
                  lambda: self.manager.enter_state (game.test_phase),
                  lambda: self.manager.leave_state () ])
        else:
            self._action_iter = cycle (
                [ lambda: self._next_turn (),
                  lambda: self.manager.enter_state ('reinforce'),
                  lambda: self.manager.enter_state ('attack'),
                  lambda: self.manager.enter_state ('move'),
                  lambda: self._finish_turn () ])

    def _next_turn (self):
        game = self.game
        
        old_player = game.world.current_player
        new_player = self._player_iter.next ()
        game.world.current_player = new_player
        game.ui_player [new_player].but_pass.activate ()
        if old_player:
            game.ui_player [old_player].but_pass.deactivate ()
        else:
            game.world.first_player = new_player # Not-so hack
        if new_player == game.world.first_player:
            game.world.round += 1
        
        if not new_player.alive:
            self._next_turn ()
        else:
            new_player.mission.pre_check_mission (game.world)
            self._action_iter.next () ()
    
    def _next_card (self):
        return choice (list (chain (repeat (card.infantry,  25),
                                    repeat (card.cavalry,   11),
                                    repeat (card.artillery, 18),
                                    repeat (card.wildcard,  2))))

    def _finish_turn (self):
        player = self.game.world.current_player

        if player.mission.check_mission (self.game.world):
            self.manager.enter_state (
                'message', message =
                '%%50%%Game Finished.\nPlayer %s won the game!' % player.name,
                position = player.position)
            self.manager.system.audio.play_sound (
                'data/sfx/marchs/winning_player.wav')
            self._action_iter = iter ([ self.manager.leave_state ])
        
        elif player.conquered > 0:
            player.conquered = 0
            if len (player.cards) < 5:
                player.add_card (self._next_card ())
                self.manager.enter_state (
                    'message', message =
                    'Player %s got a new reinforcement card.' % player.name,
                    position = player.position)
            else:
                self.manager.enter_state ('message', message =
                                          'Player %s can not get more cards.' %
                                          player.name,
                                          position = player.position)
        else:
            self._action_iter.next () ()
    
    def do_unsink (self, *a, **k):
        super (GameRoundState, self).do_unsink (*a, **k)
        if not k.get ('must_quit', False):
            self._action_iter.next () ()
