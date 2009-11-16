#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base.log import get_log
from base.app import AppBase
from base.conf import GlobalConf, OptionConfWith, OptionConfFlag

from tf.behavior.gameloop import get_game_loop
from tf.behavior.eventloop import EventLoop
from tf.behavior.sm import StateMachine
from tf.gfx.ui import Window

from sfml_controller import SfmlController

_log = get_log (__name__)

class GameApp (AppBase):

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
"""

    def __init__ (self, *a, **k):
        super (GameApp, self).__init__ (*a, **k)
        self.root_state = None

    @property
    def game (self):
        return self._game_loop

    @property
    def state_machine (self):
        return self._state_machine

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

    def do_execute (self, freeargs):
        _log.info ("Setting up system...")        
        self._video_ctl = SfmlController (self._video_cfg,
                                          self.NAME + ' ' + self.VERSION)
        self._video_ctl.setup ()
        self._window = Window (self._video_ctl.window)
        
        self._game_loop  = get_game_loop ()
        self._event_loop = EventLoop (self.NAME,
                                      self._window,
                                      self._game_loop,
                                      None)
        self._state_machine = StateMachine (self.NAME, self.root_state, system = self)
        #self._state_machine.start (self._game_loop, self)

        self._game_loop.add_statemachine (self._state_machine)
        _log.info ("Starting game...")
        self.do_loop ()
        
    def do_loop (self):
        self._event_loop.loop ()

    def do_release (self):
        _log.info ("Shutting down... Have a nice day ;)")
        if hasattr (self, '_video_ctl'):
            self._video_ctl.close ()

