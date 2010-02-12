#
# Copyright (C) 2009 The JAGSAT project team.
#
# This software is in development and the distribution terms have not
# been decided yet. Therefore, its distribution outside the JAGSAT
# project team or the Project Course evalautors in Abo Akademy is
# completly forbidden without explicit permission of their authors.
#
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Provides some error base clases to be used in all the project.
"""

from log import *

class LoggableError (Exception):
    
    LEVEL      = LOG_ERROR
    MESSAGE    = ""
    ERROR_CODE = -1

    def __init__ (self, message = None, level = None,
                  *a, **k):
        super (Exception, self).__init__ (*a, **k)

        self._message = self.MESSAGE if message is None else message
        self.level    = self.LEVEL   if level   is None else level
    
    def log (self, level = None, msg = None):
        if msg is None:
            msg = self.message
        if level is None:
            level = self.level
            
        log (self.__class__.__module__, level, msg)

    def get_code (self):
        return self.ERROR_CODE

    def _get_message (self):
        return self._message

    def _set_message (self, message):
        self._message = message

    message = property (_get_message, _set_message)

class BaseError (LoggableError):
    pass
