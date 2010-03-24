#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base.log import get_log
from base import signal

from tf.gfx import ui
from tf.gfx.uiactions import *

import widget
import theme

from PySFML import sf

_log = get_log (__name__)

rotation = [ 180, 135, 45, 0, 315, 225 ]
position = [ (.5, .01), (.95, .05), (.95, .95),
             (0.5, .99), (.05, .95), (.05, .05) ]


def move_to_player_position (comp, player):
    comp.set_center_rel (0.5, 1.0)
    comp.set_position_rel (* position [player.position])
    comp.set_rotation (rotation [player.position])
    

class PlayerComponent (widget.VBox, object):

    def __init__ (self, parent = None, player = None, *a, **k):
        super (PlayerComponent, self).__init__ (parent, center = True, *a, **k)
        
        self.player = player
        self._can_change_cards = False
        self._menu_enabled = False
        move_to_player_position (self, player)

        # Area for windows
        self._menu_area = ui.FreeformContainer (self)
        self._menu_area.width  = 1024 # HACK
        self._menu_area.height = 768

        # The main button
        self._but_theme = theme.copy_button_theme (theme.small_button)
        pc = theme.player_color [player.color]
        self._but_theme.active.color  = pc
        self._but_theme.active.border = sf.Color (pc.r*.4, pc.g*.4, pc.b*.4)

        self._but_main = widget.Button (
            self, None, 'data/icon/small.png', theme = self._but_theme)
        self._but_main.on_click += lambda ev: self.on_toggle_menu (self)
        
        self._txt_troops = ui.String (self._but_main, u"0")
        self._txt_troops.set_center_rel (0.5, 0.5)
        self._txt_troops.set_position (28, 26)
        self._txt_troops.set_size (20)
        self._txt_troops._sprite.SetStyle (sf.String.Bold)

        player.on_set_player_troops += self._on_set_player_troops
        player.on_add_player_card   += self._on_cards_change
        player.on_del_player_card   += self._on_cards_change
        
        # The main menu
        self._menu_main = widget.VBox (self._menu_area)
        self._but_pass = widget.SmallButton (
            self._menu_main, None, 'data/icon/next-small.png')
        self._but_cards = widget.SmallButton (
            self._menu_main, None, 'data/icon/troops-small.png')
        self._but_mission = widget.SmallButton (
            self._menu_main, None, 'data/icon/world-small.png')
        self._but_undo = widget.SmallButton (
            self._menu_main, None, 'data/icon/undo-small.png')
        
        self.padding_bottom = 0
        self._menu_main.padding_bottom = 6
        self._menu_main.set_visible (self._menu_enabled)
        self._position_menu (self._menu_main)
        
        self._but_mission.on_click += self._on_show_mission
        self._but_cards.on_click   += self._on_show_cards

        self._but_undo.deactivate ()
        self._but_pass.deactivate ()

        self._but_pass.on_click += self.on_toggle_menu
        self._current_menu = self._menu_main

    def _position_menu (self, menu):
        menu.set_center_rel (.5, 1.)
        menu.set_position_rel (.5, 1.)

    @signal.signal
    def on_drop_cards (self, selected):
        pass
        
    @signal.signal
    def on_exchange_cards (self, selected):
        pass
    
    @property
    def but_pass (self):
        return self._but_pass

    @signal.signal
    def on_toggle_menu (self, _):
        _log.debug ('Toggle menu for player: ' + str (self.player))
        self._menu_enabled = not self._menu_enabled
        self._current_menu.set_visible (self._menu_enabled)

    def enable_exchange_cards (self):
        self._can_change_cards = True
        if isinstance (self._current_menu, _CardsMenu):
            self._on_show_cards ()

    def disable_exchange_cards (self):
        self._can_change_cards = False
        if isinstance (self._current_menu, _CardsMenu):
            self._on_show_cards ()

    def toggle (self):
        self.on_toggle_menu (None)

    @signal.weak_slot
    def _on_show_mission (self, _ = None):
        self._current_menu.set_visible (False)
        self._current_menu = self._make_mission_menu ()
        self._current_menu.set_visible (self._menu_enabled)

    @signal.weak_slot
    def _on_show_cards (self, _ = None):
        self._current_menu.set_visible (False)
        self._current_menu = self._make_cards_menu ()
        self._current_menu.set_visible (self._menu_enabled)

    def _make_mission_menu (self):
        menu = widget.SmallButton (self._menu_area)
        menu.set_margin (7)
        text = ui.MultiLineString (
            menu, unicode (self.player.mission.description).split ('\n'),
            center=True)
        text.set_size (16)
        text.set_position (14, 14)
        menu.set_enable_hitting (True)
        menu.signal_click.add (self._on_back_to_main)
        menu.activate ()
        self._position_menu (menu)
        menu.set_position (1024/2, 768-10) # hack        
        return menu

    def _make_cards_menu (self):
        return _CardsMenu (self)

    @signal.weak_slot
    def _on_cards_change (self, p, c):
        if isinstance (self._current_menu, _CardsMenu):
            self._on_show_cards ()

    @signal.weak_slot
    def _on_back_to_main (self, ev = None):
        self._current_menu.remove_myself ()
        self._current_menu = self._menu_main
        self._current_menu.set_visible (self._menu_enabled)

    @signal.weak_slot
    def _on_add_player_card (self, player, card):
        self._rebuild_card_ui ()

    @signal.weak_slot
    def _on_del_player_card (self, player, card):
        self._rebuild_card_ui ()
    
    @signal.weak_slot
    def _on_set_player_troops (self, player, troops):
        if troops > 0:
            self._txt_troops.set_visible (True)
            self._txt_troops.set_string (unicode (troops))
        else:
            self._txt_troops.set_visible (False)

    def enable_undo (self):
        pass # TODO

    def disable_undo (self):
        pass # TODO


class _CardsMenu (widget.VBox, object):

    def __init__ (self, comp = None, *a, **k):
        assert isinstance (comp, PlayerComponent)
        super (_CardsMenu, self).__init__ (comp._menu_area,
                                          center = True, *a, **k)

        cards    = widget.HBox (self)
        buttons  = widget.HBox (self)
        
        self.padding_bottom  = 6
        cards.padding_left   = 6
        buttons.padding_left = 6
        
        selected = []
        for c in comp.player.cards:
            b = widget.SelectButton (cards, None, 'data/icon/card%i.png'%c)
            b.on_select   += lambda c=c: selected.append (c)
            b.on_unselect += lambda c=c: selected.remove (c)
            
        back   = widget.SmallButton (
            buttons, None, 'data/icon/undo-small.png')
        change = widget.SmallButton (
            buttons, None, 'data/icon/retreat-small.png')
        drop   = widget.SmallButton (
            buttons, None, 'data/icon/cancel-small.png')

        back.on_click   += comp._on_back_to_main
        change.on_click += lambda ev: comp.on_exchange_cards (selected)
        drop.on_click   += lambda ev: comp.on_drop_cards (selected)

        if not comp._can_change_cards:
            change.deactivate ()

        comp._position_menu (self)
