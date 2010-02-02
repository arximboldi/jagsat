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
from tf.gfx.widget import intermediate
from model.world import create_game
from base.conf import ConfNode
from ui.world import WorldComponent
from PySFML import sf
from tf import signalslot
from base import signal
from base.log import get_log
import os


_log = get_log (__name__)

ui2 = intermediate

THEME = { 'active' : sf.Color.Blue,
          'inactive' : sf.Color.Red, 
          'border' : sf.Color.Green,
          'thickness' : 2 }

class ingame_menu (State, object):
    
    def do_enter (self, *a, **k):
        sfview = self.system._window.window.GetDefaultView ()
        view  = ui.View (self.system._window, sfview)
        layer = ui.Layer (view)
        
        cfg = ConfNode (
            { 'player-0' :
              { 'name'     : 'jp',
                'color'    : 1,
                'position' : 2,
                'enabled'  : True },
              'player-2' :
              { 'name'     : 'pj',
                'color'    : 3,
                'position' : 4,
                'enabled'  : True },
              'map' : 'doc/map/worldmap.xml' })

        world = create_game (cfg)
        comp = WorldComponent (layer, world)



	self.ingame_menu_button = ui2.Button (layer, ui.String (layer, unicode ('Menu')), THEME)
	self.ingame_menu_button.set_position(490,0)

	self.ingame_menu_button.on_click = signal.Signal ()
        self.ingame_menu_button.signal_click.add (self.ingame_menu_button.on_click)
        self.ingame_menu_button.on_click += self.ingame_menu
        self.ingame_menu_button.set_enable_hitting (True)

	self.hbox = ui.HBox(layer)
	self.hbox.set_visible(False)
	self.hbox.set_position(384,350)
    
        #self.vbox = ui.MultiLineString(layer)
        self.vbox = ui.VBox(layer)
        self.vbox.set_visible(False)
        self.vbox.set_position(384,100)
        #self.vbox.set_color()
        #self.vbox.set_font(2)
       
       
        self.save = ui2.Button (self.hbox, ui.String (self.hbox, unicode ('Save')), THEME)
        self.help = ui2.Button (self.hbox, ui.String (self.hbox, unicode ('Help')), THEME)
        self.quit = ui2.Button (self.hbox, ui.String (self.hbox, unicode ('Quit')), THEME)

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
	
	#quit2 = ui.Image(hbox,"home/prjc0910-group1/trunk/src/states/quitbutton.png")
	self.save.activate()
	self.help.activate()
	self.quit.activate()
	#self.save.signal_click(self.show_help)
	#self.help.signal_click(self.show_help)
	#self.quit.signal_click(self.show_help)
	#self.on_click = show_help()


    def ingame_menu(self, random):
	#random is needed to make the function work, anyone know why?
	#pretty simple method, changes the visibility of the ingame menu
	
	if self.hbox.get_visible():
	    self.hbox.set_visible(False)
	elif self.hbox.get_visible() == False:
	    self.hbox.set_visible(True)


    def show_help(self, random):
	
        print "supposed to save the game"
        self.startfile()
   
    def startfile(self):
        os.system("gnome-open "+ "/home/aksu/projectcourse/prjc0910-group1/src/help.txt") 
        #Opens the helpfile via system with default editor
        
	print "supposed to show help file"

    def savegame(self, random):

	#save the game with the pickler, not sure how yet will be filled in later
	print "supposed to save the game"
    def quitgame(self, random):
        #quit the game (to desktop or main menu?)
        #quitting the game, pressing this button should do the same thing as ctrl-c 
	print "supposed to quit"
   
	
        

