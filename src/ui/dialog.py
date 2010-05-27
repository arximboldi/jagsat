#
#  Copyright (C) 2009, 2010 JAGSAT Development Team (see below)
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
#  JAGSAT Development Team is:
#    - Juan Pedro Bolivar Puente
#    - Alberto Villegas Erce
#    - Guillem Medina
#    - Sarah Lindstrom
#    - Aksel Junkkila
#    - Thomas Forss
#

import widget
from base import signal

class DialogReturn (object):
    
    def __init__ (self, retval = None, *a, **k):
        super (DialogReturn, self).__init__ (*a, **k)
        self.retval = retval

class DialogBase (object):
    
    @signal.signal
    def on_dialog_exit (self, ret):
        pass

class YesNoDialog (widget.VBox, DialogBase):

    def __init__ (self, parent = None, message = None, *a, **k):
        super (YesNoDialog, self).__init__ (parent, center = True, *a, **k)

        self.separation = 30
        self.message = widget.Text (self, unicode (message))
        self.message.set_size (50)

        self._but_box = widget.HBox (self)
        self._but_box.separation = 20
        
        self.yes_button = widget.Button (
            self._but_box, 'Yes', 'data/icon/accept.png', vertical = False)
        self.no_button  = widget.Button (
            self._but_box, 'No', 'data/icon/no.png', vertical = False)

        self.yes_button.on_click += lambda _: self.on_dialog_exit (ret = 'yes')
        self.no_button.on_click  += lambda _: self.on_dialog_exit (ret = 'no')


class InputDialog (widget.VBox, DialogBase):

    def __init__ (self,
                  parent = None,
                  message = None,
                  input_text = 'Enter text here.',
                  *a, **k):
        super (InputDialog, self).__init__ (parent, center = True, *a, **k)

        self.margin_bottom = 400
        self.message = widget.Text (self, unicode (message))
        self.message.set_size (50)
        
        widget.get_keyboard_input (input_text, lambda text:
                                   self.on_dialog_exit (text))

