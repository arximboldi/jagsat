#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from state import State
import model.world
from tf.gfx import ui
from tf.gfx.widget import intermediate as ui2
from model.world import create_game
from base.conf import ConfNode
from ui.world import WorldComponent
from PySFML import sf
from tf import signalslot
from base import signal
from base.log import get_log
import os
from quit import QuittableState

_log = get_log (__name__)

THEME = { 'active'    : sf.Color (0, 0, 0),
          'inactive'  : sf.Color (128, 128, 128), 
          'border'    : sf.Color (255, 255, 128),
          'thickness' : 2 }


class IngameMenuState (QuittableState):
    """
    TODO: Most of this has to be turned into a Component.
    """

    def do_release (self):
        super (IngameMenuState, self).do_release ()
        self.root.remove_myself ()
    
    def do_setup (self, *a, **k):
        super (IngameMenuState, self).do_setup (*a, **k)

        # TODO: Make this in a less breakable way
        self.root = ui.HBox (
            self.parent_state.parent_state.ui_layer)
        self.root.set_position_rel (0.30, 0.4)
        layer = self.root
        #layer._sprite = None # HACK
        
        #
        # JP: The logic shoudl work in a different way, I will explain late.r
        #
        
	# self.ingame_menu_button = ui2.Button (
        #     layer, ui.String (layer, unicode ('Menu')), THEME)
	# self.ingame_menu_button.set_position(490,0)

	# self.ingame_menu_button.on_click = signal.Signal ()
        # self.ingame_menu_button.signal_click.add (
        #     self.ingame_menu_button.on_click)
        # self.ingame_menu_button.on_click += self.ingame_menu
        # self.ingame_menu_button.set_enable_hitting (True)
        
	self.hbox = ui.HBox(layer)
	self.hbox.set_visible(False)
	self.hbox.set_position(384,350)
    
        #self.vbox = ui.MultiLineString(layer)
        self.vbox = ui.VBox(layer)
        self.vbox.set_visible(False)
        self.vbox.set_position(384,100)
        #self.vbox.set_color()
        #self.vbox.set_font(2)
       
        self.hbox.padding_left = 10
        self.save = ui2.Button (
            self.hbox, ui.String (self.hbox, unicode ('| Save')), THEME)
        self.help = ui2.Button (
            self.hbox, ui.String (self.hbox, unicode ('| Help')), THEME)
        self.quit = ui2.Button (
            self.hbox, ui.String (self.hbox, unicode ('| Quit')), THEME)

	self.help.on_click = signal.Signal ()
        self.help.signal_click.add (self.help.on_click)
        self.help.on_click += self.show_help
        self.help.set_enable_hitting (True)

	self.save.on_click = signal.Signal ()
        self.save.signal_click.add (self.save.on_click)
        self.save.on_click += self.savegame
        self.save.set_enable_hitting (True)

	self.quit.on_click = signal.Signal ()
        self.quit.signal_click.add (self.quit.on_click)
        self.quit.on_click += self.quitgame
        self.quit.set_enable_hitting (True)
	
	#quit2 = ui.Image(hbox,
        #   "home/prjc0910-group1/trunk/src/states/quitbutton.png")
	self.save.activate()
	self.help.activate()
	self.quit.activate()
	#self.save.signal_click(self.show_help)
	#self.help.signal_click(self.show_help)
	#self.quit.signal_click(self.show_help)
	#self.on_click = show_help()

        # HACK:
        self.ingame_menu (None)

    def ingame_menu(self, random):
	# random is needed to make the function work, anyone know why?
	# pretty simple method, changes the visibility of the ingame menu
	#
        # ANSWER BY JP: Because the signal is sending an 'event' parameter
        #        
	if self.hbox.get_visible():
	    self.hbox.set_visible(False)
	elif self.hbox.get_visible() == False:
	    self.hbox.set_visible(True)

    def show_help(self, random):
	_log.debug ('Showing the help...')
        self.startfile()
   
    def startfile(self):
        #os.system ("gnome-open "+
        #           "/home/aksu/projectcourse/prjc0910-group1/src/help.txt") 
        #Opens the helpfile via system with default editor
        # TODO: We should do this in an embedded way
        _log.debug ("Showing help file...")

    def savegame(self, random):
	#save the game with the pickler, not sure how yet will be
	#filled in later
	_log.debug ("Saving the game...")
        
    def quitgame(self, random):
        #quit the game (to desktop or main menu?)  quitting the game,
        #pressing this button should do the same thing as ctrl-c
	_log.debug ("Quitting...")
        self.quit_state ()
