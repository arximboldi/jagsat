#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#


from base.signal import weak_slot
from base.log import get_log
from game import GameSubstate
import random

from PySFML import sf
from tf.gfx import ui

_log = get_log (__name__)


class MovementState (GameSubstate):
    """
    TODO: Automatic pass to next player when no more movements are possible?
    """
    
    def do_setup (self, *a, **k):
        super (MovementState, self).do_setup (*a, **k)
        game = self.game

	game.ui_world.enable_used ()
        game.ui_world.enable_picking (
            lambda r:
            r.model.owner == game.world.current_player and
            r.model.has_troops (),
            lambda p, r:
            r.model.owner == game.world.current_player and
            r.model.definition in p.model.definition.neighbours)

        game.ui_world.on_pick_regions += self.on_move
        game.ui_world.on_click_region += self.on_click_region

        self.manager.enter_state ('message', message =
                                  'Move your troops among your countries.')

    def do_release (self):
        super (MovementState, self).do_release ()
        self.game.world.clean_used ()
        self.game.ui_world.disable_used ()
        self.game.ui_world.disable_picking ()
    
    @weak_slot
    def on_move (self, src, dst):
        _log.debug ('Moving from %s to %s.' %
                    (str (src.model), str (dst.model)))
	self.risk_move(src, dst)
    
    @weak_slot
    def on_click_region (self, region):
        game = self.game
        if region == self.game.ui_world.picked:
            if region.model.has_troops ():
                region.model.troops -= 1
                game.world.current_player.troops += 1

    def risk_move (self, src, dst):
        player = self.game.world.current_player
        dst.model.used += player.troops
        player.troops = 0










	




