#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base.log   import get_log
from core.state import State
from ui.music   import MusicPlayer

_log = get_log (__name__)

test_playlist = [ 'data/sfx/clicks/failed_click.wav',
                  'data/sfx/clicks/failed_click2.wav',
                  'data/sfx/clicks/successful_click.wav',
                  'data/sfx/clicks/successful_click2.wav' ]

class RootState (State):

    def do_setup (self, *a, **k):
        super (RootState, self).do_setup (*a, **k)
        self._music = self.tasks.add (MusicPlayer (self.manager.system.audio))
        self._music.play ()

        self.manager.enter_state ('main_menu')

    def do_unsink (self, *a, **k):
        self.manager.leave_state ()

        
