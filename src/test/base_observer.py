#
# Copyright (C) 2009 The JAGSAT project team.
#
# This software is in development and the distribution terms have not
# been decided yet. Therefore, its distribution outside the JAGSAT
# project team or the Project Course evalautors in Abo Akademy is
# completly forbidden without explicit permission of their authors.
#
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import unittest
from base.observer import *


_Subject, _Listener = \
    make_observer (['on_test'], '_', __name__)

class AListener (_Listener):

    def __init__ (self):
        super (AListener, self).__init__ ()
        self.message = None
        
    def on_test (self):
        self.message = "test"

class TestObserver (unittest.TestCase):
        
    def test_emit (self):
        
        sub = _Subject ()
        lis = AListener ()
        
        sub.connect (lis)
        self.assertEquals (sub.count, 1)
        
        sub.on_test ()
        self.assertEquals (lis.message, "test")

