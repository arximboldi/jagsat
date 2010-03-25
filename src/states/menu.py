#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evaluators in Abo Akademy is
#  completely forbidden without explicit permission of their authors.
#

from base import signal

from root import RootSubstate
from tf.gfx import ui
from ui.menu import *

def validate_profile (cfg):
    players = filter (lambda c: c.child ('enabled').value,
                      map (lambda i: cfg.child ('player-%i'%i), range (6)))
    if len (players) < 3:
        return "There must be at least 3 players to play."
    for i, x in enumerate (players):
        for y in players [i+1:]:
            if x.child ('position').value == y.child ('position').value:
                return "Two players have the same position."
            if x.child ('color').value == y.child ('color').value:
                return "Two players have the same color."
            if x.child ('name').value == y.child ('name').value:
                return "Two players have the same name."
    return None
        
class MainMenuState (RootSubstate):
    
    def do_setup (self, *a, **k):
	
	system = self.manager.system 
        self.ui_layer = ui.Layer (system.view)
        self.ui_layer.zorder = -1

        self._menu = None
        self._rebuild ()

    def _rebuild (self):
        if self._menu:
            self._menu.remove_myself ()
        self._menu = MainMenu (self.ui_layer)

        self._menu.actions.quit.on_click += self.manager.leave_state
        self._menu.actions.play.on_click += self._on_click_play

        self._menu.profiles.change_profile.on_click += self._on_change_profile

    @signal.weak_slot
    def _on_change_profile (self, ev = None):
        pass
    
    @signal.weak_slot
    def _on_click_play (self, ev = None):
        profile = self._menu.options.config
        check = validate_profile (profile)
        if check is not None:
            self.manager.enter_state (
                'message', message =
                "Invalid game options:\n%%30%%%s" % check)
        else:
            self.manager.change_state ('game', profile = profile)
        
    def do_release (self):
        self._menu.remove_myself ()
