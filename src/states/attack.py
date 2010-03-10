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
import ui.widget
import ui.theme

_log = get_log (__name__)


class AttackState (GameSubstate):

    def do_setup (self, *a, **k):
        super (AttackState, self).do_setup (*a, **k)
        game = self.game
	
        game.ui_world.enable_used ()
        game.ui_world.enable_picking (
            lambda r:
            r.model.owner == game.world.current_player and
            r.model.has_troops (),
            lambda p, r:
            r.model.owner != game.world.current_player and
            r.model.definition in p.model.definition.neighbours)
        game.ui_world.on_pick_regions += self.on_attack
	game.ui_player[game.world.current_player].on_player_pass += \
            lambda ev: self.on_pass (self)

        self.manager.enter_state ('message', message =
            "You are ready to attack your enemies.")

    def do_release (self):
        self.game.ui_world.disable_used ()
	self.game.ui_world.disable_picking ()
        super (AttackState, self).do_release ()

    @weak_slot
    def on_attack (self, src, dst):
        _log.debug ('Attacking from %s to %s.' %
                    (str (src.model), str (dst.model)))
        self.manager.enter_state ('risk_attack',
                                  attacker = src.model,
                                  defender = dst.model)
 
    def on_pass (self, random):
        self.manager.change_state ('move')
        
