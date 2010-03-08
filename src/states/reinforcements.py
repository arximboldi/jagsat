#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

import random
from base.signal import weak_slot
from base.log import get_log
from game import GameSubstate

_log = get_log (__name__)

class ReinforcementState (GameSubstate):

    def do_setup (self, *a, **k):
        super (ReinforcementState, self).do_setup (*a, **k)

        game = self.game
	game.world.current_player.troops = self._count_continent_troops () + \
                                           self._count_region_troops ()        
	game.ui_world.on_click_region += self.on_place_troop

        self.manager.enter_state ('message', message =
            "New turn for player: %s.\n%s" % (game.world.current_player.name,
            "Place your reinforcements on the map."))

    def do_release (self):
        pass # Fill with signal deallocation, but first try to check
             # why the weak_slot is not doing the job.
        
    def _count_region_troops (self):
	""" This method counts the reinforcements that the player
	should get for having conquered whole continents."""	

        world = self.game.world
        num_regions = len (filter (lambda r: r.owner == world.current_player,
                                   world.regions.values ()))
	return max (3, num_regions / 3)
	
    def _count_continent_troops (self):
	""" This method counts the reinforcements that the player
	should get for having conquered whole continents."""
	
        world = self.game.world
	continents = self.game.world.map.continents
        player_regions = [ r.definition for r in world.regions.values ()
                           if r.owner == world.current_player ]

	return sum (c.troops
                    for c in continents.itervalues ()
                    if len (c.regions) ==
                    len (filter (lambda r: r.continent == c, player_regions)))
            
    def _count_card_troops(self):	
	# TODO: Not sure how to handle cards at the moment JP ANSWER:
        # We should manage them with help from the PlayerComponent, no
        # worries by now.
	pass

    @weak_slot
    def on_place_troop (self, region):
        """
        Pressing a regions will increase the troops in the region by 1
        and decrease player troops by 1
        """
	player = self.game.world.current_player
        region = region.model
        
        _log.debug ('Placing troop on region: ' + region.definition.name)
	if  player.troops > 0 and region.owner == player:	
	    region.troops += 1
	    region.owner.troops -= 1

        if player.troops <= 0:
            self.manager.change_state ('attack')
