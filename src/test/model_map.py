#
#  Copyright (C) 2009, 2010 JAGSAT Development Team (see below)
#  
#  This file is part of TF.
#  
#  TF is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  
#  TF is distributed in the hope that it will be useful,
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

from model.map import load_map

import unittest
import os

_TEST_PATH = os.path.dirname (__file__)
_TEST_FILENAME = os.path.join (
    _TEST_PATH,
    '../../doc/file-formats/example-map.xml')

class TestLoadMap (unittest.TestCase):

    def setUp (self):
        self.map = load_map (_TEST_FILENAME)
        
    def test_load_world (self):
        self.assertEquals (len (self.map.regions), 2)
        self.assertEquals (len (self.map.continents), 1)

    def test_load_link (self):
        self.assertTrue (self.map.regions ['spain'] in \
                         self.map.regions ['finland'].neighbours)
        self.assertTrue (self.map.regions ['finland'] in \
                         self.map.regions ['spain'].neighbours)

    def test_load_meta (self):
        self.assertEquals (self.map.meta.author, 'John Foo')
        self.assertEquals (self.map.meta.description, 'Conquer the world!')

