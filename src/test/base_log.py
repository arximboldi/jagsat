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
from StringIO import StringIO

from base.log import *

class TestLog (unittest.TestCase):

    def setUp (self):
        self.info_out  = StringIO ()
        self.error_out = StringIO ()

        self.node = LogNode ()
        self.node.name = "test"
        self.node.connect (
            StdLogListener (LOG_INFO,
                            self.info_out,
                            self.error_out))

    def test_message (self):
        msg_one = "[test.a.b] INFO: test one\n"
        msg_two = "[test.a.b] FATAL: test two\n"

        self.node.get_path ('a.b').log (LOG_INFO, "test one")
        self.node.get_path ('a.b').log (LOG_FATAL, "test two")
        self.node.get_path ('a.b').log (LOG_DEBUG, "test three")
        
        self.assertEqual (self.info_out.getvalue (), msg_one)
        self.assertEqual (self.error_out.getvalue (), msg_two)

