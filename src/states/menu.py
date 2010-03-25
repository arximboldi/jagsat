#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evaluators in Abo Akademy is
#  completely forbidden without explicit permission of their authors.
#

from base import signal
from base import conf

from root import RootSubstate
from tf.gfx import ui
from ui.menu import (MainMenu, ProfileChangerDialog, ProfileChangeReturn,
                     RulesOptionsDialog)


def validate_profile (cfg):
    players = filter (lambda c: c.child ('enabled').value,
                      map (lambda i: cfg.child ('player-%i'%i), range (6)))
    if not cfg.child ('map').value:
        return "You must choose a map."
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

        self.menu = None
        self._rebuild ()

    def _rebuild (self):
        if self.menu:
            self.menu.remove_myself ()
        self.menu = MainMenu (self.ui_layer)

        self.menu.actions.quit.on_click += self.manager.leave_state
        self.menu.actions.play.on_click += self._on_click_play

        self.menu.profiles.change_profile.on_click += self._on_change_profile
        self.menu.profiles.del_profile.on_click += self._on_del_profile
        self.menu.profiles.add_profile.on_click += self._on_add_profile

        self.menu.options.rules.on_click += self._on_change_rules

    @signal.weak_slot
    def _on_change_rules (self, ev):
        self.manager.enter_state ('dialog', mk_dialog = RulesOptionsDialog,
                                  config = self.menu.profiles.current)
    
    @signal.weak_slot
    def _on_add_profile (self, ev):
        profiles = self.menu.profiles
        new_name = profiles.find_valid_name ('new profile')
        profiles.selection.value = new_name
        profiles.profiles.adopt (profiles.current.dict_copy (), new_name)
        self._rebuild ()
    
    @signal.weak_slot
    def _on_del_profile (self, ev):
        self.manager.enter_state (
            'yes_no_dialog',
            message = 'Are you sure you want to delete\nthe profile: %s?' %
            self.menu.profiles.current.name,
            yes_ret = 'remove_profile')

    @signal.weak_slot
    def _on_change_profile (self, ev = None):
        self.manager.enter_state ('dialog', mk_dialog = ProfileChangerDialog)
    
    @signal.weak_slot
    def _on_click_play (self, ev = None):
        profile = self.menu.options.config
        check = validate_profile (profile)
        if check is not None:
            self.manager.enter_state (
                'message', message =
                "Invalid game options:\n%%30%%%s" % check)
        else:
            self.manager.change_state ('game', profile = profile)

    def do_unsink (self,
                   dialog_ret = None,
                   dialog_yes = None,
                   dialog_no = None):
        
        if dialog_yes == 'remove_profile':
            selection = self.menu.profiles.selection
            profiles = self.menu.profiles.profiles
            profiles.remove (selection.value)
            proflist = profiles.childs ()
            if profiles.childs ():
                selection.value = proflist [0].name
            else:
                selection.value = 'default'
            self._rebuild ()

        elif isinstance (dialog_ret, ProfileChangeReturn):
            self.menu.profiles.selection.value = dialog_ret.retval
            self._rebuild ()
    
    def do_release (self):
        super (MainMenuState, self).do_release ()
        self.menu.remove_myself ()
