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
from base.conf import *

class TestConfBackend:

    class MockBackend:
        def __init__ (self):
            self.called = None
        def _do_load (self, overwrite):
            self.called = "_do_load"
        def _do_save (self):
            self.called = "_do_save"
        def _handle_conf_new_child (self):
            self.called = "_handle_conf_new_child"
        def _handle_conf_del_child (self):
            self.called = "_handle_conf_del_child"

    def test_called (self):
        c = ConfNode ()
        c.backend = TestConfBackend.MockBackend ()

        c.load ()
        self.assertEqual (c.backend.called, "_do_load")
        c.save ()
        self.assertEqual (c.backend.called, "_do_load")
        c.child ("x")
        self.assertEqual (c.backend.called, "_handle_cond_new_child")
        c.remove ("x")
        self.assertEqual (c.backend.called, "_handle_conf_del_child")
        c.val = 1
        self.assertEqual (c.backend.called, "_handle_conf_change")
        c.nudge ()
        self.assertEqual (c.backend.called, "_handle_conf_nudge")

    def test_set_backend (self):
        c = ConfNode ()
        c.child ("a")
        c.backend = TestConfBackend.MockBanckend ()
        c.child ("b")

        self.assertTrue (isinstance (c.backend,
                                     TestConfBackend.MockBanckend))
        self.assertTrue (isinstance (c.child ("a").backend,
                                      TestConfBackend.MockBanckend))
        self.assertTrue (isinstance (c.child ("b").backend,
                                      TestConfBackend.MockBanckend))
        self.assertRaises (ConfError,
                           c.child ("a").set_backend, ConfBackend ())
        
    def test_global_conf (self):
        cfg = GlobalConf ()

        self.asserTrue (isinstance (cfg.path ("h.o.l.a"), ConfNode))
        self.asserTrue (not isinstance (cfg.path ("h.o.l.a"), GlobalConf))
