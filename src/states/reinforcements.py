#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

import random
#from itertools import cycle
from base.log import get_log
from round import GameRoundState


class ReinforcementState (GameRoundState):

    def do_setup (self, *a, **k):
        super (ReinforcementState, self).do_setup (*a, **k)
        game = self.game
    
	self.player_turn = self.game.world.players.keys()
	#random.random(self.player_turn)
	self._regions = self.game.ui_world.regions
	
	self._add_region_troops()
	self._add_continent_troops()  
	self._add_card_troops()

	self.game.ui_world.on_click_region += self.on_place_troop

    def _add_region_troops(self):

	"""this method counts how many regions the player taking the turn owns and then decides
	to either give the minimum amount of troops (=3) or the amount of regions divided by 3."""	

	i = 0	
	for x in self.game.world.regions.values():
	    if x.owner == self.game.world.players[self.player_turn[0]]:
	        i += 1
	if i >= 12:
	    self.game.world.players[self.player_turn[0]].troops += i/3

	else:
	    self.game.world.players[self.player_turn[0]].troops += 3	    
	
    def _add_continent_troops(self):

	"""This method automatically goes through all the continents and checks if they are
	ownerd by the player taking the turn. Continent_owner is set to true and if a region
	is not owned by that player it will be set to false and the loop broken."""
	

	continents = self.game.world.map.continents
	regions = self.game.world.regions
	player = self.game.world.players
	
	for x in continents.values():	
	    continent_owner = True
	    
	    for r in x.regions:
		if regions.has_key(r.name):
		    if regions[r.name].owner == player[self.player_turn[0]]:
		        pass
		    else:
		        continent_owner = False
			break
	    if continent_owner:
		self.game.world.players[self.player_turn[0]].troops += x.troops
		
    def _add_card_troops(self):	
	#TODO: Not sure how to handle cards at the moment				
	pass
    
    def on_place_troop (self, region):
        """
        Pressing a regions will increase the troops in the region by 1
        and decrease player troops by 1
        """
	player = self.game.world.players
        region = region.model
        _log.debug ('Placing troop on region: ' + region.definition.name)
	if  region.owner == player[self.player_turn[0]] and region.owner.troops > 0:	
	    region.troops += 1
	    region.owner.troops -= 1
        elif region.owner == player[self.player_turn[0]] and region.owner.troops == 0:
            self._finish_player (region.owner)
	else:
	    _log.debug ('Wrong owner of region: ' + region.definition.name)

    def _finish_player (self, p):
        """
        If the active player has 0 troops left to put out the program will
        automatically jump to turn attack phase
        """
        _log.debug ('Player %s have finished the reinforcement phase.' % p.name)
        
        self.manager.change_state ('attack_state')
