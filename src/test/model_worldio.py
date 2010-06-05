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

import unittest
import os
import os.path

from base.conf import ConfNode
from model.world import create_game
from model.worldio import load_game, save_game
from PySFML import sf

_TEST_PATH = os.path.dirname (__file__)
_TEMP_FILE = os.path.join (_TEST_PATH, 'model_worldio_test_file')

_test_profile = ConfNode (
    { 'player-0' :
      { 'name'     : 'jp',
        'color'    : sf.Color (255, 0, 0),
        'position' : 3,
        'enabled'  : True },
      'player-2' :
      { 'name'     : 'pj',
        'color'    : sf.Color (0, 255, 0),
        'position' : 4,
        'enabled'  : True },
      'player-3' :
      { 'name'     : 'pjj',
        'color'    : sf.Color (0, 0, 255),
        'position' : 5,
        'enabled'  : True },
      'map' : 'data/map/world_map.xml' })


class TestWorldIO (unittest.TestCase):

    def test_save (self):        
        x = create_game (_test_profile)
        save_game (x, _TEMP_FILE)

    def test_load (self):
        x = create_game (_test_profile)
        x.regions ['spain'].used = 10
        save_game (x, _TEMP_FILE)
        y = load_game (_TEMP_FILE)
        self.assertEquals (y.regions ['spain'].used, 10)



        
        
