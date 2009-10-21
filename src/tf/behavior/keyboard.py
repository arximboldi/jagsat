#
# This file is copyright Tribeflame Oy, 2009.
#
from tf import signalslot


class KeyShortcut(object):

    def __init__(self, keycode, **kwargs):
        self.keycode = keycode
        self.requires_alt = False
        self.requires_ctrl = False
        self.requires_shift = False
        self.__dict__.update(kwargs)


class KeyboardManager:

    def __init__(self):
        self._keyboard_shortcuts = {}

    def create_keyboard_shortcut(self,
                                 widget,
                                 keyshortcut,
                                 func):
        if isinstance(keyshortcut, long):
            keyshortcut = KeyShortcut(keyshortcut)

        k = (keyshortcut.keycode,
             keyshortcut.requires_alt,
             keyshortcut.requires_ctrl,
             keyshortcut.requires_shift)
        try:
            self._keyboard_shortcuts[k].append(func)
        except KeyError:
            self._keyboard_shortcuts[k] = [func]

        print "Added shortcut for", k
        if widget:
            widget._keyboard_shortcuts.append((k, func))

    def call_key(self,
                 keycode,
                 has_alt,
                 has_ctrl,
                 has_shift):
        k = (keycode,
             has_alt,
             has_ctrl,
             has_shift)
        #print "K", k
        #print self._keyboard_shortcuts
        if k not in self._keyboard_shortcuts \
                or len(self._keyboard_shortcuts[k]) == 0:
            print "tf: no shortcut on key", k
            return

        e = signalslot.Event("KeypressEvent", key=keycode)
        for func in self._keyboard_shortcuts[k]:
            func(e)

    def remove_keyboard_shortcut(self,
                                 widget,
                                 keyshortcut,
                                 func):
        if isinstance(keyshortcut, tuple):
            k = keyshortcut
        else:
            k = (keyshortcut.keycode,
                 keyshortcut.requires_alt,
                 keyshortcut.requires_ctrl,
                 keyshortcut.requires_shift)
        if k not in self._keyboard_shortcuts \
                or func not in self._keyboard_shortcuts[k]:
            print "tf: Error, no", func, "shortcut on key", k, ",can't remove."
            return
        self._keyboard_shortcuts[k].remove(func)
        if widget:
            widget._keyboard_shortcuts.remove((k, func))
