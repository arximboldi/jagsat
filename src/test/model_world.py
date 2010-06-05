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
from base.conf import ConfNode
from model.world import *

import os
_TEST_PATH = os.path.dirname (__file__)
_TEST_FILENAME = os.path.join (
    _TEST_PATH,
    '../../doc/file-formats/example-map.xml')

class TestWorld (unittest.TestCase):

    def test_create (self):

        cfg = ConfNode (
            { 'player-0' :
              { 'name'     : 'jp',
                'color'    : 1,
                'position' : 2,
                'enabled'  : True },
              'player-2' :
              { 'name'     : 'pj',
                'color'    : 3,
                'position' : 4,
                'enabled'  : True },
              'map' : _TEST_FILENAME })
        
        w = create_game (cfg)
        self.assertEquals (len (w._players),       2)
        self.assertEquals (w._players['jp'].name,     'jp')
        self.assertEquals (w._players['jp'].color,    1)
        self.assertEquals (w._players['jp'].position, 2)
