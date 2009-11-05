#
# This file is copyright Tribeflame Oy, 2009.
#
from __future__ import with_statement

from tf.gfx import ui
import tf.arch
from PySFML import sf
import os
import tf
import re
import time
import sys
import gc
import subprocess

from tf.gfx import uiactions

import types


class FramesPerSecond(ui.String):
    """Adds a Frames-per-second counter at the topright corner.
    Used for debugging."""

    EVERY_NTH = 10

    def __init__(self, parent, length = 10):
        """@parent is the layer where this object is added."""
        ui.String.__init__(self, parent, u"FPS:")
        self.fps = [0.0] * length
        self.idx = 0
        self.sum = 0
        self.clock = sf.Clock()
        self._sprite.SetSize(12)
        self.set_center_rel(1.0, 0.0)
        self.set_position_rel(0.97, 0.03)

        self.ticks = 0

        self.add_action(uiactions.CallInfinitely0(self.tick_once))

    def calc_frame_rate(self, fps):
        self.sum -= self.fps[self.idx]
        self.fps[self.idx] = fps
        self.sum += fps
        self.idx = (self.idx + 1) % len(self.fps)
        return self.sum / len(self.fps)

    def tick_once(self):
        self.ticks += 1
        if self.ticks < FramesPerSecond.EVERY_NTH:
            return
        self.ticks = 0

        fps = 1.0 / self.clock.GetElapsedTime()
        fps *= FramesPerSecond.EVERY_NTH
        fps_avg = self.calc_frame_rate(fps)
        self.set_string(u"FPS: %.1f" % fps_avg)
        self.clock.Reset()


_win32_cpu_usage = None


class CpuPerSecond(ui.String):
    """
    Adds a total CPU usage counter at the topright corner.

    Used for debugging.
    """

    EVERY_NTH = 50

    def __init__(self, parent, length = 10):
        """@parent is the layer where this object is added."""
        ui.String.__init__(self, parent, u"CPU:")
        self.values = [0.0] * length
        self.idx = 0
        self.sum = 0
        self.clock = sf.Clock()
        self._sprite.SetSize(12)
        self.set_center_rel(1.0, 0.0)
        self.set_position_rel(0.97, 0.05)

        self.ticks = 0

        self.add_action(uiactions.CallInfinitely0(self.tick_once))

    def calc_cpu_usage(self, val):
        self.sum -= self.values[self.idx]
        self.values[self.idx] = val
        self.sum += val
        self.idx = (self.idx + 1) % len(self.values)
        return self.sum / len(self.values)

    def get_average_cpu_usage(self):
        usage = tf.arch.get_cpu_usage()
        return self.calc_cpu_usage(usage)

    def tick_once(self):
        self.ticks += 1
        if self.ticks < CpuPerSecond.EVERY_NTH:
            return
        self.ticks = 0

        avg = self.get_average_cpu_usage()

        self.set_string(u"CPU: %2.f%%" % avg)
        self.clock.Reset()


def get_dir_of_python_file(file):
    dir = re.sub("\\" + os.sep + "[^\\" + os.sep + "]+$", "", file)
    return dir


def _display_error(layer, errortext):
    t = ui.MultiLineString(layer,
                           errortext, Size = 15.0)
    t.SetPosition(10, 50)
    t.set_enable_hitting(True)
    t.signal_click.add(lambda e: e.component.remove_myself())


class _Error(ui.Image):

    def __init__(self, parent, exception_string):
        dir = get_dir_of_python_file(__file__)
        ui.Image.__init__(self,
                          parent,
                          dir + os.sep + "debug_error.png")
        self.set_center_rel(0.5, 0)
        self.exception_component = None
        self.signal_click.add(lambda e:
                                  _display_error(self.get_layer(),
                                                 exception_string))
        self.signal_click.add(
            lambda e:
                self.add_action_sequence([uiactions.FadeOut(),
                                          uiactions.RemoveMyself()]))


def create_error(exception_string, layer):
    if not tf.DEBUG:
        return
    print "tf: Exception:", exception_string
    e = _Error(layer, exception_string)
    errors = [obj for obj in layer.objects if isinstance(obj, _Error)]
    x = max([e.GetPosition()[0] for e in errors])
    e.set_position(x + e._get_width() + 5, 10)
    e.set_enable_hitting(True)


info = None


def count_children(o, level):
    count = len(o.children)
    count += len(o.children_back)
    active_actions = len(o.active_actions)
    n_actions = len(o.actions)
    spaces = " " * level
    vis = " (visible)"
    if not o._visible:
        vis = " (hidden)"
    print spaces + str(o) + vis
    if o.children_back:
        print spaces + "Children back:"
        for i in o.children_back:
            c, a, n = count_children(i, level + 1)
            count += c
            active_actions += a
            n_actions += n
    if o.children:
        print spaces + "Children:"
        for i in o.children:
            c, a, n = count_children(i, level + 1)
            count += c
            active_actions += a
            n_actions += n
    #print spaces "-"
    return count, active_actions, n_actions


def toggle_info(window, layer = None):
    global info
    if info:
        info.remove_myself()
        info = None
        return

    if not layer:
        layer = window.views[-1].layers[-1]
    s = u""
    s += u"Internal generic information for the current game\n"
    s += u"Views:\n"
    for view in window.views:
        s += u"- " + str(view) + "\n"
        for lr in view.layers:
            s += u"  - Layer" + str(lr) + "\n"
            print ""
            vis = " (visible)"
            if not lr._visible:
                vis = " (hidden)"
            print "Layer: " + str(lr) + vis
            children = 0
            active_actions = 0
            n_actions = 0
            for obj in lr.objects:
                c, a, n = count_children(obj, 0)
                children += c
                active_actions += a
                n_actions += n
            s += "       Children: %d\n" % children
            s += "       Active actions: %d\n" % active_actions
            s += "       Total amount of actions: %d\n" % n_actions
    info = ui.MultiLineString(layer, s, Size = 12.0)


def create_screenshot(window, name):
    lc = time.localtime()
    f = "%s-screenshot-%04d-%02d-%02d-%02d:%02d:%02d.png" % \
        (name, lc[0], lc[1], lc[2], lc[3], lc[4], lc[5])
    i = sf.Image()
    ret = i.CopyScreen(window.window)
    assert ret
    # SFML BUG http://www.sfml-dev.org/todo/index.php?do=details&task_id=68
    # Image is y-flipped.
    ret = i.SaveToFile(f)
    assert ret

    try:
        subprocess.Popen(["convert",
                          "-flip",
                          f,
                          f])
    except OSError:
        # Probably on Windows, or a unix without the convert program.
        pass


def dump_information(window):
    gc.collect()
    objs = gc.get_objects()
    dumpfilename = time.strftime("dump-%Y-%m-%d-%H:%M:%S")
    with file(dumpfilename, "wb") as f:
        f.write("DUMP INFORMATION FOR OBJECTS\n")
        n_objs = 0
        for obj in objs:
            if type(obj) == types.InstanceType:
                n_objs += 1
                f.write("***" + repr(obj) + "\n")
                f.write("CLASS" + repr(obj.__class__) + "\n")
            elif type(obj) != types.ClassType and \
                    type(obj) != types.TypeType and \
                    type(type(obj)) == types.TypeType:
                n_objs += 1
                f.write("***" + repr(obj) + "\n")
                f.write("CLASS" + repr(obj.__class__) + "\n")

        f.write("TOTAL AMOUNT OF OBJECTS: %d.\n" % n_objs)
