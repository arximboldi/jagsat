#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

import random
from itertools import cycle

from base.log import get_log
from quit import QuittableState

_log = get_log (__name__)


class InitGameState (QuittableState):
    
    def do_setup (self, *a, **k):
        game = self.parent_state

        self._give_troops ()
	self._give_objectives ()
	self._give_regions ()
        self._finished = set ()
        
	game.ui_world.on_click_region += self.on_place_troop

    def _give_troops (self):
        """
        Give troops to player. TODO: Match Risk rules.
        """
        world = self.parent_state.world
        for p in world.players.itervalues ():
            p.troops = 20

    def _give_objectives (self):
        """
        Randomly give one objective to each player, should be
        filled in with the missions that alberto is working on
        """

        world = self.parent_state.world
        objectives = ['obj-a', 'obj-b', 'obj-c', 'obj-d', 'obj-e', 'obj-f']
        random.shuffle (objectives)
        
	for p in world.players.itervalues ():
	    p.objective = objectives.pop ()
    
    def _give_regions (self):
        """
        Randomly divides the regions between the players
        """
        _log.debug ('Giving regions')
        world = self.parent_state.world
        regions = world.regions.values ()
	random.shuffle (regions)
        
	for r, p in zip (regions, cycle (world.ordered_players ())):
	    r.owner = p

    def on_place_troop (self, region):
        """
        Pressing a regions will increase the troops in the region by 1
        and decrease player troops by 1
        """
        region = region.model
        _log.debug ('Placing troop on region: ' + region.definition.name)
	if region.owner.troops > 0:	
	    region.troops += 1
	    region.owner.troops -= 1
        else:
            self._finish_player (region.owner)
            
    def _finish_player (self, p):
        """
        If all players have 0 troops left to put out the program will
        automatically jump to turn based gameplay
        """
        _log.debug ('Player %s have finished the init phase.' % p.name)
        game = self.parent_state
        
        if not p in self._finished:
            self._finished.add (p)
            if len (self._finished) == len (game.world.players):
                self.manager.change_state ('game_round')
