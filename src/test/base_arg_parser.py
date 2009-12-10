#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

import unittest

from util import *
from base.arg_parser import *

class TestArgParser (unittest.TestCase):
    
    def setUp (self):
        self._op_a = OptionWith (int, -1)
        self._op_b = OptionFlag ()
        self._op_c = OptionFunc (mock_raiser)
        self._op_d = OptionWith (float, -1.0)
        
        self._args = ArgParser ()
        self._args.add ('a', 'alpha', self._op_a)
        self._args.add ('b', 'beta', self._op_b)
        self._args.add ('c', 'gamma', self._op_c)
        self._args.add ('d', 'delta', self._op_d)
        
    def tearDown (self):
        self._args = None

    def test_unkown_args (self):
        self.assertRaises (MockError, self._args.parse, ['test', '-c'])
        self.assertRaises (UnknownArgError, self._args.parse, ['test', '-x'])
        
    def test_int_option_and_multi_flag_argument (self):
        self._args.parse (['test', '-ab', '10'])
        self.assertEqual (self._op_a.value, 10)
        self.assertEqual (self._op_b.value, True)

    def test_corner_option (self):
        self._args.parse (['test', '--alpha'])
        self.assertEqual (self._op_a.value, -1)
        self.assertEqual (self._op_b.value, False)

    def test_float_option (self):
        self._args.parse (['test', '-ad', '2', '2.5'])
        self.assertEqual (self._op_a.value, 2)
        self.assertEqual (self._op_d.value, 2.5)
