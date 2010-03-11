#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base import signal
from widget import VBox, SmallButton, SelectButton

class GameMenuComponent (VBox, object):

    def __init__ (self, parent = None, *a, **k):
        super (GameMenuComponent, self).__init__ (parent, *a, **k)

        self.but_menu = SmallButton (self, None, 'data/icon/home-small.png')
        self.but_move = SelectButton (self, None, 'data/icon/move-small.png')
        self.but_zoom = SelectButton (self, None, 'data/icon/zoom-small.png')
        self.but_rot  = SelectButton (self, None, 'data/icon/rotate-small.png')
        self.but_restore = SmallButton (self, None, 'data/icon/undo-small.png')
        
        self.but_menu.margin_right = 52
        self.but_move.margin_right = 52
        self.but_zoom.margin_right = 52
        self.but_rot.margin_right  = 52

        self.padding_bottom = 10
        
        self.set_center_rel (.5, .5)
        self.set_position_rel (1., .5)

        self.map_ops = [self.but_move, self.but_zoom, self.but_rot]
        for op in self.map_ops:
            op.on_select += self._unselect_ops
    
    @signal.weak_slot
    def _unselect_ops (self):
        for x in self.map_ops:
            x.unselect ()

