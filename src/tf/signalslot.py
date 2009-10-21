#
# This file is copyright Tribeflame Oy, 2009.
#
"""
Signals form the basic Event information passing primitive.
"""
import weakref


__all__ = [
'Signal',
'forward_signal',
'disable_signal',
'disable_signal_callback',
'disable_signals_callback',
'Event']


class Signal:
    """
    A Signal is a generic Subject-Observer pattern which transmits
    Event objects to interested parties.

    A Signal is first created by the object that wishes to transmit
    information.

    Then, interested parties can register to it by calling its add
    method.

    Upon certain actions in this object, the signal is triggered by
    calling its call method by the object itself. The Event object that
    is sent contains information that the registered parties can handle.

    Depending on the Event, there are other attributes available.

    """

    def __init__(self, name):
        self.name = name
        self.targets = set()
        self._is_enabled = True

    def __repr__(self):
        s = "Tribeflame signal %s with %d targets" % \
            (self.name, len(self.targets))
        return s

    def set_enabled(self, b):
        old = self._is_enabled
        self._is_enabled = b
        return old

    def disable(self):
        print "Disabling", self.name
        return self.set_enabled(False)

    def enable(self):
        return self.set_enabled(True)

    def is_enabled(self):
        return self._is_enabled

    def add(self, target):
        """
        Add a target callable to this signal.
        """
        self.targets.add(target)

    def remove(self, target):
        """
        Remove a target callable from this signal.
        """
        self.targets.remove(target)

    def remove_all(self):
        """
        Removes all callables from this signal. In other words,
        calling this signal will have no effect.
        """
        self.targets.clear()

    def call(self, ev):
        """
        Call this signal by propagating the @Event ev to all the
        callables of the signal.
        """
        if not self._is_enabled:
            return
        assert isinstance(ev, Event)

        # This happens when forwarding
        if hasattr(ev, "signal"):
            try:
                ev.signal_chain
            except AttributeError:
                ev.signal_chain = []
            ev.signal_chain.append(ev.signal)

        ev.signal = self
        for target in self.targets:
            target(ev)


def forward_signal(signal1, signal2):
    """
    Forwards any @Event objects that are sent on @signal1 to @signal2.
    """
    signal1.add(signal2.call)


def disable_signal_callback(signal):
    """
    Creates a callable that will disable @signal. This is used to
    disable e.g. the user interface after the user has clicked on a
    button.

    See also disable_signal_callbacks
    """
    # This is a bit cumbersome, but the interface is similar
    # to disable_signals_callback

    def d(e):
        # BUG disable signal_chain?
        assert signal == e.signal
        e.signal.disable()
    return d


def disable_signals_callback(signals):
    """
    Creates a callable that will disable all signals in @signals.
    This is used to disable e.g. the user interface after the user has
    clicked on a button.
    """

    def d(e):
        for s in signals:
            s.disable()
    return d


class Event:
    """
    An Event object contains basically nothing but the parameters
    that were passed to it during construction.
    """

    def __init__(self, name, **kwargs):
        self._tribeflame_synthetic = False
        self._tribeflame_name = name
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_event_name(self):
        return self._tribeflame_name

    def get_signal(self):
        return self._signal
