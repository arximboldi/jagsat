#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base import signal
from core import task
import theme

from PySFML import sf
from tf.gfx import ui
import tf.gfx.widget.basic as ui2
import tf.gfx.widget.intermediate as ui3
import functools

Component = ui.Component
VBox = ui.VBox
HBox = ui.HBox

Frame = lambda parent, theme = theme.FRAME_THEME: \
    ui.RoundedRectangle (parent, 0, 0, 0, 0, 15,
                         theme ['inactive'],
                         theme ['border'],
                         theme ['thickness'])

SmallButton = lambda *a, **k: \
    Button (theme = theme.SMALL_BUTTON_THEME, *a, **k)

Text = ui.String

class Button (ui3.Button, object):

    def __init__ (self,
                  parent = None,
                  text   = None,
                  image  = None,
                  vertical = True,
                  theme  = theme.BUTTON_THEME,
                  *a, **k):
        
        self._box    = VBox (center = True) if vertical else HBox () 
        self.string = None
        self.image  = None
        if image:
            self.image = ui.Image (self._box, image)
        if text:
            self.string = ui.String (self._box, unicode (text))
            self.string.set_size (20)
            
        super (Button, self).__init__ (
            parent, self._box, theme, *a, **k)

        self.on_click = signal.Signal ()
        self.signal_click.add (self.on_click)


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
