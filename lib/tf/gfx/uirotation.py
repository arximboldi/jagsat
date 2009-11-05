#
# This file is copyright Tribeflame Oy, 2009.
#
import math
import weakref

from tf.gfx import uiactions
from tf import signalslot


def rotate_coords(x, y, degrees):
    """Rotates a pair of coordinates around (0,0) for @degrees degrees."""
    r = math.radians(degrees)
    s = math.sin(r)
    c = math.cos(r)
    return (x * c - y * s, x * s + y * c)


def rotate_coords_around_point(x, y, degrees, origin_x, origin_y):
    """Rotates a pair of coordinates around (@origin_x, @origin_y)
    for @degrees degrees."""
    r = math.radians(degrees)
    s = math.sin(r)
    c = math.cos(r)
    x -= origin_x
    y -= origin_y
    return (x * c - y * s + origin_x, x * s + y * c + origin_y)


def set_rotation(realplayerinfo, uicomponent):
    if realplayerinfo.rotate_ui:
        uicomponent.SetRotation(-realplayerinfo.rotation)


def set_position_rel_to_window(realplayerinfo,
                               uicomponent,
                               relx,
                               rely,
                               alsorotate = True):
    if realplayerinfo.rotate_ui:
        relx, rely = \
            rotate_coords_around_point(relx, rely,
                                       realplayerinfo.rotation,
                                       0.5,
                                       0.5)

    uicomponent.set_position_rel(relx, rely)
    set_rotation(realplayerinfo, uicomponent)


ROTATION_IMMEDIATELY = 0
ROTATION_SMOOTH = 1


class UINotifications(object):

    def __init__(self):
        self.signal_notifier = signalslot.Signal("UiChange")

    def register_component_for_rotation(self,
                                        component,
                                        focuschangeobj):
        self.signal_notifier.add(\
            lambda e:
                focuschangeobj.do_focus_change(component,
                                               e.rotation))

    def notify_all_ui(self, newrotation):
        self.signal_notifier.call(\
                signalslot.Event("UiRotationEvent",
                                 component = self,
                                 rotation = newrotation))


class UiRotateOnFocusChange(object):

    def do_focus_change(self, component, newrotation):
        r = component.GetRotation()
        speed = 360
        secs = uiactions.rotate_distance(r, -newrotation)[0] / speed
        act = uiactions.RotateT(secs, r, -newrotation)
        component.add_action(act)


class UiRotateOnFocusChangeImmediate(object):

    def do_focus_change(self, component, newrotation):
        component.SetRotation(-newrotation)


class UiRotateAroundWindowOnFocusChange(object):

    def __init__(self, relx, rely):
        self.relx = relx
        self.rely = rely

    def do_focus_change(self, component, newrotation):
        r = component.GetRotation()
        speed = 360
        secs = uiactions.rotate_distance(r, -newrotation)[0] / speed
        act1 = uiactions.RotateT(secs, r, -newrotation)
        act2 = uiactions.SetPositionRelativeToRotation(self.relx,
                                                       self.rely)
        component.add_parallell_actions(act1, act2)
