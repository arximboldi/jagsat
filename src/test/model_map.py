#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
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

