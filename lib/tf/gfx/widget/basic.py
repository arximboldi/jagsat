# -*- coding: utf-8 -*-
#
# This file is copyright Tribeflame Oy, 2009.
#

from tf.gfx import ui
from PySFML import sf
import math
import sets
from tf.gfx import uirotation
from tf.gfx import uiactions
import re
import os
import random

from PySFML import sf

from tf import signalslot


class PlayerPositionMarker(ui.Image):
    """This is a small marker symbol at the edge of the screen
    from which the user can control the direction in which the user
    interface is displayed."""

    def __init__(self,
                 parent,
                 uirotationnotifier,
                 realplayerinfo,
                 marker_img_filename,
                 markershadow_img_filename):
        ui.Image.__init__(self, parent, marker_img_filename)
        self.uirotationnotifier = uirotationnotifier
        self.set_enable_hitting(True)
        self.set_center(self._get_width() - 5,
                        self._get_height() / 2.0)

        self.shadow = ui.Image(parent, markershadow_img_filename)
        self.shadow.set_center(self._get_width() - 5,
                               self._get_height() / 2.0)

        self.shadow.set_visible(False)
        self.sticky_angles = sets.Set()

    def _calc_sticky_angles(self, window):
        self.sticky_angles = sets.Set([0, 90, 180, 270, 360])
        ang = math.degrees(math.atan2(window.window.GetHeight(),
                                      window.window.GetWidth()))
        self.sticky_angles.add(90 - ang)
        self.sticky_angles.add(90 + ang)
        self.sticky_angles.add(270 + ang)
        self.sticky_angles.add(270 - ang)

    def set_focus(self, realplayerinfo, window):
        self.realplayerinfo = realplayerinfo
        self.window = window
        self._calc_sticky_angles(self.window)
        if self.realplayerinfo.rotate_ui:
            x, y = self.rotate(self.realplayerinfo.rotation)
            self.set_position(x, y)
            self.SetRotation(-self.realplayerinfo.rotation - 90)
            self.uirotationnotifier.notify_all_ui(self.realplayerinfo.rotation)

    def rotate(self, rotation):
        width = self.window.window.GetWidth()
        height = self.window.window.GetHeight()
        hw = width / 2
        hh = height / 2
        rot = rotation
        rot += 90 # XXX ???
        rot = rot % 360
        r = math.radians(rot)
        t = math.tan(r)

        # I don't understand this, but it seems to work

        if rot > 270 or rot <= 90:
            y = hh + t * hw
            x = width - 1
            if y <= 0:
                y = 0
                x = hw - hh / t
            elif y >= height:
                y = height - 1
                x = hw + hh / t
        else:
            y = height - (hh + t * hw)
            x = 0
            if y <= 0:
                y = 0
                x = hw - hh / t
            elif y >= height:
                y = height - 1
                x = hw + hh / t

        return x, y

    def start_pan(self, event):
        print "start player marker panning"
        self.shadow.set_visible(True)
        x, y = self.GetPosition()
        self.shadow.set_position(x, y)
        self.shadow.SetRotation(self.GetRotation())

    def do_pan(self, event):
        x = event[0]
        y = event[1]
        angle = self._calc(x, y)
        x, y = self.rotate(angle)
        self.shadow.set_position(x, y)
        self.shadow.SetRotation(-angle - 90)

    def _calc(self, x, y):
        width = self.window.window.GetWidth()
        height = self.window.window.GetHeight()
        hw = width / 2
        hh = height / 2
        dx = x - hw
        dy = - (y - hh)
        angle = -math.degrees(math.atan2(dy, dx))
        angle += 270 #??
        angle = angle % 360
        assert angle >= 0
        assert angle < 360

        STICKY_ANGLE = 3
        for i in self.sticky_angles:
            da = abs(angle - i)
            if da < STICKY_ANGLE:
                angle = i
                break
        angle = angle % 360
        return angle

    def end_pan(self, event):
        if self.realplayerinfo.rotate_ui:
            angle = self._calc(event[0], event[1])
            self.realplayerinfo.rotation = angle
            self.set_focus(self.realplayerinfo, self.window)

        self.shadow.set_visible(False)


def create_player_position_marker(parent,
                                  uirotationnotifier,
                                  realplayerinfo,
                                  img_name,
                                  imgshadow_name):
    c = PlayerPositionMarker(parent,
                             uirotationnotifier,
                             realplayerinfo,
                             img_name,
                             imgshadow_name)
    return c


