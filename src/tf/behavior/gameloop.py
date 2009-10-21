#
# This file is copyright Tribeflame Oy, 2009.
#
import time
import sys
import heapq
import tf
from tf.behavior import timer
from tf import signalslot
from tf.behavior import soundfile
from tf.behavior import keyboard
from tf.behavior import actions


class GameLoop:
    """
    The game loop is the main application object that controls everything.

    So far, it takes care of running the statemachines.

    In the future, it will also run all actions, sounds.
    """

    def __init__(self):
        self.running = False
        self.statemachines = []
        self.ticks = 0
        self.hertz = 60
        self.previous_frame_duration = 0
        self.time_now = 0
        self._total_freeze_time = 0
        self.time_func = time.time
        # time.clock is much more precise on win32
        if sys.platform == "win32":
            self.time_func = time.clock
        # heap
        self.timers = []

        self._audiomanager = soundfile.AudioManager()
        self._actionmanager = actions.ActionManager()
        self._keyboardmanager = keyboard.KeyboardManager()
        self.start()

#    def set_audiomanager(self, am):
#        self._audiomanager = am

#    def set_keyboardmanager(self, km):
#        self._keyboardmanager = km

    def get_audiomanager(self):
        return self._audiomanager

    def get_keyboardmanager(self):
        return self._keyboardmanager

    def get_hertz(self):
        return self.hertz

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def is_running(self):
        return self.running

    def add_statemachine(self, sm):
        """
        Add a statemachine. It will be called every frame tick.
        """
        self.statemachines.append(sm)

    def get_statemachine(self, name):
        """
        Return a statemachine by name.
        """
        x = [i for i in self.statemachines if i.name == name]
        if not x:
            print "tf: Error: Could not find statemachine by name", name, "."
            assert 0
        return x[1]

    def now(self):
        """
        Return the current game time.
        Note that this might not be the same as wall-clock time, due to
        calling the freeze method.
        """
        return self.time_now

    def get_duration_per_frame(self):
        """
        Return the ideal duration per frame, according to the given hertz.
        """
        return 1.0 / self.hertz

    def get_duration_of_previous_frame(self):
        """
        Return the actual duration of the previous frame, in seconds.
        """
        return self.previous_frame_duration

    def _call_timers(self):
        e = None
        while self.timers and self.timers[0][0] <= self.time_now:
            if e is None:
                e = signalslot.Event("TimerEvent",
                                     now = self.time_now)
            ts = heapq.heappop(self.timers)[1]
            ts.call(e)

    def freeze(self, seconds):
        """
        Freezes the gameloop for @seconds seconds. Mainly useful for debugging,
        as this freezes the whole execution.
        """
        time.sleep(seconds)
        self._total_freeze_time += seconds

    def do_game_loop(self):
        self.ticks += 1

        t = self.time_func()
        # This is so we can freeze the action
        t -= self._total_freeze_time

        self.previous_frame_duration = t - self.time_now
        self.time_now = t
        #self.previous_frame_duration = self.get_duration_per_frame()
        #self.time_now += self.get_duration_per_frame()

        self._call_timers()

        for i, sm in enumerate(self.statemachines):
            if sm._gameloop is None:
                sm._gameloop = self
                sm.start(self)

        for i, sm in enumerate(self.statemachines):
            sm.do_statemachine(self)

    def timer_after(self, seconds, once = True):
        """
        Return a signal object which is fired (called) after
        @seconds. If @once if False, the signal will be fired every @seconds
        seconds.
        """
        ts = timer.TimerSignal("TimerSignal",
                               self,
                               seconds,
                               once)
        self._add_timer(ts)
        return ts

    def _add_timer(self, ts):
        heapq.heappush(self.timers, (ts.call_time, ts))

_thegameloop = None


def get_game_loop():
    """
    Main routine to get the singleton gameloop. Before you call this
    the first time, you may place something into _thegameloop by calling
    installGameLoop() if you really know what you are doing.
    """
    global _thegameloop
    if _thegameloop is None:
        _thegameloop = GameLoop()
    return _thegameloop


def install_game_loop(gl):
    global _thegameloop
    assert _thegameloop is None
    _thegameloop = gl
