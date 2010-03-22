#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
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
            # This would break if the players could pass in a state that is not
            # just above this one in the stack.
            
	game.world.current_player = None
        
        players = game.world.ordered_players ()        
        player_iter = islice (cycle (players), randint (0, len (players)), None)

        if game.test_phase:
            self._action_iter = iter (
                [ lambda: self._next_turn (player_iter),
                  lambda: self.manager.enter_state (game.test_phase),
                  lambda: self.manager.leave_state () ])
        else:
            self._action_iter = cycle (
                [ lambda: self._next_turn (player_iter),
                  lambda: self.manager.enter_state ('reinforce'),
                  lambda: self.manager.enter_state ('attack'),
                  lambda: self.manager.enter_state ('move'),
                  lambda: self._finish_turn () ])
        self._action_iter.next () ()

    def _next_turn (self, player_iter):
        game = self.game

        old_player = game.world.current_player
        new_player = player_iter.next ()

        game.world.current_player = new_player
        
        game.ui_player [new_player].but_pass.activate ()
        if old_player:
            game.ui_player [old_player].but_pass.deactivate ()
        else:
            self._first_player = new_player # Hack

        if new_player == self._first_player:
            game.world.round += 1
        
        self._action_iter.next () ()

    def _next_card (self):
        return choice (list (chain (repeat (card.infantry,  25),
                                    repeat (card.cavalry,   11),
                                    repeat (card.artillery, 18),
                                    repeat (card.wildcard,  2))))

    def _finish_turn (self):
        player = self.game.world.current_player
        if player.conquered > 0:
            player.conquered = 0
            if len (player.cards) < 5:
                player.add_card (self._next_card ())
                self.manager.enter_state (
                    'message', message =
                    'Player %s got a new reinforcement card.' % player.name)
            else:
                self.manager.enter_state ('message', message =
                                          'Player %s can not get more cards.' %
                                          player.name)
        else:
            self._action_iter.next () ()
    
    def do_unsink (self, *a, **k):
        super (GameRoundState, self).do_unsink (*a, **k)
        if not k.get ('must_quit', False):
            self._action_iter.next () ()
