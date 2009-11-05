#
#  Copyright (C) 2009 Juan Pedro Bolivar Puente, Alberto Villegas Erce
#  
#  This file is part of Pigeoncide.
#
#  Pigeoncide is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  
#  Pigeoncide is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Provides some error base clases to be used in all the project.
"""

from log import *

class LoggableError (Exception):
    """
    Prueba
    """
    
    LEVEL      = LOG_ERROR
    MESSAGE    = ""
    ERROR_CODE = -1

    def __init__ (self, *a, **k):
        self._message = k.pop ('message', self.MESSAGE)
        self.level   = k.pop ('level', self.LEVEL)
        super (Exception, self).__init__ (*a, **k)
    
    def log (self, level = None, msg = None):
        if msg is None:
            if self.message is None:
                msg = self.MESSAGE
            else:
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
