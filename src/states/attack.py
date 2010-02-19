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
	
	self.risk_attack(src, dst)
    

    def risk_attack (self, src, dst):

	"""
	Basic risk attack system. Attacker gets to throw up to 3 dices, defender throws up to 2 dices.
	If the highest dice of the defender is same or greater than the attackers highest then the attacker
	loses one troop, same goes for second dice if defender has two. If the attackers highest dice is 
	higher than the defenders highest the defender loses a troop etc. This is done by adding elements to
	a list depending on how many troops there are in the region and then comparing the list elements 
	between attacker and defender.
	"""	

	defender_dice_list =[]
	attacker_dice_list =[]
	
	if dst.model.troops >= 2:
	    defender_dice_list.append(random.randint(1,6))
	    defender_dice_list.append(random.randint(1,6))
	elif dst.model.troops == 1:
	    defender_dice_list.append(random.randint(1,6))
	elif dst.model.troops == 0:
	    if src.model.troops > 1:
	        dst.model.owner = self.game.world.current_player
	        dst.model.troops = src.model.troops -1
	        src.model.troops = 1
	    return
	if src.model.troops > 3:
	    attacker_dice_list.append(random.randint(1,6))
	    attacker_dice_list.append(random.randint(1,6))
	    attacker_dice_list.append(random.randint(1,6))
	elif src.model.troops == 3:
	    attacker_dice_list.append(random.randint(1,6))
	    attacker_dice_list.append(random.randint(1,6))
	elif src.model.troops == 2:
	    attacker_dice_list.append(random.randint(1,6))
	elif src.model.troops == 1:
	    return

	defender_dice_list.sort()
	defender_dice_list.reverse()
	attacker_dice_list.sort()
	attacker_dice_list.reverse()
	
	for n in defender_dice_list:
	    try:
	        if defender_dice_list[0] == 0:
	            break
	        if defender_dice_list[0] >= attacker_dice_list[0]:       
	            defender_dice_list.pop(0)
		    defender_dice_list.append(0)
	            src.model.troops -=1	
		    if src.model.troops <= 1:
		        break
	        if defender_dice_list[0] < attacker_dice_list[0]:
		    attacker_dice_list.pop(0)
		    dst.model.troops -=1
		    if dst.model.troops == 0:
		        break
	    except Exception:
	        break

	#self.risk_attack(src, dst)
	self.manager.change_state ('move')	# Hop to MovementState


	

