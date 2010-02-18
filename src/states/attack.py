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

from PySFML import sf
from tf.gfx import ui

_log = get_log (__name__)


class AttackState (GameSubstate):

    def do_setup (self, *a, **k):
        super (AttackState, self).do_setup (*a, **k)
        game = self.game

        game.ui_world.enable_picking (
            lambda r:
            r.model.owner == game.world.current_player and
            r.model.troops - r.model.used > 1,
            lambda p, r:
            r.model.owner != game.world.current_player and
            r.model.definition in p.model.definition.neighbours)
        game.ui_world.on_pick_regions += self.on_attack
        
    @weak_slot
    def on_attack (self, src, dst):
        _log.debug ('Attacking from %s to %s.' % (str (src.model), str (dst.model)))
