#
# This file is copyright Tribeflame Oy, 2009.
#
from tf import signalslot


class TimerSignal(signalslot.Signal):

    def __init__(self, name, gameloop, duration, once = True):
        signalslot.Signal.__init__(self, name)
        self.duration = duration
        self.once = once
        self.gameloop = gameloop
        self.now = self.gameloop.now()
        self.call_time = self.now + self.duration
        if not self.once:

            def x(e):
                self.now += self.duration
                self.gameloop._add_timer(self)
            self.add(x)
