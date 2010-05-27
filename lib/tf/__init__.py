#
#  Copyright (C) 2009 TribleFlame Oy
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

"""
The Tribeflame toolkit documentation.

Important parts:

tf.gfx.ui - Anything visible on the screen

tf.gfx.uiactions - Actions perform changes to the user interface elements.

tf.behavior.gameloop - The game loop consists of various managers for
statemachines, audio, keybindings, timers, etc.

tf.behavior.sm - Statemachine interfaces

tf.behavior.eventloop - Main event loop that drives everything.

tf.behavior.soundfile - Audio management.

tf.globalization - For internationalization. You can initially ignore this.

tf.arch - Ignore

tf.parsers - Ignore
"""


__all__ = [
'DEBUG',
'PRODUCTION',
'TribeflameException']

DEBUG = True
PRODUCTION = True

import sys


def _internal_is_asus_eee_platform():
    if sys.platform == "win32":
        return True
    return False


def _internal_is_production_linux():
    return not _internal_is_asus_eee_platform() and PRODUCTION


def _internal_is_developer_linux():
    return not _internal_is_asus_eee_platform() and not PRODUCTION


class TribeflameException(Exception):
    pass
