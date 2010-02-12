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
from base.sender import *

class OneReceiver (Receiver):

    def on_something (self):
        self.value = 'something'

    def on_somewhat (self, param):
        self.value = param
    
class TestSender (unittest.TestCase):

    def setUp (self):
        self.one = OneReceiver ()
        self.two = OneReceiver ()
        self.sender = Sender ()

    def test_add_del (self):
        self.assertEqual (self.sender.count, 0)
        self.sender.connect (self.one)
        self.assertEqual (self.sender.count, 1)
        self.sender.connect (self.two)
        self.assertEqual (self.sender.count, 2)
        self.sender.connect (self.two)
        self.assertEqual (self.sender.count, 2)

        self.sender.disconnect (self.two)
        self.assertEqual (self.sender.count, 1)
        self.assertRaises (ValueError, self.sender.disconnect, self.two)
        self.sender.disconnect (self.one)
        self.assertEqual (self.sender.count, 0)

    def test_sending (self):
        self.sender.connect (self.one)
        self.sender.connect (self.two)

        self.sender.send ('on_something')
        self.assertEqual (self.one.value, 'something')
        self.assertEqual (self.two.value, 'something')

        self.sender.send ('on_somewhat', 'what')
        self.assertEqual (self.one.value, 'what')
        self.assertEqual (self.two.value, 'what')

        self.sender.disconnect (self.one)
        self.sender.send ('on_something')
        self.assertEqual (self.one.value, 'what')
        self.assertEqual (self.two.value, 'something')


        
