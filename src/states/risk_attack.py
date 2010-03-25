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
from core import task

import random

from PySFML import sf
from tf.gfx import ui

import ui.widget
import ui.theme
from ui.attack import AttackComponent

from base import signal

_log = get_log (__name__)


class RiskAttackState (GameSubstate, ui.widget.VBox):

    def do_setup (self, attacker = None, defender = None, *a, **k):
        super (RiskAttackState, self).do_setup (*a, **k)

        self.attacker = attacker
        self.defender = defender
        
        self.root.enable_bg ()
        self.ui_attack = AttackComponent (self.root.ui_layer,
                                          attacker.model,
                                          defender.model,
                                          self.manager.system.audio,
                                          self.game.world.use_on_attack)

        self.ui_attack.on_retreat  += self._on_retreat
        self.ui_attack.on_attack   += self._on_attack
        self.ui_attack.on_continue += self._attack_result
    
    @signal.weak_slot
    def _on_retreat (self):
        self.root.disable_bg ()
        self.ui_attack.remove_myself ()
        self.manager.leave_state ()

    @signal.weak_slot
    def _on_attack (self):
        self.tasks.add (self._make_roll_dice_task (
            iter (self.ui_attack.attacker_dices.dices +
                  self.ui_attack.defender_dices.dices)))

    @signal.weak_slot
    def _attack_result (self):
        defender = self.defender.model
        attacker = self.attacker.model
        use_on_attack = self.game.world.use_on_attack
        
        if defender.troops == 0:
            # Note that it is impossible to the country to be conquered
            # if the defender killed a unit
            conquerors = len (self.ui_attack.attacker_dices.dices)

            if use_on_attack:
                defender.used += conquerors
                attacker.used -= conquerors
            else:
                defender.troops += conquerors
                attacker.troops -= conquerors
                
            old_owner = defender.owner
            defender.owner = attacker.owner

            if use_on_attack:
                self.defender.enable_used ()
            attacker.owner.conquered += 1

            old_owner.alive = self.game.world.check_alive (old_owner)

            if old_owner.alive:
                self.manager.change_state (
                    'message', message =
                    "Player %s conquered %s." % (
                        attacker.owner.name,
                        defender.definition.name.title ()))
            else:
                self.manager.change_state (
                    'message', message =
                    "Player %s conquered %s.\nPlayer %s is now dead." %
                    (attacker.owner.name, defender.definition.name.title (),
                     old_owner.name))
                self.manager.system.audio.play_sound (
                    'data/sfx/marchs/killed_player.wav')
                
        elif not attacker.can_attack:
            self.manager.change_state ('message', message =
                "No more availible troops in %s." %
                                       attacker.definition.name.title ())
        else:
            self.ui_attack.restore ()
    
    def _evaluate_dices (self):
        sorted_attack = list (self.ui_attack.attacker_dices.dices)
        sorted_attack.sort (lambda x, y: cmp (x.value, y.value), reverse = True)
        sorted_defend = list (self.ui_attack.defender_dices.dices)
        sorted_defend.sort (lambda x, y: cmp (x.value, y.value), reverse = True)
        self.tasks.add (self._make_dice_eval_task (iter (
            zip (sorted_attack, sorted_defend))))

    def _make_dice_eval_task (self, dice_iter):
        use_on_attack = self.game.world.use_on_attack
        def eval_dice_fn ():
            try:
                attack_dice, defend_dice = dice_iter.next ()
                if attack_dice.value > defend_dice.value:
                    attack_dice.win ()
                    defend_dice.fail ()
                    self.defender.model.troops -= 1
                else:
                    attack_dice.fail ()
                    defend_dice.win ()
                    if use_on_attack:
                        self.attacker.model.used -= 1
                    else:
                        self.attacker.model.troops -= 1
                self.manager.system.audio.play_sound (random.choice (map (
                    lambda i: 'data/sfx/swords/sword_%i.wav'%i, range (1,7))))
                self.tasks.add (self._make_dice_eval_task (dice_iter))
            except StopIteration:
                self.ui_attack.enable_continue ()
        return task.sequence (task.wait (.5), task.run (eval_dice_fn))
        
    def _make_roll_dice_task (self, dice_iter):
        def roll_dice_fn ():
            try:
                dice = dice_iter.next ()
                dice.roll ()
                self.manager.system.audio.play_sound (random.choice (map (
                    lambda i: 'data/sfx/canon/canon-%i.wav' % i, range (1, 4))))
                self.tasks.add (self._make_roll_dice_task (dice_iter))
            except StopIteration:
                self._evaluate_dices ()
        return task.sequence (task.wait (.5), task.run (roll_dice_fn))
    
    def do_release (self):
        self.ui_attack.remove_myself ()
        super (RiskAttackState, self).do_release ()

