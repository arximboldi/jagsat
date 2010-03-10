#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from PySFML import sf

from base.log import get_log
from base import signal
from player import move_to_player_position

from tf.gfx import ui
import widget
import theme
import random

from PySFML import sf

_log = get_log (__name__)

def set_attacker_text_style (txt):
    txt.set_size (15)
    txt.set_color (sf.Color (255, 150, 150))
    
def set_defender_text_style (txt):
    txt.set_size (15)
    txt.set_color (sf.Color (150, 150, 255))


class DiceBox (ui.FreeformContainer, object):

    def __init__ (self,
                  parent = None,
                  style = None,
                  vpos = None,
                  *a, **k):
        super (DiceBox, self).__init__ (parent, *a, **k)
        self.width      = 1024   # hack
        self.hegiht     = 768
        self.style      = style
        self.vpos       = vpos
        self.num_dices  = 1
        
        self._dices     = []
        self._box_dices = None
        self._rebuild_dices ()
        
    def add_dice (self):
        self.num_dices += 1
        self._rebuild_dices ()

    def del_dice (self):
        self.num_dices -= 1
        self._rebuild_dices ()

    def _rebuild_dices (self):
        if self._box_dices:
            self._box_dices.remove_myself ()

        self._dices = []
        self._box_dices = widget.HBox (self.parent)
        self._box_dices.padding_right = 5
        for x in xrange (0, self.num_dices):
            self._dices.append (ui.Image (self._box_dices, self.style % 0))
        self._box_dices.set_center_rel (0.5, 0.5)
        self._box_dices.set_position_rel (.5, self.vpos)


class AttackComponent (ui.FreeformContainer, object):

    def __init__ (self,
                  parent = None,
                  attacker = None,
                  defender = None,
                  audio = None,
                  *a, **k):
        super (AttackComponent, self).__init__ (parent, *a, **k)
        self.width = 1024
        self.height = 768
        self.audio = audio
        
	self._dice_enabled = False
        self._sprite = None
        
        self.attacker = attacker
        self.defender = defender
        
        self._attacker_dices = DiceBox (self, 'data/icon/rdice%i.png', .58)
        self._defender_dices = DiceBox (self, 'data/icon/bdice%i.png', .42)
        
        self._box_attacker = widget.VBox (self)

        self._txt_attacker_troops = ui.String (self._box_attacker, unicode (
            self.attacker.definition.name +
            ": %i/%i" % (self.attacker.troops, self.attacker.used)))            
        set_attacker_text_style (self._txt_attacker_troops)
       
        self._box_attacker_a = widget.HBox (self._box_attacker)
        self._box_attacker_b = widget.HBox (self._box_attacker)
        self._box_attacker.padding_bottom = 10
        self._box_attacker_a.padding_right = 10
        self._box_attacker_b.padding_right = 10
        
        self._box_defender = widget.VBox (self)
        self._box_defender_txt = widget.HBox (self._box_defender)
        self._box_defender_txt.padding_left = 10 # DIRTY HACK, bugs in TF
        self._txt_defender_troops = ui.String (self._box_defender_txt, unicode (
            self.defender.definition.name + 
            ": %i" % self.defender.troops))
        set_defender_text_style (self._txt_defender_troops)
        
        self._box_defender_a = widget.HBox (self._box_defender)
        self._box_defender_b = widget.HBox (self._box_defender)
        self._box_defender.padding_bottom = 10
        self._box_defender_a.padding_left = 10
        self._box_defender_b.padding_left = 10
        self._box_defender_b.set_center_rel (-0.5, 0)
        self._box_defender_b.set_position_rel (0.5, 0)
        
        move_to_player_position (self._box_attacker, self.attacker.owner)
        move_to_player_position (self._box_defender, self.defender.owner)
        
        self._attack_troops_increase = widget.SmallButton (
            self._box_attacker_a, None, 'data/icon/attacker-more.png')	
        self._attack_troops_decrease = widget.SmallButton (
            self._box_attacker_a, None, 'data/icon/attacker-less.png')
        self._but_attack_attack  = widget.SmallButton (
            self._box_attacker_b, None, 'data/icon/attack.png')
        self._but_attack_retreat = widget.SmallButton (
            self._box_attacker_b, None, 'data/icon/retreat.png')
        
	self._defense_troops_increase = widget.SmallButton (
            self._box_defender_a, None, 'data/icon/defender-more.png')
	self._defense_troops_decrease = widget.SmallButton (
            self._box_defender_a, None, 'data/icon/defender-less.png')
        self._but_defense_attack  = widget.SmallButton (
            self._box_defender_b, None, 'data/icon/attack.png')

        self._attack_troops_increase.on_click += \
            self.attacker_troops_increase
        self._attack_troops_decrease.on_click += \
            self.attacker_troops_decrease
        self._defense_troops_decrease.on_click += \
            self.defender_troops_decrease
        self._defense_troops_increase.on_click += \
            self.defender_troops_increase

        self._box_defender.deactivate ()
        
    @signal.weak_slot
    def attacker_troops_increase(self, _):
        num_dices = self._attacker_dices.num_dices
	if num_dices < 3 and self.attacker.troops > num_dices + 1:
	    self._attacker_dices.add_dice ()
            self.audio.play_sound (theme.ok_click)
        else:
            self.audio.play_sound (theme.bad_click)

    @signal.weak_slot
    def attacker_troops_decrease(self, _):
	if self._attacker_dices.num_dices > 1:
	    self._attacker_dices.del_dice ()
            self.audio.play_sound (theme.ok_click)
        else:
            self.audio.play_sound (theme.bad_click)

    @signal.weak_slot
    def defender_troops_increase(self, _):
        num_dices = self._defender_dices.num_dices
	if num_dices < 2 and self.defender.troops > num_dices:
	    self._defender_dices.add_dice ()
            self.audio.play_sound (theme.ok_click)
        else:
            self.audio.play_sound (theme.bad_click)

    @signal.weak_slot
    def defender_troops_decrease(self, _):
	if self._defender_dices.num_dices > 1:
	    self._defender_dices.del_dice ()
            self.audio.play_sound (theme.ok_click)
        else:
            self.audio.play_sound (theme.bad_click)

    def get_dice_enabled (self):
        return self._dice_enabled

    def set_dice_enabled (self, val):
        self._dice_enabled = val
        self._attack_troops_increase.set_visible (self._dice_enabled)
	self._attack_troops_decrease.set_visible (self._dice_enabled)
	self._defense_troops_increase.set_visible (self._dice_enabled)
	self._defense_troops_decrease.set_visible (self._dice_enabled)

    dice_enabled = property (get_dice_enabled, set_dice_enabled)
