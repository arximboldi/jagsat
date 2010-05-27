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
#

"""
Main menu ui part.
TODO: Making it more MVC would simplify states.menu a bit.
"""

from PySFML import sf
from tf.gfx import ui
from tf.gfx.widget.intermediate import Button, Button2
from tf.gfx.widget.intermediate import LineEdit
from tf.gfx.widget.basic import Keyboard

from base.conf import ConfNode, GlobalConf
from base import signal
from base import util
from base.log import get_log

from model.map import load_map_meta, load_map
from model.worldio import save_game_ext
import theme
import widget
import dialog

from os import listdir, stat, path
import time

from functools import partial
import string

_log = get_log (__name__)

def create_default_profile ():
    return ConfNode (
        { 'player-0' :
          { 'name'     : 'Napoleon',
            'color'    : 0,
            'position' : 0,
            'enabled'  : True },
          'player-1' :
          { 'name'     : 'Gengis Kan',
            'color'    : 1,
            'position' : 1,
            'enabled'  : True },
          'player-2' :
          { 'name'     : 'Mannerheim',
            'color'    : 2,
            'position' : 2,
            'enabled'  : True },
          'player-3':
          { 'name'     : 'Alexander Magnus',
            'color'    : 3,
            'position' : 3,
            'enabled'  : False },
          'player-4':
          { 'name'     : 'Julius Caesar',
            'color'    : 4,
            'position' : 4,
            'enabled'  : False },
          'player-5':
          { 'name'     : 'Attila',
            'color'    : 5,
            'position' : 5,
            'enabled'  : False },
          'map'         : 'data/map/world_map.xml',
          'use-on-attack' : True,
          'use-on-move'   : True })

def title_text (parent, text):
    txt = ui.String (parent, unicode (text))
    txt.set_size  (25)
    txt.set_color (sf.Color (255, 255, 255, 70))
    txt._sprite.SetStyle (sf.String.Bold)
    return txt

class MainMenu (ui.Image):

    def __init__ (self, parent = None, *a, **k):
        super (MainMenu, self).__init__ (parent, 'data/image/texture04.jpg',
                                         *a, **k)

        self._vbox = widget.VBox (self)
                
        self.profiles = ProfileManager (self._vbox)
        self.options  = GameOptions (self._vbox, config =
                                     self.profiles.current)
        self.actions  = MainActions (self._vbox)

        self._vbox.separation = 30

        self._vbox.set_center_rel (.5, .5)
        self._vbox.set_position_rel (.53, .52)


class CreditsDialog (ui.FreeformContainer, dialog.DialogBase):
    """
    TODO: Add artwork makers.
    """
    
    def __init__ (self, parent = None, *a, **k):
        super (CreditsDialog, self).__init__ (parent, *a, **k)
        self.width  = 1024
        self.height = 768
        self.set_enable_hitting (True)
        self.activate ()
        self.signal_click.add (lambda ev: self.on_dialog_exit ('credits'))
        
        self._box = widget.VBox (self)
        self._box.separation = 20
        
        title_text (self._box, '> The JAGSAT Team')
        ui.MultiLineString (self._box, unicode (
            "%25%Juan Pedro Bolivar Puente\n"
            "%15%Main Programmer\n%8%\n"
            "%25%Aksel Junkkila\n"
            "%15%Game Designer\n%8%\n"
            "%25%Guillem Medina\n"
            "%15%Progammer\n%8%\n"
            "%25%Sarah Lidstrom\n"
            "%15%Bussiness Consultant\n%8%\n"
            "%25%Alberto Villegas Erce\n"
            "%15%Documentation Manager\n%8%\n"
            "%25%Thomas Forss\n"
            "%15%Project Manager\n%8%\n"))

        ui.MultiLineString (self._box, unicode (
            "%15%(Click to quit or wait 5 seconds)")).set_color (
            sf.Color (255, 255, 0, 200))

        self._box.set_center_rel (.5, .5)
        self._box.set_position_rel (.5, .5)

