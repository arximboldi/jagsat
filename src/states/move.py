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
    
    def do_setup (self, *a, **k):
        super (MovementState, self).do_setup (*a, **k)
        game = self.game
	
	game.ui_world.disable_picking()		# Disable picking first, otherwise attackphase picking is on
        game.ui_world.enable_picking (
            lambda r:
            r.model.owner == game.world.current_player and
            r.model.troops - r.model.used > 1,
            lambda p, r:
            r.model.owner == game.world.current_player and
            r.model.definition in p.model.definition.neighbours)
        game.ui_world.on_pick_regions += self.on_move
        
    @weak_slot
    def on_move (self, src, dst):
        _log.debug ('Moving from %s to %s.' % (str (src.model), str (dst.model)))
	
	self.risk_move(src, dst)
	

    def risk_move (self, src, dst):			#TO DO: Set constraints for movement, hop to next player.
	
	if src.model.owner == dst.model.owner:
		if src == dst:
			pass
		else:		
			dst.model.troops += 1
			src.model.troops -= 1
	else:
		pass










	




