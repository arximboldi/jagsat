#
# This file is copyright Tribeflame Oy, 2009.
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
