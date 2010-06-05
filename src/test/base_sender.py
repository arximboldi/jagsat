#
#  Copyright (C) 2009, 2010 JAGSAT Development Team (see below)
#  
#  This file is part of JAGSAT.
#  
#  JAGSAT is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  
#  JAGSAT is distributed in the hope that it will be useful,
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


        
