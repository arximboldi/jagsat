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

from PySFML import sf
from tf.behavior import keyboard

from base.signal import Signal, weak_slot

class _key (object):
    def __init__ (self):
        for key, val in sf.Key.__dict__.iteritems ():
            if key.find ('__', 0, 2) != 0:
                self.__dict__ [key.lower ()] = val

key = _key ()

class mod (object):
    none    = 0
    control = 1
    shift   = 1 << 1
    alt     = 1 << 2

class KeyboardManager (object):

    def __init__ (self, *a, **k):
        super (KeyboardManager, self).__init__ (*a, **k)
        self._key_map = {}

    def clear (self):
        for s in self._key_map.itervalues ():
            s.clear ()
        self._key_map.clear ()

    def get_key (self, k, m = mod.none):
        try:
            sig = self._key_map [(k, m)]
        except KeyError:
            sig = Signal ()
            self._key_map [(k, m)] = sig
        return sig
    
    @weak_slot
    def on_sfml_event (self, ev):
        if ev.ev.Type == sf.Event.KeyPressed:
            k = ev.ev.Key.Code
            m = mod.none
            if ev.ev.Key.Alt:     m |= mod.alt
            if ev.ev.Key.Control: m |= mod.control
            if ev.ev.Key.Shift:   m |= mod.shift
            try:
                sig = self._key_map [(k, m)]
                sig (k, m)
                if sig.count == 0:
                    del self._key_map [(k, m)]
            except KeyError:
                pass

