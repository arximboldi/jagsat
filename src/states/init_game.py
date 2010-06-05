#
#  Copyright (C) 2009, 2010 JAGSAT Development Team (see below)
#  
#  This file is part of JAGSAT.
#  
#  JAGSAT is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  
#  JAGSAT is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  
#  JAGSAT Development Team is:
#    - Juan Pedro Bolivar Puente
#    - Alberto Villegas Erce
#    - Guillem Medina
#    - Sarah Lindstrom
#    - Aksel Junkkila
#    - Thomas Forss
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
from model.mission import create_missions

_log = get_log (__name__)


class InitGameState (GameSubstate):
    
    def do_setup (self, *a, **k):

        self.game.phase = 'init'

        if self.game._load_game: # HACK?
            self._finished = set ([
                p for p in self.game.world.players.itervalues ()
                if p.troops == 0 ])
        else:
            self._give_regions ()
            self._give_troops ()
            self._give_missions ()
            self._finished = set ()
        
	self.game.ui_world.on_click_region += self.on_place_troop
        self.game.ui_world.click_cond = lambda r: r.model.owner.troops > 0
        self.tasks.add (self.game.ui_world.rotate_to_owner ())
        
        if self.game.test_phase is None:
            self.manager.system.audio.play_sound (
                'data/sfx/drums/drum_march_2.wav')
            self.manager.enter_state (
                'message', message =
                "%50%Welcome to the game, emperors.\n"
                "Check your missions and place the troops.\n")
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
        factor =  len (self.game.world.regions) / 44.
        standard_troops = int (50 * factor - len (world.players) * 5 * factor) 
        for p in world.players.itervalues ():
            p.troops = standard_troops - len (world.regions_of (p))
    
    def _give_missions (self):
        """
        Randomly give one mission to each player.
        """
        world = self.game.world
        
        missions = create_missions (world)
        random.shuffle (missions)
        
	for p in world.players.itervalues ():
	    p.mission = missions.pop ()
    
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

        # DEBUG
        """
        for r, p in zip (regions, cycle ([world.ordered_players () [0]])):
	    r.owner  = p
            r.troops = 1
        self.manager.change_state ('game_round')
        """
    
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