class _Key(ui.Image):

    def __init__(self, parent, fname, keyinfo):
        ui.Image.__init__(self, parent, fname)
        #self.set_center_rel(ui.CENTER)
        self.set_enable_hitting(True)
        self.keyinfo = keyinfo
        self.signal_click.add(lambda e: self.parent._hit_key(self))
#    def user_hit(self, gameloop, x, y):
#        self.parent._hit_key(self)


def get_dir_of_python_file(file):
    dir = re.sub("\\" + os.sep + "[^\\" + os.sep + "]+$", "", file)
    return dir


class _KeyboardConfig:

    def __init__(self, parent):
        self.keys = set()

        self.is_shifted = False

        dir = get_dir_of_python_file(__file__)

        start_x = 30
        start_y = 90

        x = start_x
        y = start_y

        key_unit_width = 50
        key_unit_height = 50

        for i in [
#{ "key": "!", "pos": (0.0, 0.0) },
#{ "key": "?", },
#{ "key": ".", },
#{ "key": ",", },
#{ "key": ":", },
#{ "key": ";", },
#{ "key": "+", },
#{ "key": "-", },
#{ "key": "_", },
#{ "key": "\"", },
#{ "key": "#", },
#{ "key": "$", },
#{ "key": "%", },
#{ "key": "&", },
#{ "key": "/", },
#{ "key": "(", },
#{ "key": ")", },
#{ "key": "=", },
#{ "key": "<", "pos": (0.0, 0.0) },
#{ "key": ">", },
#{ "key": "{", },
#{ "key": "}", },
#{ "key": "[", },
#{ "key": "]", },
#{ "key": "", },
#{ "key": "", },
#{ "key": "", },
#{ "key": "", },
# + accented chars
# + Other european chars
# + others?

{"key": "1", "shift": "!", "pos": (1.0, 0.0)},
{"key": "2", "shift": "\""},
{"key": "3", "shift": "#"},
{"key": "5", "shift": "%"},
{"key": "6", "shift": "&"},
{"key": "7", "shift": "/"},
{"key": "8", "shift": "("},
{"key": "9", "shift": ")"},
{"key": "0", "shift": "="},
{"key": "<-", "extra": "DEL", "pos": (13, 0)},

{"key": "q", "shift": "Q", "pos": (1.5, 1.0)},
{"key": "w", "shift": "W"},
{"key": "e", "shift": "E"},
{"key": "r", "shift": "R"},
{"key": "t", "shift": "T"},
{"key": "y", "shift": "Y"},
{"key": "u", "shift": "U"},
{"key": "i", "shift": "I"},
{"key": "o", "shift": "O"},
{"key": "p", "shift": "P"},

{"key": "a", "shift": "A", "pos": (2, 2.0)},
{"key": "s", "shift": "S"},
{"key": "d", "shift": "D"},
{"key": "f", "shift": "F"},
{"key": "g", "shift": "G"},
{"key": "h", "shift": "H"},
{"key": "j", "shift": "J"},
{"key": "k", "shift": "K"},
{"key": "l", "shift": "L"},
{"key": "<-/", "extra": "ENTER", "pos": (13, 1)},

{"key": "=^=", "extra": "SHIFTLEFT", "pos": (0.5, 3.0)},
{"key": "<", "shift": ">"},
{"key": "z", "shift": "Z"},
{"key": "x", "shift": "X"},
{"key": "c", "shift": "C"},
{"key": "v", "shift": "V"},
{"key": "b", "shift": "B"},
{"key": "n", "shift": "N"},
{"key": "m", "shift": "M"},
{"key": "=^=", "extra": "SHIFTRIGHT"},
]:
            i["key"] = unicode(i["key"], "UTF-8")
            if "shift" in i:
                i["shift"] = unicode(i["shift"], "UTF-8")

            fname = None

            if "extra" in i:
                e = i["extra"]
                if False:
                    pass
                elif e == "DEL":
                    fname = dir + os.sep + "key_del.png"
                elif e == "ENTER":
                    fname = dir + os.sep + "key_return.png"
                elif e == "SHIFTLEFT":
                    fname = dir + os.sep + "key_shift_left.png"
                elif e == "SHIFTRIGHT":
                    fname = dir + os.sep + "key_shift_right.png"
                else:
                    # Key not supported
                    print "KEY", e
                    assert 0
            else:
                fname = dir + os.sep + "one_key.png"
            u = _Key(None, fname, i)

            if "pos" in i:
                x = i["pos"][0] * key_unit_width + start_x
                y = i["pos"][1] * key_unit_height + start_y
            u.SetPosition(x, y)
            # XXX render this to the blackbox instead...
            parent.add_back_child(u)
            self.keys.add(u)

            if "extra" not in i:
                k = ui.String(None, i["key"])
                yfuzz = -4
                xfuzz = 0
                k.SetPosition(u.GetPosition()[0] + u._get_width()/2.0 - \
                                  k._get_width()/2.0 + xfuzz,
                              u.GetPosition()[1] + u._get_height()/2.0 - \
                                  k._get_height()/2.0 + yfuzz)
                parent.add_child(k)
                u.keysprite = k

            x += key_unit_width
            if x > parent.width - key_unit_width:
                x = start_x
                y += key_unit_height


