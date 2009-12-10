#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

import unittest
from base.meta import *

class TestMeta (unittest.TestCase):

    class Tester_1:
        def __init__ (self):
            self.count = 0
            
    class Tester_2 (Tester_1):        
        def method (self):
            return "ok"

    def extension (self):
        self.count += 1
    
    extend_methods (Tester_1, extension = extension)
    extend_methods (Tester_2, method = extension)

    def test_addition (self):
        a = TestMeta.Tester_1 ()
        a.extension ()
        self.assertEqual (a.count, 1)
        
    def test_replace (self):
        a = TestMeta.Tester_2 ()
        r = a.method ()
        self.assertEqual (r, "ok")
        self.assertEqual (a.count, 1)

