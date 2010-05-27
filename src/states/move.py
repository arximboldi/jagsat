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

        self.tasks.add (game.ui_world.rotate_to_player (
            game.world.current_player))

        if game.world.use_on_move:
            game.ui_world.enable_used ()
            is_reachable = lambda p, r: \
                r.model.definition in p.model.definition.neighbours
        else:
            table = game.world.find_components (
                lambda r: r.owner == game.world.current_player)
            is_reachable = lambda p, r: r.model in table [p.model]
        
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
        self.manager.enter_state (
            'message', message =
            'Movement phase for player %s.\n'
            '%%30%%Move your troops among your countries.' %
            game.world.current_player.name,
            position = game.world.current_player.position)

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
        









	




