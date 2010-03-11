#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base.log import get_log
from base import signal

import widget

_log = get_log (__name__)


class IngameMenu (widget.HBox, object):

    def __init__ (self, *a, **k):
        super (IngameMenu, self).__init__ (*a, **k)

        self.on_quit_game  = signal.Signal ()
        self.on_close_menu = signal.Signal ()

        self.set_position_rel (0.5, 0.5)
        self.set_center_rel (0.5, 0.5)
        self.padding_left = 20

        self._but_close = widget.Button (
            self, 'Close', 'data/icon/close.png')
        self._but_save = widget.Button (
            self, 'Save', 'data/icon/save.png')
        self._but_help = widget.Button (
            self, 'Help', 'data/icon/help.png')
        self._but_quit = widget.Button (
            self, 'Quit', 'data/icon/quit.png')

        self._but_close.on_click += lambda ev: self.on_close_menu ()
        self._but_help.on_click += self.show_help
        self._but_save.on_click += self.show_save
        self._but_quit.on_click += lambda ev: self.on_quit_game ()
        
    def show_help (self, ev):
	_log.debug ('Showing the help...')
        
    def show_save (self, ev):
        _log.debug ("Saving the game...")