class MainActions (widget.HBox):

    def __init__ (self, parent = None, *a, **k):
        super (MainActions, self).__init__ (parent, center = True, *a, **k)
        self.separation = 20

        # title_text (self, '> Actions ')
        
        self.play = widget.Button (
            self, 'Play', 'data/icon/troops-small.png', vertical = False)
        self.load = widget.Button (
            self, 'Load', 'data/icon/load-small.png', vertical = False)
        self.quit = widget.Button (
            self, 'Quit', 'data/icon/quit-small.png', vertical = False)


class LoadGameReturn (dialog.DialogReturn): pass
class DeleteGameReturn (dialog.DialogReturn): pass
class LoadGameDialog (widget.VBox, dialog.DialogBase):

    def __init__ (self, parent = None,
                  save_folder = '',
                  *a, **k):
        super (LoadGameDialog, self).__init__ (parent, *a, **k)

        self.separation = 20
        title_text (self, '> Load Game')

        extension = '.' + save_game_ext
        
        contents = [ ('data/icon/save-small.png',
                      "%%22%%%s\n%%14%%%s" %
                      (s [:-len (extension)],
                       time.asctime (
                           #"%b %e  %Y",
                           time.localtime (
                               stat (path.join (save_folder, s)).st_mtime))),
                      path.join (save_folder, s))
                     for s in listdir (save_folder)
                     if s [-len (extension):] == extension]
        print contents
        print listdir (save_folder)
        self._save_list = widget.List (parent = self,
                                       num_slots = 6,
                                       contents = contents,
                                       button_size = (450, 56))

        self._but_box = widget.HBox (self)
        self._but_box.separation = 15

        self._but_load = widget.Button (
            self._but_box, 'Load', 'data/icon/load-small.png', vertical = False)
        self._but_delete = widget.Button (
            self._but_box, 'Delete', 'data/icon/cancel-small.png',
            vertical = False)
        self._but_back = widget.Button (
            self._but_box, 'Back', 'data/icon/undo-small.png', vertical = False)

        self._but_load.on_click   += self._on_load_game
        self._but_delete.on_click += self._on_delete_game
        self._but_back.on_click   += self._on_go_back

    @signal.weak_slot
    def _on_load_game (self, ev):
        self.on_dialog_exit (LoadGameReturn (self._save_list.selected))

    @signal.weak_slot
    def _on_delete_game (self, ev):
        self.on_dialog_exit (DeleteGameReturn (self._save_list.selected))

    @signal.weak_slot
    def _on_go_back (self, ev):
        self.on_dialog_exit (None)


class ProfileChangerReturn (dialog.DialogReturn): pass
class ProfileChangerDialog (widget.VBox, dialog.DialogBase):

    def __init__ (self, parent = None,
                  config = GlobalConf (),
                  *a, **k):

        super (ProfileChangerDialog, self).__init__ (parent)

        self.separation = 15
        title_text (self, "> Choose a profile")

        self._prof_list = widget.List (
            parent    = self,
            contents  = [ ('data/icon/credits-tiny.png', p.name, p.name)
                          for p in config.child ('profiles').childs () ],
            num_slots = 8,
            button_size = (400, 40),
            *a, **k)
        
        self._prof_list.select (config.child ('current-profile').value)
        self._prof_list.on_change_select += lambda x: self.on_dialog_exit (
            ProfileChangerReturn (self._prof_list.selected))


class ProfileManager (widget.HBox):

    def __init__ (self, parent = None,
                  config = GlobalConf (), *a, **k):

        super (ProfileManager, self).__init__ (parent, center = True, *a, **k)
        
        self._cfg_root     = config
        self._cfg_profiles = config.child ('profiles')

        profile_name = config.child ('current-profile').value
        if profile_name is None:
            profile_name = 'default'
            config.child ('current-profile').value = profile_name

        if self._cfg_profiles.has_child (profile_name):
            self._cfg_current = self._cfg_profiles.child (profile_name)
        else:
            self._cfg_current = self._cfg_root.child ('profiles').adopt (
                create_default_profile (), profile_name)

        title_text (self, '> Profile ')
        
        self._edit_profile = widget.LineEdit (self,
                                              text = profile_name,
                                              theme = theme.small_button_green)
        self._edit_profile.activate ()
        self._edit_profile.on_edit += self._on_profile_rename

        self.add_profile = widget.Button (
            self, 'Add', 'data/icon/add-tiny.png', vertical = False,
            theme = theme.small_button_green)
        self.del_profile = widget.Button (
            self, 'Delete', 'data/icon/cancel-tiny.png', vertical = False,
            theme = theme.small_button_green)
        self.change_profile = widget.Button (
            self, 'Change', 'data/icon/retreat-tiny.png', vertical = False,
            theme = theme.small_button_green)

        self.separation = 15

    @property
    def current (self):
        return self._cfg_current

    @property
    def profiles (self):
        return self._cfg_profiles

    @property
    def selection (self):
        return self._cfg_root.child ('current-profile')
    
    @signal.weak_slot
    def _on_profile_rename (self, name):
        if name == self._cfg_root.child ('current-profile').value:
            return # No changes.
        new_name = self.find_valid_name (name)

        self._cfg_current.rename (new_name)
        self._cfg_root.child ('current-profile').value = new_name
        self._edit_profile.on_edit (new_name)

    def find_valid_name (self, name):
        i = 1
        new_name = name
        while self._cfg_profiles.has_child (new_name):
            new_name = name + ' %i'%i
            i += 1
        return new_name


