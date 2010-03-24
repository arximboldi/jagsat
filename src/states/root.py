#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base.util  import lazyprop
from base.log   import get_log
from core.state import State
from ui.music   import MusicPlayer
from ui         import widget

from tf.gfx import ui

_log = get_log (__name__)

test_playlist = [ 'data/sfx/clicks/failed_click.wav',
                  'data/sfx/clicks/failed_click2.wav',
                  'data/sfx/clicks/successful_click.wav',
                  'data/sfx/clicks/successful_click2.wav' ]


class RootSubstate (State):

    @lazyprop
    def root (self):
        result = self.manager.current
        while result and not isinstance (result, RootState):
            result = result.parent_state
        return result

class RootState (State):

    def do_setup (self, *a, **k):
        super (RootState, self).do_setup (*a, **k)
        self._music = self.tasks.add (MusicPlayer (self.manager.system.audio))
        self._music.play ()

        system = self.manager.system
        self.ui_layer = ui.Layer (system.view)
        self.ui_layer.zorder = 1
        
        self.ui_bg = widget.Background (self.ui_layer)
        self._ui_bg_disabled = []

        self.manager.enter_state ('main_menu')

    def do_release (self):
        super (RootState, self).do_release ()
        self.ui_bg.remove_myself ()

    def do_unsink (self, *a, **k):
        self.manager.leave_state ()
    
    def disable_bg (self):
        self._ui_bg_disabled.pop ()
        if not self._ui_bg_disabled:
            self.ui_bg.set_enable_hitting (False)
            return self.tasks.add (self.ui_bg.fade_out ())
        return self.tasks.add (lambda t: None)

    def enable_bg (self):
        # self._ui_bg_disabled.append (True)
        if len (self._ui_bg_disabled) == 0:
            self._ui_bg_disabled.append (True)
            self.ui_bg.set_enable_hitting (True)
            return self.tasks.add (self.ui_bg.fade_in ())
        return self.tasks.add (lambda t: None)
