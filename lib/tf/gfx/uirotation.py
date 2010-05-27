#
#  Copyright (C) 2009 TribleFlame Oy
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
