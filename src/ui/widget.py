#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base.log import get_log
from base import util
from base import signal
from core import task
import theme

from PySFML import sf
from tf.gfx import ui
import tf.gfx.widget.basic as ui2
import tf.gfx.widget.intermediate as ui3
import functools
from itertools import islice

_log = get_log (__name__)

Component = ui.Component
VBox = ui.VBox
HBox = ui.HBox

class Frame (ui.RoundedRectangle, object):
    def __init__ (self, parent = None, theme = theme.frame):
        super (Frame, self).__init__ (parent, 0, 0, 0, 0, 15,
                                      theme.active.color,
                                      theme.active.border,
                                      theme.active.thickness)
        self.set_expand (True, True)

SmallButton = lambda *a, **k: \
    Button (theme = theme.small_button, *a, **k)

Text = ui.String

class Button (ui3.Button, object):

    def __init__ (self,
                  parent = None,
                  text   = None,
                  image  = None,
                  vertical = True,
                  theme  = theme.button,
                  *a, **k):

        if vertical:
            self._box    = VBox (center = True)
        else:
            self._box    = HBox ()
            self._box.padding_right = 6
        
        self.string = None
        self.image = ui.Image (self._box, image)

        if text is None: text = u""
        self.string = ui.MultiLineString (self._box, unicode (text))
        self.string.set_size (theme.active.text_size)
            
        super (Button, self).__init__ (
            parent, self._box, theme, *a, **k)

        self.on_click = signal.Signal ()
        self.signal_click.add (self.on_click)

    def set_image (self, fname):
        if self.image:
            self.image.load_image (fname)

    def set_string (self, string):
        if self.string:
            self.string.set_string (unicode (string))


class SelectButton (Button):

    def __init__ (self, *a, **k):
        super (SelectButton, self).__init__ (theme=theme.select_button, *a, **k)
        self._is_selected = False
        self.on_select   = signal.Signal ()
        self.on_unselect = signal.Signal ()
        self.on_click += self.toggle_select
        
    @property
    def is_selected (self):
        return self._is_selected
    
    def select (self):
        if not self._is_selected:
            self.on_select (self)
            self._is_selected = True
            self._rebuild (self.theme.selected)
    
    def unselect (self):
        if self._is_selected:
            self.on_unselect (self)
            self._is_selected = False
            self._rebuild (self.theme.active)
    
    @signal.weak_slot
    def toggle_select (self, ev = None):
        if self._is_selected:
            self.unselect ()
        else:
            self.select ()


class List (HBox):

    def __init__ (self,
                  parent      = None,
                  num_slots   = None,
                  contents    = None,
                  button_size = None,
                  *a, **k):
        super (List, self).__init__ (parent)

        self._slot_box     = VBox (self)
        self._but_box      = VBox (self)
        self._contents     = contents
        self._num_slots    = num_slots

        self._but_up       = SmallButton (self._but_box, None,
                                          'data/icon/up-tiny.png')
        self._but_down     = SmallButton (self._but_box, None,
                                          'data/icon/down-tiny.png')
        
        self._slots        = map (lambda _: SelectButton (self._slot_box,
                                                          vertical = False),
                                  xrange (num_slots))

        self._selected_idx = -1
        self._offset       = 0

        self._but_box.padding_bottom  = 6
        self._slot_box.padding_bottom = 6
        self.padding_right            = 6
        
        for i, s in enumerate (self._slots):
            s.on_select   += self._on_select_slot
            s.on_unselect += self._on_unselect_slot
            if button_size:
                s.set_expand (False, False)
                s._width, s._height = button_size
            s.deactivate ()

        self._but_down.on_click += self.on_move_down
        self._but_up.on_click   += self.on_move_up

        self._rebuild ()

    def _rebuild (self):
        i = 0
        for (i, (img, txt, _)) in enumerate (
            islice (self._contents,
                    self._offset,
                    self._offset + self._num_slots)):
            slot = self._slots [i]
            slot.set_image (img)
            slot.set_string (txt)
            slot._list_idx = i + self._offset
            slot.activate ()
            if slot._list_idx == self._selected_idx:
                slot.select ()
            else:
                slot.unselect ()

        for j in range (i+1, self._num_slots):
            slot = self._slots [j]
            slot.set_string (" ")
            slot.set_image (None)
            slot.deactivate ()
            slot._list_idx = -1

        if self._offset + self._num_slots >= len (self._contents):
            self._but_down.deactivate ()
        else:
            self._but_down.activate ()

        if self._offset == 0:
            self._but_up.deactivate ()
        else:
            self._but_up.activate ()

    def select (self, cnt):
        _log.debug ("Trying to select: %s" % cnt)
        idx = util.index_if (lambda (i,t,c): c == cnt, self._contents)
        self._selected_idx = idx
        self._rebuild ()
    
    @property
    def selected (self):
        if self._selected_idx < 0:
            print "WTF: ", self._selected_idx
            return None
        try:
            return self._contents [self._selected_idx] [2]
        except Exception:
            return None

    @signal.weak_slot
    def on_move_down (self, ev = None):
        if self._offset < len (self._contents) - self._num_slots:
            self._offset += 1
            self._rebuild ()

    @signal.weak_slot
    def on_move_up (self, ev = None):
        if self._offset > 0:
            self._offset -= 1
            self._rebuild ()

    @signal.weak_slot
    def _on_select_slot (self, slot):
        if slot._list_idx < 0:
            slot.unselect ()
            return
        for s in self._slots:
            if s != slot:
                s.unselect ()
        print "Selecting: ", slot._list_idx
        self._selected_idx = slot._list_idx

    @signal.weak_slot
    def _on_unselect_slot (self, slot):
        if slot._list_idx == self._selected_idx:
            print "Unselecting: ", self._selected_idx
            self._selected_idx = -1
    

class Background (ui.Rectangle, object):

    def __init__ (self, parent = None, *a, **k):
        super (Background, self).__init__ (
            parent, 0, 0,
            1024 * 2, 768 * 2, # HACK!
            sf.Color.Black, sf.Color.Black, 1., *a, **k)
        self.set_center_rel (.5, .5)
        self.set_position_rel (.5, .5)
        self.on_click = signal.Signal ()
        self.signal_click.add (lambda ev: self.on_click ())
        
    def fade_in (self, duration = .75):
        """ TODO: Make generic for any widget, but its not trivial """
        return self._make_fade_task (task.fade, duration)

    def fade_out (self, duration = .75):
        return self._make_fade_task (task.invfade, duration)

    def _make_fade_task (self, fade_task, duration = .75):
        return fade_task (lambda x:
                       self.set_color (sf.Color (0, 0, 0, x*210)),
                       init = True, duration = duration)

def move_in (comp, vertical = False, duration = .75, inverse = False):
    start = sf.Vector2 (-1, 0) if not vertical else sf.Vector2 (0, -1)
    end   = sf.Vector2 (0, 0)

    if inverse:
        return task.linear (comp.set_position_rel, end, start,
                            init = True, duration = duration)
    return task.linear (comp.set_position_rel, start, end,
                        init = True, duration = duration)

move_out = functools.partial (move_in, inverse = True)
