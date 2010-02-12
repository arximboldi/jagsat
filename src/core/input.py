#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
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