class RulesOptionsDialog (widget.VBox, dialog.DialogBase):

    def __init__ (self, parent = None, config = None, *a, **k):
        super (RulesOptionsDialog, self).__init__ (parent = parent, *a, **k)

        self.separation = 25
        self._config = config
        
        title_text (self, "> Rules configuration")

        self._options = widget.VBox (self)
        self._options.separation = 10
        self._opt_use_on_attack = widget.CheckedText (
            self._options, "Troops get tired on attack.")
        self._opt_use_on_move = widget.CheckedText (
            self._options, "Troops get tired on movement.")

        if config.child ('use-on-attack').value:
            self._opt_use_on_attack.check.select ()
        if config.child ('use-on-move').value:
            self._opt_use_on_move.check.select ()
        
        self._but_ok = widget.Button (
            self, 'Done', 'data/icon/accept-small.png', vertical = False)

        self._but_ok.on_click += self.on_dialog_exit
        
        self._opt_use_on_attack.check.on_toggle += self._update_use_on_attack
        self._opt_use_on_move.check.on_toggle   += self._update_use_on_move

    @signal.weak_slot
    def _update_use_on_attack (self, but):
        self._config.child ('use-on-attack').value = but.is_selected

    @signal.weak_slot
    def _update_use_on_move (self, but):
        self._config.child ('use-on-move').value = but.is_selected

        
class GameOptions (widget.HBox):
    
    def __init__ (self, parent = None, config = create_default_profile ()):

	super (GameOptions, self).__init__ (parent)
        
	self.on_start_game   = signal.Signal ()
	self.on_quit_program = signal.Signal ()
        self._config = config

        self._box_left = widget.VBox (self)
        self._box_left.separation = 15
        
        title_text (self._box_left, '> Player options')

        self._box_players  = widget.VBox (self._box_left)
        self._player_options = \
            [ PlayerOptions (self._box_players, config.child ('player-%i' % i))
              for i in range (6) ]
        self._box_players.separation = 10

        txt = title_text (self._box_left, '> Game options')
        txt.padding_top = 10
        self._box_extra = widget.HBox (self._box_left)
        self._box_extra.separation = 10

        self.rules = widget.SmallButton (self._box_extra,
            'Rules', 'data/icon/world-small.png', vertical = False)

        self._but_music = widget.SelectButton (
            self._box_extra, text = 'Music',  vertical = False,
            selected_img = 'data/icon/music-small.png',
            unselected_img = 'data/icon/nomusic-small.png')
        # HACK
        if GlobalConf ().child ('global-music').value:
            self._but_music.select ()
        self._but_music.on_select   += self._update_music
        self._but_music.on_unselect += self._update_music
        
        self._box_map  = widget.VBox (self)
        title_text (self._box_map, '> War map')
        self._box_map.separation = 10
        
        self._map_selector = MapSelector (parent = self._box_map)
        self._map_selector.on_change_select += self._update_map
        try:
            self._map_selector.select (config.child ('map').value)
        except Exception:
            try:
                self._map_selector.select (self._map_selector._contents [0][2])
            except Exception: pass
        
        self.separation    = 50

    @property
    def config (self):
        return self._config

    @signal.weak_slot
    def _update_music (self, but):
        GlobalConf ().child ('global-music').value = but.is_selected

    @signal.weak_slot
    def _update_map (self, value):
        self._config.child ('map').value = value

    def _get_profile (self):
        return self._profile

    def _set_profile (self, profile):
        self._profile = profile

    profile = property (_get_profile, _set_profile)


