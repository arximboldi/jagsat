#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base.log import get_log
from game import GameSubstate

from PySFML import sf
from tf.gfx import ui
from itertools import cycle

_log = get_log (__name__)


class GameRoundState (GameSubstate):

    def do_setup (self, *a, **k):
        super (GameRoundState, self).do_setup (*a, **k)
        world = self.game.world

	world.current_player = None
        self._player_iter = cycle (world.ordered_players ())
	self._next_turn ()

    def _next_turn (self):
        self.game.world.current_player = self._player_iter.next ()
        self.manager.enter_state (self.game.test_phase or 'reinforcements')

    def do_unsink (self, *a, **k):
        super (GameRoundState, self).do_unsink (*a, **k)
        self._next_turn ()
