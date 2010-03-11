#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from widget import VBox, SmallButton

class GameMenuComponent (VBox, object):

    def __init__ (self, parent = None, *a, **k):
        super (GameMenuComponent, self).__init__ (parent, *a, **k)

        self.but_menu = SmallButton (self, None, 'data/icon/home-small.png')
        self.but_move = SmallButton (self, None, 'data/icon/move-small.png')
        self.but_zoom = SmallButton (self, None, 'data/icon/zoom-small.png')
        self.but_rot  = SmallButton (self, None, 'data/icon/rotate-small.png')

        self.but_menu.margin_right = 52
        self.but_move.margin_right = 52
        self.but_zoom.margin_right = 52
        self.but_rot.margin_right  = 52

        self.padding_bottom = 10
        
        self.set_center_rel (.5, .5)
        self.set_position_rel (1., .5)

        self.but_move.deactivate ()
        self.but_zoom.deactivate ()
        self.but_rot.deactivate ()
