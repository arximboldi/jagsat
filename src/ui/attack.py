#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base.log import get_log
from base import signal

from tf.gfx import ui
import widget
import theme
import random

from PySFML import sf

_log = get_log (__name__)

rotation = [ 180, 135, 45, 0, 315, 225 ]
position = [ (.5, .01), (.97, .03), (.97, .97),
             (0.5, .99), (.03, .97), (.03, .03) ]

class AttackComponent (widget.HBox, object):
#widget.VBox,
#self, parent = None, player = None, *a, **k

    def __init__ (self, parent = None, player = None, *a, **k):
        super (AttackComponent, self).__init__ (parent, *a, **k)
        
	self._but_theme = theme.SMALL_BUTTON_THEME
        self.player = player
	self.dice_enabled = False
	self.src = None
	self.dst = None
	self.set_position_rel (0.5, 0.5)
        self.set_center_rel (0.2, 0.2)
        self.padding_left = 20
	self.attacker_number_of_dices = 1
	self.defender_number_of_dices = 1
	self.defender_dice_list = []
	self.attacker_dice_list = []

	# The attack buttons

	self.on_attack = signal.Signal ()
	self.on_retreat = signal.Signal ()
	
	self._dice_box_attacker = widget.VBox(self)
	self._dice_box_attacker.set_position_rel (0.5, 0.5)
	self._dice_box_attacker.set_center_rel (0.5, 0.5)
	self._dice_box_attacker.set_visible (self.dice_enabled)


	self._dice_box_defender = widget.VBox(self)
	self._dice_box_defender.set_position_rel (0.5, 0.5)
	self._dice_box_defender.set_center_rel (0.5, 0.5)
	self._dice_box_defender.set_visible (self.dice_enabled)
	"""
	self._attack_box = widget.HBox (self)
	self._attack_box.set_position_rel (0.5, 0.5)
	self._attack_box.set_center_rel (0.5, 0.5)
	self._attack_box.padding_left = 20
	self._attack_box.set_visible (self.dice_enabled)
	"""


        self._attack_troops_increase = widget.Button (
            self, None, 'data/icon/a_increase.png', theme = self._but_theme)
        self._attack_troops_increase.on_click += lambda ev : self.attacker_troops_increase (self)
	self._attack_troops_increase.set_visible (self.dice_enabled)

        #self._attack_troops_decrease = widget.SmallButton (
        #    self._attack_box, None, 'data/icon/a_decrease.png')
        #self._attack_troops_decrease.on_click += lambda ev : self.attacker_troops_decrease (self)

        self._attack_troops_decrease = widget.Button (
            self, None, 'data/icon/a_decrease.png', theme = self._but_theme)
        self._attack_troops_decrease.on_click += lambda ev : self.attacker_troops_decrease (self)
	self._attack_troops_decrease.set_visible (self.dice_enabled)

	#self._defense_box = widget.HBox (self)
	#self._defense_box.set_position_rel (0.5, 0.5)
	#self._defense_box.set_center_rel (0.5, 0.5)
	#self._defense_box.padding_left = 20
	#self._defense_box.set_visible (self.dice_enabled)

        #self._defense_troops_increase = widget.SmallButton (
        #    self._defense_box, None, 'data/icon/d_increase.png')
        #self._defense_troops_increase.on_click += lambda ev : self.defender_troops_increase (self)

	self._defense_troops_increase = widget.Button (
            self, None, 'data/icon/d_increase.png', theme = self._but_theme)
        self._defense_troops_increase.on_click += lambda ev : self.defender_troops_increase (self)
	self._defense_troops_increase.set_visible (self.dice_enabled)

	#self._defense_troops_decrease = widget.SmallButton (
        #    self._defense_box, None, 'data/icon/d_decrease.png')
        #self._defense_troops_decrease.on_click += lambda ev : self.defender_troops_decrease (self)

	self._defense_troops_decrease = widget.Button (
            self, None, 'data/icon/d_decrease.png', theme = self._but_theme)
        self._defense_troops_decrease.on_click += lambda ev : self.defender_troops_decrease (self)
	self._defense_troops_decrease.set_visible (self.dice_enabled)
	

	self._choice_box = widget.HBox (self)
	self._choice_box.set_position_rel (0.5, 0.5)
	self._choice_box.set_center_rel (0.5, 0.5)
	self._choice_box.padding_left = 20
	self._choice_box.set_visible (self.dice_enabled)
	

        self._attack = widget.SmallButton (
            self._choice_box, 'Attack')
        self._attack.on_click += lambda ev: self.attack (self)

        self._retreat = widget.SmallButton (
            self._choice_box, 'Retreat')
        self._retreat.on_click += self.on_retreat


    def attack(self, _):
	print "attack"
	for x in range(0, self.defender_number_of_dices):
	    temp = random.randint(1,6)
	    self.defender_dice_list.append(temp)
	    
	    self._dice = widget.SmallButton (
                self._dice_box_attacker,None, 'data/icon/dice'+str(temp)+'.png')

	for x in range(0, self.attacker_number_of_dices):
	    temp = random.randint(1,6)
	    self.attacker_dice_list.append(temp)

	    self._dice = widget.SmallButton (
                self._dice_box_defender, None, 'data/icon/dice'+str(temp)+'.png')

	self._dice_box_attacker.set_visible (True)
	self._dice_box_defender.set_visible (True)
	self.attacker_dice_list.sort()
	self.defender_dice_list.sort()
	self.lost_troop()
	self.dice_enable()
	

    def lost_troop (self):
	if len(self.attacker_dice_list) != 0 and len(self.defender_dice_list) != 0:
	    if self.attacker_dice_list[0] <= self.defender_dice_list[0]:
		print "attacker lost unit"
		self.src.model.troops -= 1
		self.defender_dice_list.pop(0)
	    elif self.attacker_dice_list[0] > self.defender_dice_list[0]:
		print "defender lost unit"
		self.dst.model.troops -= 1
		self.attacker_dice_list.pop(0)
	    self.lost_troop()

	elif len(self.attacker_dice_list) == 0:
	    pass
	elif len(self.defender_dice_list) == 0:
	    if self.dst.model.troops == 0:

		#TODO: fix so that only non-used troops are moved and can attack

		self.dst.model.owner = self.src.model.owner
		self.dst.model.troops = self.src.model.troops -1
		self.src.model.troops = 1
	    else:
		return

    def attacker_troops_increase(self, _):
	if self.attacker_number_of_dices < 3 and self.src.model.troops > 1:
	    self.attacker_number_of_dices +=1
	    self.src.model.troops -=1

    def attacker_troops_decrease(self, _):
	if self.attacker_number_of_dices > 1:
	    self.attacker_number_of_dices -= 1
	    self.src.model.troops +=1

    def defender_troops_increase(self, _):
	if self.defender_number_of_dices < 2 and self.dst.model.troops > 1:
	    self.defender_number_of_dices +=1
	    self.dst.model.troops -=1

    def defender_troops_decrease(self, _):
	if self.defender_number_of_dices > 1:
	    self.defender_number_of_dices -= 1
	    self.dst.model.troops +=1

    def dice_enable (self):
	self.defender_dice_list = []
	self.attacker_dice_list = []
	self._attacker_number_of_dices = 1
	self._defender_number_of_dices = 1

	    

	self.dice_enabled = True
        self._dice_box_attacker.set_visible (self.dice_enabled)
	self._dice_box_defender.set_visible (self.dice_enabled)
	
	#self._attack_box.set_visible (self.dice_enabled)
	#self._defense_box.set_visible (self.dice_enabled)
	self._choice_box.set_visible (self.dice_enabled)

	self._attack_troops_increase.set_visible (self.dice_enabled)
	self._attack_troops_decrease.set_visible (self.dice_enabled)
	self._defense_troops_increase.set_visible (self.dice_enabled)
	self._defense_troops_decrease.set_visible (self.dice_enabled)



    def enable_pass (self):
        pass

    def disable_pass (self):
        pass
