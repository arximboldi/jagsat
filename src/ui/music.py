#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from core import task

import theme
import random

class MusicPlayer (task.Task):

    def __init__ (self, audio = None, playlist = None, *a, **k):
        self.audio = audio
        self.playlist = playlist or theme.background_music
        self._song_queue = list (theme.background_music)
        random.shuffle (self._song_queue)

    def play (self):
        pass

    def stop (self):
        pass

    def do_update (self):
        pass
