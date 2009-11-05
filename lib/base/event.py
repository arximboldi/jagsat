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

from log import get_log
from signal import Signal
from sender import Sender, Receiver

"""
This module defines the EventManager class for managing a dynamic
group of signals with forwarding capabilities.
"""

_log = get_log (__name__)

class EventManager (Sender, Receiver):

    def __init__ (self):
        super (EventManager, self).__init__ ()
        self._events = {}
        self.quiet = False
        
    def notify (self, name, *args, **kw):
        if not self.quiet:
            if name in self._events: 
                self._events [name].notify (*args, **kw)
            else:
                self.send (name, *args, **kw)

    receive = notify
    
    def event (self, name):
        if name in self._events:
            return self._events [name]

        _log.debug ('Creating event: ' + name)
        signal = Signal ()
        signal += lambda *a, **k: self.send (name, *a, **k)
        self._events [name] = signal
        return signal

    def clear_events (self, name = None):
        if name:
            del self._events [name]
        else:
            self._events.clear ()
