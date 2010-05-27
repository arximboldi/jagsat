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

from PySFML import sf

from tf.behavior.gameloop import get_game_loop
from tf.behavior.eventloop import EventLoop
from tf.gfx.ui import Window, View

from base.conf import GlobalConf
from base.signal import slot, Signal
from base.connection import Tracker

from input import KeyboardManager
from timer import Timer
import task

class TfController (Tracker):

    DEFAULT_WIDTH      = 1024
    DEFAULT_HEIGHT     = 768
    DEFAULT_FPS        = 60
    DEFAULT_BPP        = 32
    DEFAULT_ANTIALIAS  = 4
    DEFAULT_VSYNCH     = False
    DEFAULT_FULLSCREEN = False
    DEFAULT_SHOWMOUSE  = False
    
    def __init__ (self, conf = None, window_title = '', *a, **k):
        super (TfController, self).__init__ (*a, **k)

        self._conf = GlobalConf ().child ('video') if conf is None else conf
        self._window_title = window_title
        self._is_setup = False
        self._music = None
        
        self.on_sfml_event = Signal () # TODO: abstract sfml here
        
        self._setup_conf_defaults ()
        self._setup_conf_signals ()
        self._setup_window ()
        self._setup_logic ()
        self._setup_input ()

    def dispose (self):
        if self._is_setup:
            self.on_sfml_event.clear ()
            self._event_loop.signal_event.remove (self.on_sfml_event)
            self.disconnect_all ()
            self._window.Close ()
            self._is_setup = False

    def play_music (self, file):
        if self._music:
            self._music.Stop ()
        self._music = sf.Music ()
        self._music.OpenFromFile (file)
        self._music.Play ()
        
    def loop (self):        
        self._timer.reset ()
        self._timer.loop (self._loop_fn)

    def _loop_fn (self, timer):
        if self._tasks.count > 1:
            return self._tasks.update (timer)
        return False

    @property
    def audio (self):
        return self._game_loop.get_audiomanager ()
    
    @property
    def keys (self):
        return self._keyboard
    
    @property
    def game (self):
        return self._game_loop

    @property
    def timer (self):
        return self._timer
    
    @property
    def tasks (self):
        return self._tasks
    
    @property
    def sfml_window (self):
        return self._window
    
    @property
    def window (self):
        return self._tf_window

    @property
    def view (self):
        return self._tf_view

    def _setup_input (self):
        self._keyboard = KeyboardManager ()
        self.on_sfml_event += self._keyboard.on_sfml_event

    def _setup_logic (self):
        self._timer = Timer ()
        self._tasks = task.TaskGroup ()
        self._game_loop  = get_game_loop ()
        self._event_loop = EventLoop ('screenshot', self._tf_window,
                                      self._game_loop, None)
        self._event_loop.signal_event.add (self.on_sfml_event)
        self._tasks.add (task.repeat (task.run (self._event_loop.loop_once)))
        
    def _setup_window (self):
        self._window = sf.RenderWindow (
            sf.VideoMode (self._conf.child ('width').value,
                          self._conf.child ('height').value,
                          self._conf.child ('bpp').value),
            self._window_title,
            sf.Style.Fullscreen if self._conf.child ('full').value else 0,
            sf.WindowSettings (AntialiasingLevel =
                               self._conf.child ('antialias').value))
        self._window.ShowMouseCursor (self._conf.child ('showmouse').value)
        self._window.SetFramerateLimit (self._conf.child ('fps').value)
        self._window.UseVerticalSync (self._conf.child ('vsync').value)

        self._tf_window = Window (self._window)
        self._tf_view   = View (self._tf_window, self._window.GetDefaultView ())
    
    def _setup_conf_defaults (self):
        self._conf.child ('width').default (self.DEFAULT_WIDTH)
        self._conf.child ('height').default (self.DEFAULT_HEIGHT)
        self._conf.child ('full').default (self.DEFAULT_FULLSCREEN)
        self._conf.child ('fps').default (self.DEFAULT_FPS)
        self._conf.child ('bpp').default (self.DEFAULT_BPP)
        self._conf.child ('vsync').default (self.DEFAULT_VSYNCH)
        self._conf.child ('antialias').default (self.DEFAULT_ANTIALIAS)
        self._conf.child ('showmouse').default (self.DEFAULT_SHOWMOUSE)

    def _setup_conf_signals (self):
        self._conf.on_conf_nudge                  += self._on_nudge_video
        self._conf.child ('fps').on_conf_change   += self._on_change_fps
        self._conf.child ('vsync').on_conf_change += self._on_change_vsync

    @slot
    def _on_change_fps (self, node):
        self._window.SetFrameLimit (node.value)

    @slot
    def _on_change_vsync (self, node):
        self._window.UseVerticalSync (node.value)

    @slot
    def _on_nudge_video (self, node):
        self._window.Create (
            sf.VideoMode (self._conf.child ('width').value,
                          self._conf.child ('height').value,
                          self._conf.child ('bpp').value),
            self._window_title,
            sf.Style.Fullscreen if self._conf.child ('full').value else 0)
