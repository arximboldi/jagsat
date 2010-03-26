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

from collections import defaultdict


_log = get_log (__name__)


class MovementState (GameSubstate):
    """
    TODO: Automatic pass to next player when no more movements are possible?
    """
    
    def do_setup (self, *a, **k):
        super (MovementState, self).do_setup (*a, **k)
        game = self.game

        game.world.phase = 'move'

        if game.world.use_on_move:
            game.ui_world.enable_used ()
            is_reachable = lambda p, r: \
                r.model.definition in p.model.definition.neighbours
        else:
            game.world.find_components (
                lambda r: r.owner == game.world.current_player)
            is_reachable = lambda p, r: r.model in p.model.component
        
        game.ui_world.enable_picking (
            lambda r:
            game.world.current_player.troops == 0 and
            r.model.owner == game.world.current_player and
            r.model.can_attack,
            lambda p, r:
            p != r and
            r.model.owner == game.world.current_player and
            is_reachable (p, r))

        game.ui_world.on_pick_regions += self.on_move
        game.ui_world.on_click_region += self.on_click_region
        self.manager.enter_state ('message', message =
                                  'Move your troops among your countries.')

    def do_release (self):
        super (MovementState, self).do_release ()
        if self.game.ui_world.picked:
            self.game.ui_world.picked.model.troops += \
                self.game.world.current_player.troops
            self.game.world.current_player.troops = 0
        if self.game.world.use_on_move:
            self.game.world.clean_used ()
            self.game.ui_world.disable_used ()
        self.game.ui_world.disable_picking ()
    
    @weak_slot
    def on_move (self, src, dst):
        _log.debug ('Moving from %s to %s.' %
                    (str (src.model), str (dst.model)))
        player = self.game.world.current_player
        if player.troops > 0:
            if self.game.world.use_on_move:
                dst.model.used += player.troops
            else:
                dst.model.troops += player.troops
            player.troops = 0
        else:
            self.game.ui_world.new_pick = dst # HACK

    @weak_slot
    def on_click_region (self, region):
        game = self.game
        if region == self.game.ui_world.picked:
            if region.model.can_attack:
                region.model.troops -= 1
                game.world.current_player.troops += 1
        









	




