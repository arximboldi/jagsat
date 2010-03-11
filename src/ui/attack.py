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
    txt.set_size (16)
    txt.set_color (sf.Color (255, 150, 150))
    
def set_defender_text_style (txt):
    txt.set_size (16)
    txt.set_color (sf.Color (150, 150, 255))


class Dice (ui.FreeformContainer, object):

    def __init__ (self,
                  parent = None,
                  style = None,
                  *a, **k):
        super (Dice, self).__init__ (parent, *a, **k)

        self.width     = 96
        self.height    = 96
        self.style     = style
        self._value    = 0
        self._img_dice = None
        self._img_tag  = None
        self.clear ()

    def roll (self):
        self.value = random.randint (1, 6)
    
    def fail (self):
        self._set_tag_pic ('data/icon/cancel2.png')

    def win (self):
        self._set_tag_pic ('data/icon/accept.png')

    def _set_tag_pic (self, pic):
        if self._img_tag:
            self._img_tag.remove_myself ()
        if pic is not None:
            self._img_tag = ui.Image (self, pic)
        else:
            self._img_tag = None
    
    def clear (self):
        self._set_tag_pic (None)
        self.value = 0
    
    def set_value (self, val):
        self._value = val
        if self._img_dice:
            self._img_dice.remove_myself ()
        self._img_dice = ui.Image (self, self.style % val)
        
    def get_value (self):
        return self._value
    
    value = property (get_value, set_value)


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

    @property
    def dices (self):
        return self._dices
    
    def add_dice (self):
        self.num_dices += 1
        self._rebuild_dices ()

    def del_dice (self):
        if self.num_dices > 0:
            self.num_dices -= 1
            self._rebuild_dices ()

    def _rebuild_dices (self):
        if self._box_dices:
            self._box_dices.remove_myself ()

        self._dices = []
        self._box_dices = widget.HBox (self.parent)
        self._box_dices.padding_right = 5
        for x in xrange (self.num_dices):
            self._dices.append (Dice (self._box_dices, self.style))
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

        self.on_attack   = signal.Signal ()
        self.on_retreat  = signal.Signal ()
        self.on_continue = signal.Signal ()

        self.width = 1024
        self.height = 768
        self.audio = audio
        
	self._dice_enabled = False
        self._sprite = None
        
        self.attacker = attacker
        self.defender = defender

        self._attacker_dices = DiceBox (self, 'data/icon/rdice%i.png', .58)
        self._defender_dices = DiceBox (self, 'data/icon/bdice%i.png', .42)
        self.attacker.used   += 1
        self.attacker.troops -= 1
        
        self._but_continue = widget.Button (
            self, 'Continue', 'data/icon/next.png')
        self._but_continue.set_center_rel (.5, .5)
        self._but_continue.set_position_rel (.9, .5)
        self._but_continue.set_visible (False)
        self._but_continue.on_click += self._dispatch_continue

        self._box_attacker = widget.VBox (self)

        self._txt_attacker = ui.String (self._box_attacker, unicode (
            self.attacker.definition.name +
            ": %i/%i" % (self.attacker.troops, self.attacker.used)))            
        set_attacker_text_style (self._txt_attacker)
       
        self._box_attacker_a = widget.HBox (self._box_attacker)
        self._box_attacker_b = widget.HBox (self._box_attacker)
        self._box_attacker.padding_bottom = 10
        self._box_attacker_a.padding_right = 10
        self._box_attacker_b.padding_right = 10
        
        self._box_defender = widget.VBox (self)
        self._box_defender_txt = widget.HBox (self._box_defender)
        self._box_defender_txt.padding_left = 10 # DIRTY HACK, bugs in TF
        self._txt_defender = ui.String (self._box_defender_txt, unicode (
            self.defender.definition.name + 
            ": %i" % self.defender.troops))
        set_defender_text_style (self._txt_defender)
        
        self._box_defender_a = widget.HBox (self._box_defender)
        self._box_defender_b = widget.HBox (self._box_defender)
        self._box_defender.padding_bottom = 10
        self._box_defender_a.padding_left = 10
        self._box_defender_b.padding_left = 10
        self._box_defender_b.set_center_rel (-0.5, 0)
        self._box_defender_b.set_position_rel (0.5, 0)
        
        move_to_player_position (self._box_attacker, self.attacker.owner)
        move_to_player_position (self._box_defender, self.defender.owner)
        
        self._but_attacker_troops_inc = widget.SmallButton (
            self._box_attacker_a, None, 'data/icon/attacker-more.png')	
        self._but_attacker_troops_dec = widget.SmallButton (
            self._box_attacker_a, None, 'data/icon/attacker-less.png')
        self._but_attacker_attack  = widget.SmallButton (
            self._box_attacker_b, None, 'data/icon/attack.png')
        self._but_attacker_retreat = widget.SmallButton (
            self._box_attacker_b, None, 'data/icon/retreat.png')
        
	self._but_defender_troops_inc = widget.SmallButton (
            self._box_defender_a, None, 'data/icon/defender-more.png')
	self._but_defender_troops_dec = widget.SmallButton (
            self._box_defender_a, None, 'data/icon/defender-less.png')
        self._but_defender_attack  = widget.SmallButton (
            self._box_defender_b, None, 'data/icon/attack.png')

        self._but_attacker_troops_inc.on_click += self._attacker_troops_inc
        self._but_attacker_troops_dec.on_click += self._attacker_troops_dec
        self._but_defender_troops_dec.on_click += self._defender_troops_dec
        self._but_defender_troops_inc.on_click += self._defender_troops_inc
        self._but_attacker_attack.on_click     += self._on_attack_attacker
        self._but_defender_attack.on_click     += self._on_attack_defender
        self._but_attacker_retreat.on_click    += self._on_attack_retreat

        self.attacker.on_set_region_troops += self._on_change_attacker_txt
        self.attacker.on_set_region_used   += self._on_change_attacker_txt
        self.defender.on_set_region_troops += self._on_change_defender_txt

    @signal.weak_slot
    def _on_attack_retreat (self, ev):
        self.attacker.used   -= self.attacker_dices.num_dices
        self.attacker.troops += self.attacker_dices.num_dices
        self.on_retreat ()

    @signal.weak_slot
    def _dispatch_continue (self, ev):
        self.on_continue ()

    def enable_continue (self):
        self._but_continue.set_visible (True)

    def disable_continue (self):
        self._but_continue.set_visible (False)
    
    def _on_change_attacker_txt (self, reg, val):
        self._txt_attacker.set_string (
            self.attacker.definition.name +
            ": %i/%i" % (self.attacker.troops, self.attacker.used))

    def _on_change_defender_txt (self, reg, val):
        self._txt_defender.set_string (
            self.defender.definition.name + ": %i" % self.defender.troops)

    def restore (self):
        """ Use this method to re-setup the UI to handle a new attack. """
        self.disable_continue ()
        self._box_defender.activate ()
        self._box_attacker.activate ()

        defender_max_dices = self.defender.troops
        while self.defender_dices.num_dices > defender_max_dices:
            self.defender_dices.del_dice ()
        
        attacker_max_dices = self.attacker.troops
        while self.attacker_dices.num_dices > attacker_max_dices:
            self.attacker_dices.del_dice ()
        self.attacker.troops -= self.attacker_dices.num_dices
        self.attacker.used   += self.attacker_dices.num_dices
        
        for d in self._attacker_dices.dices:
            d.clear ()
        for d in self._defender_dices.dices:
            d.clear ()
    
    @property
    def attacker_dices (self):
        return self._attacker_dices

    @property
    def defender_dices (self):
        return self._defender_dices

    @signal.weak_slot
    def _on_attack_defender (self, ev):
        self._box_defender.deactivate ()
        if not self._but_attacker_attack.get_enable_hitting ():
            self.on_attack ()
            
    @signal.weak_slot
    def _on_attack_attacker (self, ev):
        self._box_attacker.deactivate ()
        if not self._but_defender_attack.get_enable_hitting ():
            self.on_attack ()
    
    @signal.weak_slot
    def _attacker_troops_inc (self, ev):
        num_dices = self._attacker_dices.num_dices
	if not (self.attacker.troops == 1 and num_dices == self.attacker.used) \
               and num_dices < 3 and self.attacker.can_attack:
            # The first condition avoids the possibility of losing the country
            # in the combat.
	    self._attacker_dices.add_dice ()
            self.audio.play_sound (theme.ok_click)
            self.attacker.troops -= 1
            self.attacker.used   += 1
        else:
            self.audio.play_sound (theme.bad_click)

    @signal.weak_slot
    def _attacker_troops_dec (self, ev):
	if self._attacker_dices.num_dices > 1:
	    self._attacker_dices.del_dice ()
            self.audio.play_sound (theme.ok_click)
            self.attacker.troops += 1
            self.attacker.used   -= 1
        else:
            self.audio.play_sound (theme.bad_click)

    @signal.weak_slot
    def _defender_troops_inc (self, ev):
        num_dices = self._defender_dices.num_dices
	if num_dices < 2 and self.defender.troops > num_dices:
	    self._defender_dices.add_dice ()
            self.audio.play_sound (theme.ok_click)
        else:
            self.audio.play_sound (theme.bad_click)

    @signal.weak_slot
    def _defender_troops_dec (self, ev):
	if self._defender_dices.num_dices > 1:
	    self._defender_dices.del_dice ()
            self.audio.play_sound (theme.ok_click)
        else:
            self.audio.play_sound (theme.bad_click)
