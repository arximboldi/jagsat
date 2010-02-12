#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

import sys
sys.path.append ('lib')

import unittest

from test.model_map import *
from test.model_world import *

from test.base_arg_parser import *
from test.base_tree import *
from test.base_sender import *
from test.base_connection import * 
from test.base_signal import *
from test.base_meta import *
from test.base_observer import *
from test.base_observer_old import *
from test.base_conf import *
from test.base_xml_conf import *
from test.base_singleton import *
from test.base_log import *
from test.base_event import *
from test.base_changer import *
from test.core_task import *
from test.core_state import *

if __name__ == '__main__':
    unittest.main ()
