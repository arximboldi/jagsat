#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base import signal

import theme

from PySFML import sf

from tf.gfx import ui
import tf.gfx.widget.basic as ui2
import tf.gfx.widget.intermediate as ui3

Component = ui.Component
VBox = ui.VBox
HBox = ui.HBox

SmallButton = lambda *a, **k: Button (theme = theme.SMALL_BUTTON_THEME, *a, **k)

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

