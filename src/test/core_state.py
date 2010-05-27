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
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import unittest
from core.state import *

class DummyStateBase (State):

    def __init__ (self, *a, **k):
        super (DummyStateBase, self).__init__ (*a, **k)
        self.st = "init"

    def do_setup (self):
        self.st = "setup"

    def do_sink (self):
        self.st = "sink"

    def do_unsink (self):
        self.st = "unsink"

    def do_release (self):
        self.st = "release"

class DummyStateOne (DummyStateBase):
    pass

class DummyStateTwo (DummyStateBase):
    pass

class TestState (unittest.TestCase):

    def setUp (self):
        self.mgr = StateManager ()
        self.mgr.add_state ('one', DummyStateOne)
        self.mgr.add_state ('two', DummyStateTwo)
    
    def test_errors (self):
        self.assertEqual (self.mgr.current, None)
        self.mgr.leave_state ()
        self.assertRaises (StateError, self.mgr.update, 0)
        self.mgr.start ('one')
        self.assertRaises (StateError, self.mgr.start, 'one')
        
    def test_machine (self):
        self.mgr.start ('one')
        self.assertTrue (isinstance (self.mgr.current, DummyStateOne))
        self.assertEqual (self.mgr.current.st, 'setup')
        da = self.mgr.current
        
        self.mgr.enter_state ('two')
        self.assertTrue (isinstance (self.mgr.current, DummyStateOne))
        self.assertEqual (self.mgr.current.st, 'setup')
        self.mgr.update (None)
        self.assertTrue (isinstance (self.mgr.current, DummyStateTwo))
        self.assertEqual (self.mgr.current.st, 'setup')
        self.assertEqual (da.st, 'sink')
        db = self.mgr.current

        self.mgr.leave_state ()
        self.mgr.update (None)
        self.assertEqual (da.st, 'unsink')
        self.assertEqual (self.mgr.current, da)
        self.assertEqual (db.st, 'release')

        self.mgr.change_state ('one')
        self.mgr.update (None)
        self.assertTrue (isinstance (self.mgr.current, DummyStateOne))
        self.assertNotEqual (self.mgr.current, da)
        self.assertEqual (self.mgr.current.st, 'setup')
        self.assertEqual (da.st, 'release')
