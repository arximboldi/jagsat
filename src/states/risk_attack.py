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
from base import signal

_log = get_log (__name__)


class RiskAttackState (GameSubstate):

    def do_setup (self, *a, **k):
        super (RiskAttackState, self).do_setup (*a, **k)
        game = self.game
	self.dst = game.ui_attack.dst
	self.src = game.ui_attack.src

	game.ui_attack.on_retreat += lambda ev: self.on_retreat (self)
	self.risk_attack(self.src, self.dst)


    def do_release (self):
        self.game.ui_world.disable_used ()
	self.game.ui_world.disable_picking ()
        super (RiskAttackState, self).do_release ()
        
    @weak_slot
    def on_attack (self, src, dst):
        _log.debug ('Attacking from %s to %s.' %
                    (str (src.model), str (dst.model)))
	self.game.ui_attack.dice_enable()
	#self.risk_attack (src, dst)
    

    def risk_attack (self, src, dst):
	
	"""
	When pressing a highlighted country for attack the attack menu will be enabled.
	"""	
	self.game.ui_attack.dice_enable()


    def on_retreat(self, random):
	self.game.ui_attack.dice_disable()
        self.manager.leave_state ()	# Exit risk_attack state

    def on_troops_increase(self):
	pass

    def on_troops_decrease(self):
	pass
