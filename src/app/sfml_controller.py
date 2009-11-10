#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from PySFML import sf
from base.conf import GlobalConf
from base.signal import slot
from base.connection import Tracker

class SfmlController (Tracker):

    DEFAULT_WIDTH      = 1024
    DEFAULT_HEIGHT     = 768
    DEFAULT_FPS        = 60
    DEFAULT_BPP        = 32
    DEFAULT_VSYNCH     = False
    DEFAULT_FULLSCREEN = False
    
    def __init__ (self, conf = None, window_title = '', *a, **k):
        super (SfmlController, self).__init__ (*a, **k)
        self._conf = GlobalConf ().child ('video') if conf is None else conf
        self._window_title = window_title
        self._is_setup = False
        
    @property
    def window (self):
        return self._window
    
    def setup (self):
        self.setup_conf_defaults ()
        self.setup_conf_signals ()
        self.setup_window ()
        self._is_setup = True
    
    def setup_window (self):
        self._window = sf.RenderWindow (
            sf.VideoMode (self._conf.child ('width').value,
                          self._conf.child ('height').value,
                          self._conf.child ('bpp').value),
            self._window_title,
            sf.Style.Fullscreen if self._conf.child ('full').value else 0)

        self._window.SetFramerateLimit (self._conf.child ('fps').value)
        self._window.UseVerticalSync (self._conf.child ('vsync').value)
        
    def close (self):
        if self._is_setup:
            self.disconnect_all ()
            self._window.Close ()
            del self._window
            self._is_setup = False
    
    def setup_conf_defaults (self):
        self._conf.child ('width').value  = self.DEFAULT_WIDTH
        self._conf.child ('height').value = self.DEFAULT_HEIGHT
        self._conf.child ('full').value   = self.DEFAULT_FULLSCREEN
        self._conf.child ('fps').value    = self.DEFAULT_FPS
        self._conf.child ('bpp').value    = self.DEFAULT_BPP
        self._conf.child ('vsync').value  = self.DEFAULT_VSYNCH

    def setup_conf_signals (self):
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
