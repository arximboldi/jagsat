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
from base.error import LoggableError

from ui.ingame_menu import IngameMenu
from game import GameSubstate

from model import worldio
from functools import partial

import os.path

_log = get_log (__name__)


class IngameMenuState (GameSubstate):

    def do_release (self):
        super (IngameMenuState, self).do_release ()
        self._ingame_menu.remove_myself ()
        self.root.disable_bg ()
    
    def do_setup (self, *a, **k):
        super (IngameMenuState, self).do_setup (*a, **k)
        self._ingame_menu = IngameMenu (self.root.ui_layer)

        self._ingame_menu.on_quit_game  += self.quit_state
        self._ingame_menu.on_close_menu += self.manager.leave_state
        self._ingame_menu.on_save_game  += partial (self.manager.change_state,
                                                    LoadGameState)
        self._ingame_menu.on_show_help  += partial (
            self.manager.change_state,
            'message', message =
            'Not implemented :(\n'
            '%30%Sorry for the inconvenience, '
            'we will try to do it soon!')
        self.root.enable_bg ()


class LoadGameState (GameSubstate):

    def do_setup (self, *a, **k):
        super (LoadGameState, self).do_setup (*a, **k)

        savename = self.find_valid_name (self.game.world.name)
        self.manager.enter_state (
            'input_dialog',
            message = 'Game save name:',
            input_text = savename)

    def do_unsink (self,
                   dialog_yes = None,
                   dialog_no  = None,
                   dialog_input = None, *a, **k):
        super (LoadGameState, self).do_unsink (*a, **k)

        if dialog_input:
            if self.is_valid_name (dialog_input):
                self.save_game_and_leave (dialog_input)
            else:
                self.manager.enter_state (
                    'yes_no_dialog', message =
                    "There exists a game save called: %s.\n"
                    "Do you want to overwrite it?" % dialog_input,
                    yes_ret = dialog_input)

        if dialog_yes:
            self.save_game_and_leave (dialog_yes)
    
    def save_game_and_leave (self, name):
        fname = self.get_save_file (name)
        try:
            worldio.save_game (self.game.world, fname)
            self.manager.leave_state ()
        except LoggableError, e:
            e.log ()
            self.manager.change_state ('message', message =
                                       'Error while saving game :(')
    
    def get_save_file (self, name):
        return os.path.join (self.manager.get_save_folder (),
                             name + '.' + worldio.save_game_ext)
    
    def is_valid_name (self, name):
        fname = self.get_save_file (name)
        return not os.path.exists (fname)
    
    def find_valid_name (self, name_base):
        new_name = name_base
        i = 1
        while not self.is_valid_name (new_name):
            new_name = name_base + (' %i' % i)
            i += 1
        return new_name