class PlayerOptions (widget.HBox):

    def __init__ (self, parent = None, config = 0, *a, **k):
        super (PlayerOptions, self).__init__ (parent = parent, *a, **k)

        name     = config.child ('name').value
        color    = config.child ('color').value
        enabled  = config.child ('enabled').value
        position = config.child ('position').value 

        self._config   = config
	self._check    = widget.CheckButton (self, selected = enabled)
        self._name     = widget.LineEdit (self, text = name)
        self._color    = ColorButton (self, color = color)
        self._position = PositionButton (self, position = position)

        self._check.on_select   += self._update_enabled
        self._check.on_unselect += self._update_enabled
        self._name.on_edit      += self._update_name
        self._color.on_click    += self._update_color
        self._position.on_click += self._update_position

        self.separation = 6
        
        self._update_enabled ()

    @signal.weak_slot
    def _update_color (self, ev = None):
        self._config.child ('color').value = self._color.color

    @signal.weak_slot
    def _update_position (self, ev = None):
        self._config.child ('position').value = self._position.position

    @signal.weak_slot
    def _update_name (self, ev = None):
        self._config.child ('name').value = self._name.text

    @signal.weak_slot
    def _update_enabled (self, but = None):
        self._config.child ('enabled').value = self._check.is_selected
        if self._check.is_selected:
            self._name.activate ()
            self._color.activate ()
            self._position.activate ()
        else:
            self._name.deactivate ()
            self._color.deactivate ()
            self._position.deactivate ()


class ColorButton (widget.SmallButton):
    
    def __init__(self, parent = None, color = 0):
        super (ColorButton, self).__init__ (parent = parent,
                                            image = 'data/icon/empty-tiny.png')

        self.theme = theme.copy_button_theme (self.theme)
        self.theme.active.color = theme.player_color [color]
        self._update (color)
        self.on_click += self._on_color_click
    
    @property
    def color (self):
        return self._color

    @signal.weak_slot
    def _on_color_click (self, ev = None):
        self._update ((self._color + 1) % 6)

    def _update (self, color):
        self._color = color
        self.theme.active.color = theme.player_color [color]
        self._rebuild (self.theme.active)

        
class PositionButton (widget.SmallButton):
     
    def __init__ (self, parent = None, position = 0, *a, **k):
	super (PositionButton, self).__init__ (parent = parent, *a, **k)
        self.on_click += self._on_click
        self.update (position)

    @property
    def position (self):
        return self._position
    
    @signal.weak_slot
    def _on_click (self, ev):
        self.update ((self._position + 1) % 6)
                
    def update (self, pos):
        pic = 'data/icon/dir-%i.png' % pos
        self._position = pos
        self.set_image (pic)

def get_map_list (path):
    return filter (lambda f: f [-4:] == '.xml', listdir (path))

class MapSelector (widget.List):

    def __init__ (self, parent = None, *a, **k):
	        
        mappath  = path.join ('data', 'map')
        maplist  = get_map_list (mappath)
        abslist  = map (partial (path.join, mappath), maplist)
        mapmetas = map (load_map, abslist)
        
        contents = zip (
            map (lambda m: path.join (mappath, m.meta.thumbnail), mapmetas),
            map (lambda (n, m):
                 '%%24%%%s\n'
                 '%%12%%by %s\n'
                 '%%12%%with %i regions.\n'
                 '%%8%%\n'
                 '%%16%%%s' %
                 (n.translate (string.maketrans ('_',' ')).title (),
                  m.meta.author, len (m.regions), m.meta.description),
                 zip (map (lambda m: m [:-4], maplist), mapmetas)),
            abslist)
        
        super (MapSelector, self).__init__ (parent      = parent,
                                            num_slots   = 4,
                                            button_size = (340, 104), 
                                            contents    = contents,
                                            *a, **k)
        for x in self._slots:
            x.string.set_color (sf.Color (255, 255, 255, 200))