class Keyboard(ui.FreeformContainer):

    def __init__(self, parent):
        ui.FreeformContainer.__init__(self, parent)
        self.width = 750
        self.height = 300

        self.set_position_rel(ui.CENTER)
        self.set_center_rel(ui.CENTER)

        # In letters
        self.maxlength = 15

        blackbox = ui.RoundedRectangle(None,
                                       0, 0,
                                       self.width, self.height,
                                       15,
                                       sf.Color(0, 174, 209, 255),
                                       sf.Color(0, 151, 195, 255),
                                       2)
        self.set_enable_hitting(True)
        self.add_back_child(blackbox)

        whitestr = ui.String(None,
                             u"")
        whitebox = ui.RoundedRectangle(None,
                                       170, 30,
                                       300, whitestr._get_height() + 45,
                                       10,
                                       sf.Color(0, 255, 255, 128),
                                       sf.Color(0, 150, 150, 128), 1)
        whitestr.SetPosition(5, 0)
        self.add_child(whitebox)
        whitebox.add_child(whitestr)

        self.whitestr = whitestr

        self.kconfig = _KeyboardConfig(self)

        self.signal_text_entered = signalslot.Signal("text_entered")
        self.signal_text_failed = signalslot.Signal("text_failed")

    def reinitialize(self):
        uiactions.move_in(self, 50)
        self.signal_text_entered.remove_all()
        self.signal_text_failed.remove_all()

    def set_max_length(self, mx):
        # In letters
        self.maxlength = mx

    def get_max_length(self):
        return self.maxlength

    def _hit_key(self, key):
        keyinfo = key.keyinfo
        s = self.whitestr.get_string()
        if "extra" in keyinfo:
            e = keyinfo["extra"]
            if 0:
                pass
            elif e == "DEL":
                s = s[:-1]
            elif e == "ENTER":
                # Accepts the string and sends it no observers
                e = signalslot.Event("text_entered",
                                     text = self.whitestr.get_string())
                self.signal_text_entered.call(e)

                uiactions.move_out(self, 50)
            elif e == "SHIFTLEFT" or e == "SHIFTRIGHT":
                self.kconfig.is_shifted ^= True
                value = "key"
                if self.kconfig.is_shifted:
                    value = "shift"
                for key in self.kconfig.keys:
                    if "extra" in key.keyinfo:
                        e = key.keyinfo["extra"]
                        if e == "SHIFTLEFT" or e == "SHIFTRIGHT":
                            if self.kconfig.is_shifted:
                                c = sf.Color(200, 200, 200, 255)
                            else:
                                c = sf.Color(255, 255, 255, 255)
                            key._sprite.SetColor(c)
                        continue
                    if value in key.keyinfo:
                        # BUG this should be automatic
                        u = key
                        k = u.keysprite
                        yfuzz = -4
                        xfuzz = 0
                        k.set_string(key.keyinfo[value])
                        k.SetPosition(u.GetPosition()[0] + \
                                          u._get_width()/2.0 - \
                                          k._get_width()/2.0 + xfuzz,
                                      u.GetPosition()[1] + \
                                          u._get_height()/2.0 - \
                                          k._get_height()/2.0 + yfuzz)
            else:
                assert 0
        else:
            if len(s) >= self.maxlength:
                return

            s += key.keysprite.get_string()

        self.whitestr.set_string(s)

    def show_keyboard_and_inject_answer(self,
                                        originstr,
                                        targetcallback_on_success,
                                        targetcallback_on_failure):
        self.reinitialize()
        self.whitestr.set_string(originstr)
        self.set_visible(True)
        self.signal_text_entered.add(targetcallback_on_success)
        self.signal_text_failed.add(targetcallback_on_failure)

    def show_keyboard_and_inject_answer_string(self,
                                               string):
        self.reinitialize()
        self.whitestr.set_string(string.get_string())
        self.set_visible(True)
        self.signal_text_entered.add(lambda e: string.set_string(e.text))
