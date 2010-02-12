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
from base.event import *
from base.sender import *

class TestEventManager (unittest.TestCase):

    def test_add_del (self):
        e = EventManager ()
        x = Receiver ()
        y = Receiver ()
        e.connect (x)
        self.assertEqual (e.count, 1)
        e.connect (y)
        self.assertEqual (e.count, 2)
        e.disconnect (x)
        self.assertEqual (e.count, 1)
        e.disconnect (y)
        self.assertEqual (e.count, 0)
        self.assertRaises (ValueError, e.disconnect, x)

    def test_forward_and_quiet (self):
        class DummyForwarder (Receiver):
            def __init__ (self):
                self.last = ''
            def receive (self, name, *a, **k):
                self.last = name

        fw = DummyForwarder ()
        mgr = EventManager ()
        mgr.connect (fw)
        
        a = mgr.event ('a').notify ()
        self.assertEqual (fw.last, 'a')
        
        b = mgr.notify ('b')
        self.assertEqual (fw.last, 'b')

        mgr.quiet = True
        mgr.notify ('a')
        self.assertEqual (fw.last, 'b')

    def test_notify_and_quiet (self):
        l = []
        def accum (x):
            l.append (x)

        mgr = EventManager ()
        mgr.event ('ac').connect (accum)

        mgr.notify ('ac', 1)
        self.assertEqual (l, [1])

        mgr.event ('ac') (2)
        self.assertEqual (l, [1, 2])

        mgr.quiet = True

        mgr.notify ('ac', 3)
        self.assertEqual (l, [1, 2])

        mgr.event ('ac') (3)
        self.assertEqual (l, [1, 2, 3])
