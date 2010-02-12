#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base.log import get_log
from quit import QuittableState

from PySFML import sf
from tf.gfx import ui

_log = get_log (__name__)


class GameRoundState (QuittableState):

    def do_setup (self, *a, **k):
        super (GameRoundState, self).do_setup (*a, **k)
        game = self.parent_state

        txt = ui.String (game.ui_layer,
                         u"This feature has not been implemented yet.")
        txt.set_size (50)
        txt.set_center_rel (0.5, 0.5)
        txt.set_position_rel (0.5, 0.45)
        txt.set_color (sf.Color (0, 0, 0))
        txt._sprite.SetStyle (sf.String.Bold)

