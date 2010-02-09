#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from state import State
import model.world
from tf.gfx import ui
from tf.gfx.widget import intermediate
from model.world import create_game
from base.conf import ConfNode
from ui.world import WorldComponent
from model.world import Region
from PySFML import sf
import random
from itertools import cycle
from base.log import get_log

ui2 = intermediate

THEME = { 'active' : sf.Color.Blue,
          'inactive' : sf.Color.Red, 
          'border' : sf.Color.Green,
          'thickness' : 2 }

class Init_game (State):
    
    def do_enter (self, *a, **k):
        sfview = self.system._window.window.GetDefaultView ()
        view  = ui.View (self.system._window, sfview)
        layer = ui.Layer (view)
        
        cfg = ConfNode (
            { 'player-0' :
              { 'name'     : 'jp',
                'color'    : 1,
                'position' : 2,
                'enabled'  : True },
	      'player-1' :
              { 'name'     : 'lamer',
                'color'    : 2,
                'position' : 1,
                'enabled'  : True },
              'player-2' :
              { 'name'     : 'pj',
                'color'    : 3,
                'position' : 4,
                'enabled'  : True },
              'map' : 'doc/map/worldmap.xml' })

        world = create_game (cfg)
        comp = WorldComponent (layer, world)
	self.regions = comp._regions
	self.players = world._players
	self.finished = False
	self.number_of_players = len(self.players)	#count the amount of players
	
	self.give_objectives()
	self.give_regions()  

	for x in comp._regions:
	    x.on_click += lambda ev, x=x:  self.place_troops(x)

    def give_objectives(self): 		#randomly give one objective to each player, should be filled in with the missions that alberto is working on

	for p in self.players.keys():
	    temp = self.players[p]
	    #temp.objective = self.objectives[random.random(0, len(self.objectives))]
	    pass   
	    
    def give_regions(self): 		#randomly divides the regions between the players

	random.shuffle(self.regions, random.random)
	for r, p in zip (self.regions, cycle(self.players.itervalues())):
	    r.owner = p

    def place_troops(self, x): 		#pressing a regions will increase the troops in the region by 1 and decrease player troops by 1
	if(x.owner.troops > 0):	
	    x.troops +=1		
	    x.owner.troops -=1		
			
	if x.owner.troops == 0:
	    print "owner has 0 troops, failed"
	    x.owner.can_pass = True
	    self.passed()

    def passed (self):		#if all players have 0 troops left to put out the program will automatically jump to turn based gameplay
	all_passed = True
	for p in self.players.keys():
	  
	    temp = self.players[p]
	    if temp.can_pass == False:
	        all_passed = False
	if all_passed == True:
	    self.turns = self.players.keys()
	    random.shuffle(self.turns)	#not sure at the moment what parameter is needed to be passed to reinforcement phase

