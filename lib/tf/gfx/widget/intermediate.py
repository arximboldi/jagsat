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

import sys
from tf.gfx import ui
from PySFML import sf

import math
import tf
from tf.gfx.widget.basic import Keyboard

from tf import signalslot
from tf.gfx import uiactions
from tf.gfx import uihelp
from tf.globalization.language import _, all_languages, LanguageChangeNotifier

button_radious = 15

class Button(ui.RoundedRectangle):

    def __init__(self, parent, str, theme):
        self.theme = theme

        ui.RoundedRectangle.__init__(self,
                                     parent,
                                     0, 0,
                                     0, 0,
                                     theme.active.radius,
                                     theme.active.color,
                                     theme.active.border,
                                     theme.active.thickness)
        self.set_margin (theme.margin)
        self.set_enable_hitting(True)
        self.set_expand (True, True)

        self.add_child (str)
        # TODO: After more than one our just trying to fix this
        # library... Lets just agree on that this sucks and all the
        # widget code have to be rewriten. The layout code is
        # unnecesarily complicated and full of bugs here and there.
        str.set_position (theme.margin * 2, theme.margin * 2)

        # str.set_center_rel (0.5,
        # 0.5) str.set_position (0.5, 0.5)
        self.need_recalculate = True
        self.signal_pan.set_enabled (True)
        
    def activate(self):
        self.set_enable_hitting (True)
        self._rebuild (self.theme.active)

    def deactivate (self):
        self.set_enable_hitting (False)
        self._rebuild (self.theme.inactive)
        
    def _rebuild (self, theme):
        self.ic = theme.color
        self.oc = theme.border
        self.ot = theme.thickness
        self.radius = theme.radius
        self._recreate (self._width,
                        self._height,
                        self.radius,
                        self.ic,
                        self.oc,
                        self.ot)


class Button2(ui.RoundedRectangle):

    def __init__(self, parent, str, active_color, inactive_color,
                 bordercolor, thickness):
        ui.RoundedRectangle.__init__(self,
                                     parent,
                                     0, 0,
                                     str._get_width() + 4,
                                     str._get_height() + 4,
                                     6,
                                     active_color,
                                     bordercolor,
                                     thickness)
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.set_enable_hitting(True)

        # BUG depends on center
        if not isinstance(str, ui.String):
            str.SetPosition(2 + str._get_width() / 2.0,
                            2 + str._get_height() / 2.0)
        self.add_child(str)

    def activate(self):
        self.ic = self.active_color
        for i in range(self._sprite.GetNbPoints()):
            self._sprite.SetPointColor(i, self.ic)

    def deactivate(self):
        self.ic = self.inactive_color
        for i in range(self._sprite.GetNbPoints()):
            self._sprite.SetPointColor(i, self.ic)


class Changer(ui.RoundedRectangle):

    def __init__(self, parent,
                 objs, func,
                 active_color, inactive_color, bordercolor, thickness):
        self.objs = objs
        self.active_idx = -1
        self.change_func = func
        maxw = max([w._get_width() + 15 for w in self.objs])
        maxh = max([w._get_height() + 5 for w in self.objs])

        ui.RoundedRectangle.__init__(self,
                                     parent,
                                     0, 0,
                                     maxw, maxh,
                                     6,
                                     active_color,
                                     bordercolor,
                                     thickness)

        for w in self.objs:
            # XXX only for strings?
            w.SetPosition(6, 0)
            self.add_child(w)
            w.set_visible(False)

        self.set_enable_hitting(True)

        # Activate the first choice
        self.active_idx = 0
        self.objs[0].set_visible(True)

    def user_hit(self, gameloop, x, y):
        a = self.active_idx
        if self.change_func:
            self.change_func(self)
        else:
            self.set_active((self.active_idx + 1) % len(self.objs))

    def get_active(self):
        return self.objs[self.active_idx]

    def set_active(self, idx):
        """Sets the active object. @idx can be either an integer [0..size-1] or
        one of the actual objects."""
        i = None
        try:
            i = self.objs.index(idx)
        except ValueError:
            pass

        if self.active_idx == idx:
            return
        if self.active_idx != -1:
            w = self.objs[self.active_idx]
            w.deactivate()
            w.set_visible(False)

        if i is not None:
            idx = i
        self.active_idx = idx

        w = self.objs[self.active_idx]
        w.activate()
        w.set_visible(True)

        e = signalslot.Event("ChangerClickEvent",
                             component = self,
                             active = w)
        self.signal_click.call(e)


class ButtonGroup:
    """Note that this is just a helper class. It is not part of the
    UI hierarchy."""

    def __init__(self, buttons = None):
        self.buttons = []
        self.active_idx = -1

        self.signal_activate_button = signalslot.Signal("Click")

        if buttons:
            for button in buttons:
                self.add_button(button)

    def add_button(self, button):
        self.buttons.append(button)
        button.signal_click.add(self._clicked)

    def _clicked(self, event):
        button = event.component
        self.activate_button(button)

    def activate_button(self, button):
        if isinstance(button, int):
            button = self.buttons[button]

        newidx = self.buttons.index(button)
        if newidx == self.active_idx:
            return

        if self.active_idx != -1:
            self.buttons[self.active_idx].deactivate()

        self.active_idx = newidx
        if self.active_idx != -1:
            print "ACTIVATE", button, self.active_idx
            self.buttons[self.active_idx].activate()
            e = signalslot.Event("ButtonGroupEvent",
                                 component = self,
                                 button = self.buttons[self.active_idx])
            self.signal_activate_button.call(e)


class LineEdit(ui.RoundedRectangle):

    def __init__(self, parent, str, active_color,
                 inactive_color, bordercolor, thickness):
        ui.RoundedRectangle.__init__(self,
                                     parent,
                                     0, 0,
                                     str._get_width() + 15,
                                     str._get_height() + 5,
                                     6,
                                     inactive_color,
                                     bordercolor,
                                     thickness)
        self.set_enable_hitting(True)
        self.active_color = active_color
        self.inactive_color = inactive_color

        # XXX only for strings?
        str.SetPosition(6, 0)
        self.add_child(str)

    def activate(self):
        for i in range(self._sprite.GetNbPoints()):
            self._sprite.SetPointColor(i, self.active_color)

    def deactivate(self):
        for i in range(self._sprite.GetNbPoints()):
            self._sprite.SetPointColor(i, self.inactive_color)

######################################################################


def create_language_switcher(parent, lcn, stringparams = None, colors={}):
    us = []
    for lang in lcn.get_language_support().get_supported_language_strings():
        lname = all_languages[lang]["name"]
        u = ui.String(None, lname, **stringparams)
        u._name = lang
        us.append(u)

    ch = Changer(
        parent,
        us,
        None,
        colors["active"],
        colors["inactive"],
        colors["border"],
        1.0)

    ch.signal_click.add(\
        lambda e: lcn.set_language_string(e.active._name))

    def switch_language(lang):
        try:
            lang = lang.language
        except:
            pass
        obj = [i for i in ch.objs if i._name == lang][0]
        ch.set_active(obj)
        lcn.set_language_string(obj._name)
    ch.switch_language = switch_language

    deflang = lcn.get_language_string()
    ch.switch_language(deflang)

    return ch
