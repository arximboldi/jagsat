#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base.signal import weak_slot
from base.log import get_log
from game import GameSubstate
import random

from PySFML import sf
from tf.gfx import ui
from tf.gfx import threed

import ui.widget
import ui.theme
from ui.attack import AttackComponent

from base import signal

_log = get_log (__name__)


class RiskAttackState (GameSubstate, ui.widget.VBox):

    def do_setup (self, attacker = None, defender = None, *a, **k):
        super (RiskAttackState, self).do_setup (*a, **k)
        game = self.game

        game.disable_map ()
        self.ui_attack = AttackComponent (game.ui_layer, attacker, defender)
                

    def do_release (self):
        self.game.enable_map ()
        super (RiskAttackState, self).do_release ()

