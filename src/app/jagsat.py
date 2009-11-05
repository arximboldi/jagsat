#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base.log import get_log
from base.app import *

_log = get_log (__name__)

class JagsatApp (AppBase):

    NAME = 'jagsat'
    
    OPTIONS = AppBase.OPTIONS + \
"""
Game options:
  -m, --map <file>   Map file to load.
"""

    LICENSE = \
"""
  This software is in development and the distribution terms have not
  been decided yet. Therefore, its distribution outside the JAGSAT
  project team or the Project Course evalautors in Abo Akademy is
  completly forbidden without explicit permission of their authors.
"""

    AUTHOR = 'The JAGSAT development team.'
    COPYRIGHT = 'Copyright (C) 2009 The JAGSAT development team.'

    def __init__ (self, *a, **k):
        super (JagsatApp, self).__init__ (*a, **k)
        self._arg_map = OptionWith (str)
        
    def do_prepare (self, args):
        args.add ('m', 'map', self._arg_map)
        
    def do_execute (self, args):
        _log.info ("Starting application...")        
        _log.info ("Quiting... Have a nice day ;)")
