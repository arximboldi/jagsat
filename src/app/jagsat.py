#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from functools import partial

from base.arg_parser import OptionWith, OptionFlag
from base.log import get_log
from core.app import GameApp

from tf.gfx import uihelp

from states.sandbox        import Sandbox
from states.root           import RootState
from states.root           import RootDialogState
from states.root           import RootMessageState
from states.game           import GameState
from states.init_game      import InitGameState
from states.ingame_menu    import IngameMenuState
from states.round          import GameRoundState
from states.menu           import MainMenuState
from states.reinforcements import ReinforcementState
from states.attack	   import AttackState
from states.move	   import MovementState
from states.risk_attack    import RiskAttackState

_log = get_log (__name__)

class JagsatApp (GameApp):

    NAME = 'jagsat'
    
    OPTIONS = GameApp.OPTIONS + \
"""
Game options:
  -m, --map <file>    Map file to load.
  -s, --state <state> Initial state.
      --ratio-hack    Enable hack for the Asus tablet.
"""

    LICENSE = \
"""
  This software is in development and the distribution terms have not
  been decided yet. Therefore, its distribution outside the JAGSAT
  project team or the Project Course evalautors in Abo Akademy is
  completly forbidden without explicit permission of their authors.
"""

    AUTHOR = 'The JAGSAT development team.'
    COPYRIGHT = 'Copyright (C) 2009 The JAGSAT development team.'

    def __init__ (self, *a, **k):
        super (JagsatApp, self).__init__ (*a, **k)

        self._arg_map   = OptionWith (str)
        self._arg_state = OptionWith (str)
        self._arg_rhack = OptionFlag ()
        
        self.root_state = 'root'
        
    def do_prepare (self, args):
        super (JagsatApp, self).do_prepare (args)

        args.add ('m',  'map',        self._arg_map)
        args.add ('s',  'state',      self._arg_state)
        args.add (None, 'ratio-hack', self._arg_rhack)
        
        self.add_state ('sandbox',          Sandbox)
        self.add_state ('root',             RootState)
        self.add_state ('game',             GameState)
        self.add_state ('init_game',        InitGameState)
        self.add_state ('game_round',       GameRoundState)
        self.add_state ('ingame_menu',      IngameMenuState)
	self.add_state ('main_menu',        MainMenuState)
	self.add_state ('reinforce',        ReinforcementState)
	self.add_state ('attack',	    AttackState)
	self.add_state ('move',		    MovementState)
	self.add_state ('risk_attack',      RiskAttackState)
        self.add_state ('message',          RootMessageState)
        self.add_state ('dialog',           RootDialogState)

        self.add_state ('test_reinforce', partial (GameState,
                                                   test_phase='reinforce'))
        self.add_state ('test_attack',    partial (GameState,
                                                   test_phase='attack'))
        self.add_state ('test_move',      partial (GameState,
                                                   test_phase='move'))
    
    def do_execute (self, freeargs):
        if self._arg_state.value:
            self.root_state = self._arg_state.value

        if self._arg_rhack.value:
            uihelp.xratio = 1366./1024
            
        super (JagsatApp, self).do_execute (freeargs)
