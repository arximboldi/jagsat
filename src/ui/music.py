#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base.log  import get_log
from core      import task
from itertools import cycle

import theme
import random

from PySFML import sf

_log = get_log (__name__)

class state:
    idle, playing = range (0, 2)

class MusicPlayer (task.Task):

    def __init__ (self,
                  audio    = None,
                  playlist = theme.background_music,
                  shuffle  = True,
                  loop     = True,
                  *a, **k):
        super (MusicPlayer, self).__init__ (*a, **k)

        self.audio    = audio
        self.playlist = playlist or theme.background_music
        self.shuffle  = shuffle
        self.loop     = loop

        self._queue   = []
        self._iter    = None
        self._current = None
        self._music   = None
        self._state   = state.idle

    @property
    def current (self):
        return self._current

    @property
    def state (self):
        return self._state
    
    def play (self):
        if self._state == state.playing:
            self.stop ()

        self._queue = list (self.playlist)
        if self.shuffle:
            random.shuffle (self._queue)

        self._iter = iter (self._queue)
        if self.loop:
            self._iter = cycle (self._iter)
        
        self.jump_next ()

    def jump_next (self):
        try:
            self._current = self._iter.next ()
            self.play_file (self._current)
        except StopIteration:
            self.stop ()

    def play_file (self, file):
        if self._music:
            self._music.Stop ()
            
        _log.debug ('Playing file: ' + file)
        self._music = sf.Music ()
        self._music.OpenFromFile (file)
        self._music.Play ()
        self._state = state.playing
        
    def stop (self):
        self._music.Stop ()
        self._music = None
    
    def do_update (self, timer):
        super (MusicPlayer, self).do_update (timer)
        if self._music and self._music.GetStatus () == sf.Sound.Stopped:
            self.jump_next ()
