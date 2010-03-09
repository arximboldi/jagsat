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


class RiskAttackState (GameSubstate, ui.widget.VBox):

    def do_setup (self, *a, **k):
        super (RiskAttackState, self).do_setup (*a, **k)
        game = self.game
	self.dst = game.ui_attack.dst
	self.src = game.ui_attack.src
	self.attacker_number_of_dices = self.game.ui_attack.attacker_number_of_dices
	self.defender_number_of_dices = self.game.ui_attack.defender_number_of_dices
	self.used_attacker_number = self.game.ui_attack.used_attacker_number
	self.defender_dice_list = self.game.ui_attack.defender_dice_list
	self.attacker_dice_list = self.game.ui_attack.attacker_dice_list
	self.dice_enabled = self.game.ui_attack.dice_enabled

	game.ui_attack.on_retreat += lambda ev: self.on_retreat (self)
	game.ui_attack.on_attack += lambda ev: self.on_attack (self)
	self.risk_attack(self.src, self.dst)

	self._dice_box_attacker = ui.widget.VBox(self)
	self._dice_box_attacker.set_visible (True)


	self._dice_box_defender = ui.widget.VBox(self)
	self._dice_box_defender.set_visible (True)


    def do_release (self):
        self.game.ui_world.disable_used ()
	self.game.ui_world.disable_picking ()
        super (RiskAttackState, self).do_release ()
        
    @weak_slot
    def on_attack (self, src, dst):
        _log.debug ('Attacking from %s to %s.' %
                    (str (src.model), str (dst.model)))
	self.game.ui_attack.dice_enable()
    
    def on_attack(self, _):
	
	"""
	Takes the amount of numbers in the number_of_dices, random a dice number and shows 
	them as buttonimages with the corresponding number.
	"""

        self.defender_dice_list = []
	self.attacker_dice_list = []
	self.used_attacker_number = 0
	print self.game.ui_attack.defender_number_of_dices

	for x in range(0, self.defender_number_of_dices):
	    temp = random.randint(1,6)
	    self.defender_dice_list.append(temp)
	    
	    self._dice = ui.widget.SmallButton (
                self._dice_box_attacker,None, 'data/icon/dice'+str(temp)+'.png')

	for x in range(0, self.attacker_number_of_dices):

	    temp = random.randint(1,6)
	    self.attacker_dice_list.append(temp)

	    self._dice = ui.widget.SmallButton (
                self._dice_box_defender, None, 'data/icon/dice'+str(temp)+'.png')

	self._dice_box_attacker.set_visible (True)
	self._dice_box_defender.set_visible (True)
	self.attacker_dice_list.sort()
	self.defender_dice_list.sort()
	self.lost_troop()
	
	

    def lost_troop (self):
	if len(self.attacker_dice_list) != 0 and len(self.defender_dice_list) != 0:
	    if self.src.model.troops > 1 and self.dst.model.troops > 0:

		if self.attacker_dice_list[0] == 0:
		    self.dice_disable()
		    return

		elif self.defender_dice_list[0] == 0:
		    return
		    
			
	        elif self.attacker_dice_list[0] <= self.defender_dice_list[0]:
		    """
		    If attackers highest dice is less or equal to defenders highest he loses a unit
		    and the number is popped from the defenders list aswell as the last number from the attackers list

		    """
		
		    self.src.model.troops -= 1
		    self.defender_dice_list.pop(0)
		    self.defender_dice_list.append(0)
		    self.attacker_dice_list.pop(len(self.attacker_dice_list)-1)

	        elif self.attacker_dice_list[0] > self.defender_dice_list[0]:

	   	    """
		    If defenders highest dice is less than attackers highest he loses a unit
		    and the number is popped from the attackers list
 
		    """

		    self.dst.model.troops -= 1
		    self.src.model.troops -= 1
		    self.src.model.used += 1
		    self.used_attacker_number += 1
		    self.attacker_dice_list.pop(0)
		    self.attacker_dice_list.append(0)
	        self.lost_troop()

	    elif self.src.model.troops == 1:
		"""
		Attacker is out of attacking units
		"""
		return
	        
	    elif self.dst.model.troops == 0:
		"""
		Defender is out of units
		"""
		self.dst.model.owner = self.src.model.owner
		self.dst.model.troops = len(self.attacker_dice_list)
		self.src.model.used -= self.used_attacker_number
		self.src.model.troops -= len(self.attacker_dice_list)-self.used_attacker_number
		self.game.ui_attack.dice_disable()
		self.manager.leave_state ()

	elif len(self.attacker_dice_list) == 0:
	    if self.src.model.troops == 1:
		"""
		Attacker is out of attacking units
		"""
		self.game.ui_attack.dice_disable()
		self.manager.leave_state ()
		
	elif len(self.defender_dice_list) == 0:

	    if self.dst.model.troops == 0:
		"""
		Defender is out of units
		"""

		self.dst.model.owner = self.src.model.owner
		self.dst.model.troops = len(self.attacker_dice_list)
		self.src.model.used -= self.used_attacker_number
		self.src.model.troops -= len(self.attacker_dice_list)-self.used_attacker_number
		self.game.ui_attack.dice_disable()
		self.manager.leave_state ()
		return
	    else:
	        self.src.model.troops -= len(self.attacker_dice_list)
	        self.src.model.used += len(self.attacker_dice_list)-self.used_attacker_number
		return


    def on_retreat(self, random):
	self.game.ui_attack.dice_disable()
        self.manager.leave_state ()	# Exit risk_attack state
