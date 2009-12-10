#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

import unittest
from base.singleton import *

class TestSingleton (unittest.TestCase):

    class SingletonMock:

        __metaclass__ = Singleton

    def test_singleton (self):
        a = TestSingleton.SingletonMock ()
        b = TestSingleton.SingletonMock ()

        self.assertTrue (a is b)
