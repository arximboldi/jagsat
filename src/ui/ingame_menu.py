#
#  Copyright (C) 2009, 2010 JAGSAT Development Team (see below)
#  
#  This file is part of JAGSAT.
#  
#  JAGSAT is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  
#  JAGSAT is distributed in the hope that it will be useful,
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
from base import signal

import widget

_log = get_log (__name__)


class IngameMenu (widget.HBox, object):

    def __init__ (self, *a, **k):
        super (IngameMenu, self).__init__ (*a, **k)

        self.on_quit_game  = signal.Signal ()
        self.on_save_game  = signal.Signal ()
        self.on_close_menu = signal.Signal ()
        self.on_show_help  = signal.Signal ()

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
        self._but_help.on_click  += lambda ev: self.on_show_help ()
        self._but_save.on_click  += lambda ev: self.on_save_game ()
        self._but_quit.on_click  += lambda ev: self.on_quit_game ()
        
    def show_help (self, ev):
	_log.debug ('Showing the help...')
        
    def show_save (self, ev):
        _log.debug ("Saving the game...")

