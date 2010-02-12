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
from base.xml_conf import *
from base.util import read_file
import os
import os.path

XML_TEST_PATH = os.path.dirname (__file__)
XML_TEST_FILENAME = os.path.join (XML_TEST_PATH, 'base_xml_conf_test_file.xml')
XML_TEMP_FILENAME = os.path.join (XML_TEST_PATH, 'base_xml_conf_temp_file.xml')

class TestXmlConfWrite (unittest.TestCase):

    def test_write (self):
        conf = ConfNode (name = 'test')
        conf.path ('a').value = 1
        conf.path ('b.c').value = 2
        conf.path ('b.d').value = 3

        xml = XmlConfBackend (XML_TEMP_FILENAME)
        conf.set_backend (xml)

        conf.save ()

        self.assertEqual (read_file (XML_TEST_FILENAME),
                          read_file (XML_TEMP_FILENAME))

        os.remove (XML_TEMP_FILENAME)

class TestXmlConfRead (unittest.TestCase):

    def setUp (self):
        self.conf = ConfNode ()
        self.xml = XmlConfBackend (XML_TEST_FILENAME)
        self.conf.set_backend (self.xml)

    def test_read (self):
        self.conf.load ()

        self.assertEqual (self.conf.name, 'test')
        self.assertEqual (self.conf.path ('a').value, 1)
        self.assertEqual (self.conf.path ('b.c').value, 2)
        self.assertEqual (self.conf.path ('b.d').value, 3)

    def test_read_default (self):
        self.conf.child ('a').value = 10
        self.conf.load (False)

        self.assertEqual (self.conf.name, 'test')
        self.assertEqual (self.conf.path ('a').value, 10)
        self.assertEqual (self.conf.path ('b.c').value, 2)
        self.assertEqual (self.conf.path ('b.d').value, 3)

