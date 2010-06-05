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
import sys

from base.conf import ConfNode
from model.mission import *
from model.world import create_game

import unittest

import random
from itertools import cycle

cfg = ConfNode (
    { 'player-0' :
      { 'name'     : 'jp',
        'color'    : (255, 0, 0),
        'position' : 2,
        'enabled'  : True },
      'player-2' :
      { 'name'     : 'pj',
        'color'    : (0, 255, 0),
        'position' : 4,
        'enabled'  : True },
      'map' : 'data/map/world_map.xml' })

class TestMissions (unittest.TestCase):

    def setUp (self):
        self.world = create_game (cfg)
        self.obj = create_missions (self.world)
        
    def test_show_mission (self):
        pass # print "\nTesting show mission"
        for o in self.obj:
            pass # print o.str_mission()

    def test_give_mission (self):
        pass # print "\nTesting give mission"
        obj = self.obj
        random.shuffle (obj)

        for p in self.world.players.itervalues():
            p.mission = obj.pop()

        for p in self.world.players.itervalues():
            pass # print p.mission.str_mission()

    def test_check_mission_cont (self):
        pass # print "\nTesting check mission continent"
        world = self.world
        obj = self.obj
        cont_obj = filter (lambda o: o.type == 'continent',obj)
        random.shuffle (cont_obj)

        #Assign a mission to players
        for p in world.players.itervalues():
            p.mission = cont_obj.pop()

        #Show continents to conquer
        for p in world.players.itervalues():
            pass # print p.name+" has to conquer: " 
            for c in p.mission.goal:
                pass # print "\t"+c.name

        #Asign all regions
        for r, p in zip (world.regions.values(), cycle (world.ordered_players ())):
            r.owner  = p
            r.troops = 1
        
        #Assign propper regions to acomplish missions
        for p in world.players.itervalues():
            for c in p.mission.goal:
                for r in world.regions.itervalues():
                    if c.name == r.definition.continent.name:
                        #pass # print "Continente "+c.name
                        #pass # print "\tAsigna a: "+p.name+" region: "+r.definition.name
                        r.owner = p
                        r.troops = 1
        
        for p in world.players.itervalues():
            world.current_player = p
            if p.mission.check_mission (world):
                pass # print p.name+" mission acomplished"
            else:
                pass # print p.name+" mission failed"

    def test_check_mission_region (self):
        pass # print "\nTesting check mission region"
        world = self.world
        obj = self.obj
        reg_obj = filter (lambda o: o.type == 'region',obj)

        for p in world.players.itervalues():
            p.mission = reg_obj.pop()
        
        for r, p in zip (world.regions.values(), cycle (world.ordered_players ())):
            r.owner  = p
            r.troops = 2
        
        for p in world.players.itervalues():
            world.current_player = p
            pass # print p.name+" has to conquer "+str(p.mission.goal)+\
            #" with "+str(p.mission.info)+" troops each"
            if p.mission.check_mission (world):
                pass # print p.name+" mission acomplished"
            else:
                pass # print p.name+" mission failed"

        for r in world.regions.values():
            r.owner  = world.players['jp']
            r.troops = 1

        for p in world.players.itervalues():
            world.current_player = p
            pass # print p.name+" has to conquer "+str(p.mission.goal)+\
            #            " with "+str(p.mission.info)+" troops each"
            if p.mission.check_mission (world):
                pass # print p.name+" mission acomplished"
            else:
                pass # print p.name+" mission failed"

    def test_check_mission_player (self):
        pass # print "\nTesting check mission player"
        world = self.world
        obj = self.obj
        pla_obj = filter (lambda o: o.type == 'player',obj)
        random.shuffle(pla_obj)

        for r, p in zip (world.regions.values(), cycle (world.ordered_players ())):
            r.owner  = p
            r.troops = 2

        for p in world.players.itervalues():
            world.current_player = p
            p.mission = pla_obj.pop()
            p.mission.pre_check_mission (world)
            pass # print "Player: "+p.name+" has to "+p.mission.str_mission()

        for r in world.regions.values():
            r.owner  = world.players['pj']
            r.troops = 1
         
        for p in world.players.itervalues():
            world.current_player = p
            if p.mission.check_mission (world):
                pass # print p.name+" mission acomplished"
            else:
                pass # print p.name+" mission failed"
