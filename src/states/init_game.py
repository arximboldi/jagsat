#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from PySFML import sf

import random
from itertools import cycle
from base.signal import weak_slot

from base.log import get_log
from game import GameSubstate
from ui import widget
from ui import theme
from core import task

_log = get_log (__name__)


class InitGameState (GameSubstate):
    
    def do_setup (self, *a, **k):
        self._give_regions ()
        self._give_troops ()
	self._give_objectives ()
        self._finished = set ()
        
	self.game.ui_world.on_click_region += self.on_place_troop
        self.game.ui_world.click_cond = lambda r: r.model.owner.troops > 0
        
        if self.game.test_phase is None:
            self.manager.enter_state (
                'message', message =
                "Welcome to the game, emperors.\n"
                "Check your missions and add the troops.\n")
        else:
            self._change_to_test ()

    def do_release (self):
        self.game.ui_world.click_cond = None

    def _change_to_test (self):
        world = self.game.world
        for p in world.players.itervalues ():
            p.troops = 0
        for r in world.regions.itervalues ():
            r.troops += random.randint (0, 10)
        self.manager.change_state ('game_round')
        
    def _give_troops (self):
        """
        Give troops to player.
        """
        world = self.game.world
        standard_troops = 50 - len (world.players) * 5 
        for p in world.players.itervalues ():
            p.troops = standard_troops - len (world.regions_of (p))
    
    def _give_objectives (self):
        """
        Randomly give one objective to each player, should be
        filled in with the missions that alberto is working on
        """

        objectives = ['obj-a', 'obj-b', 'obj-c', 'obj-d', 'obj-e', 'obj-f']
        random.shuffle (objectives)
        
	for p in self.game.world.players.itervalues ():
	    p.objective = objectives.pop ()
    
    def _give_regions (self):
        """
        Randomly divides the regions between the players
        """
        _log.debug ('Giving regions')
        world = self.game.world
        regions = world.regions.values ()
	random.shuffle (regions)
        
	for r, p in zip (regions, cycle (world.ordered_players ())):
	    r.owner  = p
            r.troops = 1

    @weak_slot
    def on_place_troop (self, region):
        """
        Pressing a regions will increase the troops in the region by 1
        and decrease player troops by 1
        """
        region = region.model
        _log.debug ('Placing troop on region: ' + region.definition.name)

        region.troops += 1
        region.owner.troops -= 1
                    
        if region.owner.troops <= 0:
            self._finish_player (region.owner)
            
    def _finish_player (self, p):
        """
        If all players have 0 troops left to put out the program will
        automatically jump to turn based gameplay
        """
        _log.debug ('Player %s have finished the init phase.' % p.name)
        
        if not p in self._finished:
            self._finished.add (p)
            if len (self._finished) == len (self.game.world.players):
                self.manager.change_state ('game_round')
