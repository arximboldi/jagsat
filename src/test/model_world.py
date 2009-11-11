#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

import unittest
import os

from base.conf import ConfNode
from model.world import *

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
        self.assertEquals (len (w.players),       2)
        self.assertEquals (w.players[0].name,     'jp')
        self.assertEquals (w.players[0].color,    1)
        self.assertEquals (w.players[0].position, 2)
