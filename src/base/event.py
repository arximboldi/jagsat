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

from log import get_log
from signal import Signal, signal
from sender import Sender, Receiver

"""
This module defines the EventManager class for managing a dynamic
group of signals with forwarding capabilities.
"""

_log = get_log (__name__)

class EventManager (Sender, Receiver):

    quiet = False
    
    def __init__ (self):
        super (EventManager, self).__init__ ()
        self._events = {}
        self.on_any_event = Signal ()
        
    def notify (self, name, *args, **kw):
        if not self.quiet:
            if name in self._events: 
                self._events [name].notify (*args, **kw)
            else:
                self.send (name, *args, **kw)

    receive = notify

    def send (self, name, *a, **k):
        self.on_any_event.notify (name, a, k)
        super (EventManager, self).send (name, *a, **k)
    
    def event (self, name):
        if name in self._events:
            return self._events [name]

        signal = Signal ()
        signal += lambda *a, **k: self.send (name, *a, **k)
        self._events [name] = signal
        return signal

    def clear_events (self, name = None):
        if name:
            del self._events [name]
        else:
            self._events.clear ()
