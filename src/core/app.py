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

from base.log import get_log
from base.app import AppBase
from base.conf import GlobalConf, OptionConfWith, OptionConfFlag

from state import StateManager
from tf_controller import TfController

_log = get_log (__name__)

class GameApp (AppBase, StateManager):

    OPTIONS = AppBase.OPTIONS + \
"""
Display options:
  -F, --fps <value>    Set the update frames per second.
  -f, --fullscreen     Enable fullscreen mode.
  -w, --window         Enable windowed mode.
  -b, --bpp <value>    Set window color depth.
  -W, --width <value>  Set window width.
  -H, --height <value> Set window height.
  -s, --vsync          Enable V-Sync.
  -S, --no-vsync       Disable V-Sync.
      --show-mouse     Shows the mouse cursor.
      --hide-mouse     Hides the mouse cursor.
"""

    def __init__ (self, *a, **k):
        super (GameApp, self).__init__ (*a, **k)

        self.root_state      = None
        self.root_state_args = []
        self.root_state_kwrs = {}
        
        self._system = None
        
    @property
    def system (self):
        return self._system

    def do_prepare (self, args):
        self._video_cfg = GlobalConf ().child ('video')
        cfg = self._video_cfg
        
        args.add ('F', 'fps', OptionConfWith (cfg.child ('fps'), int))
        args.add ('f', 'fullscreen', OptionConfFlag (cfg.child ('full')))
        args.add ('w', 'window', OptionConfFlag (cfg.child ('full'), False))
        args.add ('s', 'vsync', OptionConfFlag (cfg.child ('vsync')))
        args.add ('S', 'no-vsync', OptionConfFlag (cfg.child ('vsync'), False))
        args.add ('W', 'width', OptionConfWith (cfg.child ('width'), int))
        args.add ('H', 'height', OptionConfWith (cfg.child ('height'), int))
        args.add (None, 'show-mouse',
                  OptionConfFlag (cfg.child ('showmouse'), True))
        args.add (None, 'hide-mouse',
                  OptionConfFlag (cfg.child ('showmouse'), False))
        
    def do_execute (self, freeargs):
        _log.info ("Setting up system...")        
        self._system = TfController (self._video_cfg,
                                     self.NAME + ' ' + self.VERSION)
        _log.info ("Starting game...")
        self._system.tasks.add (self)
        self.start (self.root_state,
                    *self.root_state_args,
                    **self.root_state_kwrs)
        self._system.loop ()
        self._system.dispose ()
        self._system = None
    
    def do_release (self):
        _log.info ("Shutting down... Have a nice day ;)")
        if hasattr (self, '_video_ctl'):
            self._video_ctl.close ()
