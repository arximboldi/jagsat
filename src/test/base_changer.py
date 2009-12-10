#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

import unittest
from util import *
from base.changer import Changer

class TestChanger (unittest.TestCase):

    def test_member (self):
        class Mock (object):
            changer = Changer (mock_raiser, 0)

        a = Mock ()
        self.assertEquals (a.changer, 0)

        def setter (x, val):
            x.changer = val
            
        self.assertRaises (MockError, setter, a, 1)
        self.assertEquals (a.changer, 1)

        b = Mock ()
        self.assertRaises (MockError, setter, b, 2)
        self.assertEquals (a.changer, 1)
        
