#
#  Copyright (C) 2009, 2010 JAGSAT Development Team (see below)
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
#  JAGSAT Development Team is:
#    - Juan Pedro Bolivar Puente
#    - Alberto Villegas Erce
#    - Guillem Medina
#    - Sarah Lindstrom
#    - Aksel Junkkila
#    - Thomas Forss
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
