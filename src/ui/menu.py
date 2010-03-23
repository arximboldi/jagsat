#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evaluators in Abo Akademi is
#  completely forbidden without explicit permission of their authors.
#

from PySFML import sf
from tf.gfx import ui
from tf.gfx.widget.intermediate import Button, Button2
from tf.gfx.widget.intermediate import LineEdit
from base.conf import ConfNode, GlobalConf
from base import signal
from base import util
from base.log import get_log
from tf.gfx.widget.basic import Keyboard

from os import listdir

import theme
import widget

_log = get_log (__name__)

_TITLE = unicode ('Bloody Empire')
_TITLE_COLOR = sf.Color(127,127,127,400)

COLOR = {0: sf.Color.Blue,
         1: sf.Color.Red,
         2: sf.Color.Black,
         3: sf.Color.Yellow,
         4: sf.Color.Green,
         5: sf.Color.Magenta}

class MenuComponent (ui.Image):
    
    def __init__ (self, parent = None):
        
        ui.Image.__init__(self, parent, 'data/image/texture01.jpg')
	self.on_click = signal.Signal ()

	self.on_start_game = signal.Signal ()
	self.on_quit_program = signal.Signal ()

	self._profile = None     # Profile used to create the game
	self._listprof = None    # List of profilessaved on the congifuration file
       

	#Main Container
	self.vbox = ui.VBox(self)
	self.vbox.set_position(50,50)
	self.vbox.padding_bottom = 8

        #Title
	#self._title = ui.String (self, _TITLE)
        #self._title.set_size (40)
        #self._title.set_center_rel (0.5, 0.5)
        #self._title.set_position_rel (0.2, 0.05)
        #self._title.set_color (sf.Color.Black)
        #self._title._sprite.SetStyle (sf.String.Bold)
	#self.titleL = LineEdit(self.vbox, self._title , _ACTIVE_COLOR, _TITLE_COLOR, _BORDER_COLOR, _THICKNESS)
	#self.titleL.set_position_rel (0.2, 0.05)

	#Main Layer

        self.profileL = ui.HBox(self.vbox)
	self.profileL.padding_right = 50
	self.profileL.padding_top = 8
        self.gameL = ui.HBox(self.vbox)
	self.gameL.padding_top = 8
        self.actionL = ui.HBox(self.vbox)
	self.actionL.padding_right = 12
	self.actionL.padding_top = 20
	self.status = ui.String(self.vbox, unicode(''))
	self.keyboard = Keyboard(self._layer)
	self.keyboard.set_position(500, 620)
	self.keyboard.set_visible(False)

	#Profile Layer
	self.default_prof()
	self.load_listprof()
	self.profile_ComboBox = ComboBox(self.profileL, self._listprof, self)
	self.profile_HBox = ui.HBox(self.profileL)
	self.profile_HBox.padding_right = 10
        self.profile_SaveButton = widget.Button(self.profile_HBox, None,'data/icon/save-small.png',True, theme.menu)
	self.profile_DeleteButton = widget.Button(self.profile_HBox, None,'data/icon/delete.png',True, theme.menu)

	self.profile_SaveButton.on_click = signal.Signal ()
        self.profile_SaveButton.signal_click.add (self.profile_SaveButton.on_click)
        self.profile_SaveButton.on_click += lambda _: self.save_profile()
        self.profile_SaveButton.set_enable_hitting (True)

        self.profile_DeleteButton.on_click = signal.Signal ()
        self.profile_DeleteButton.signal_click.add (self.profile_DeleteButton.on_click)
        self.profile_DeleteButton.on_click += self.delete_profile
        self.profile_DeleteButton.set_enable_hitting (True)
        

 	#Game Layer
        self.gameL.padding_right = 30
        self.infoplayerL = ui.VBox(self.gameL)
	self.infoplayerL.padding_bottom = 8
        self.mapL = MapSelector(self.gameL)

	#Info Player Layer

	self.playerL1 = ui.HBox(self.infoplayerL)
	self.playerL2 = ui.HBox(self.infoplayerL)
	self.playerL3 = ui.HBox(self.infoplayerL)
	self.playerL4 = ui.HBox(self.infoplayerL)
	self.playerL5 = ui.HBox(self.infoplayerL)
	self.playerL6 = ui.HBox(self.infoplayerL)

	self.playerL1.padding_right = 10
	self.playerL2.padding_right = 10
	self.playerL3.padding_right = 10
	self.playerL4.padding_right = 10
	self.playerL5.padding_right = 10
	self.playerL6.padding_right = 10

	self.playerL1._active = True
	self.playerL2._active = True
	self.playerL3._active = True
	self.playerL4._active = False
	self.playerL5._active = False
	self.playerL6._active = False

	#Player1
        
        self.en_button1 = EnableButton(self.playerL1, theme.menu)
	self.player_name1 = PlayerName(self.playerL1, 'Player1', theme.player)
        self.player_color1 = ColorButton(self.playerL1, theme.menu, 0)
        self.player_pos1 = PositionButton(self.playerL1, 0)

	self.en_button1.activate()
	self.player_name1.activate()
	self.player_color1.activate()
	self.player_pos1.activate()

	self.en_button1.on_click = signal.Signal ()
        self.en_button1.signal_click.add (self.en_button1.on_click)
        self.en_button1.on_click += lambda _: self.enable_player(0)
	self.en_button1.set_enable_hitting (True)

	self.player_name1.on_click = signal.Signal ()
        self.player_name1.signal_click.add (self.player_name1.on_click)
        self.player_name1.on_click += lambda _: self.enable_keyboard(0)
        self.player_name1.set_enable_hitting (True)

	#Player2

	self.en_button2 = EnableButton(self.playerL2, theme.menu)
        self.player_name2 = PlayerName(self.playerL2, 'Player2', theme.player)
        self.player_color2 = ColorButton(self.playerL2, theme.menu, 1)
        self.player_pos2 = PositionButton(self.playerL2, 1)

	self.en_button2.activate()
	self.player_name2.activate()
	self.player_color2.activate()
	self.player_pos2.activate()

	self.en_button2.on_click = signal.Signal ()
        self.en_button2.signal_click.add (self.en_button2.on_click)
        self.en_button2.on_click += lambda _: self.enable_player(1)
        self.en_button2.set_enable_hitting (True)

	self.player_name2.on_click = signal.Signal ()
        self.player_name2.signal_click.add (self.player_name2.on_click)
        self.player_name2.on_click += lambda _: self.enable_keyboard(1)
        self.player_name2.set_enable_hitting (True)
	
	#Player3
        
        self.en_button3 = EnableButton(self.playerL3, theme.menu)
        self.player_name3 = PlayerName(self.playerL3, 'Player3', theme.player)
        self.player_color3 = ColorButton(self.playerL3, theme.menu, 2)
        self.player_pos3 = PositionButton(self.playerL3, 2)

	self.en_button3.activate()
	self.player_name3.activate()
	self.player_color3.activate()
	self.player_pos3.activate()

	self.en_button3.on_click = signal.Signal ()
        self.en_button3.signal_click.add (self.en_button3.on_click)
        self.en_button3.on_click += lambda _: self.enable_player(2)
        self.en_button3.set_enable_hitting (True)

	self.player_name3.on_click = signal.Signal ()
        self.player_name3.signal_click.add (self.player_name3.on_click)
        self.player_name3.on_click += lambda _: self.enable_keyboard(2)
        self.player_name3.set_enable_hitting (True)
        
	#Player4

        self.en_button4 = EnableButton(self.playerL4, theme.menu)
        self.player_name4 = PlayerName(self.playerL4, 'Player4', theme.player)
        self.player_color4 = ColorButton(self.playerL4, theme.menu, 3)
        self.player_pos4 = PositionButton(self.playerL4, 3)

	self.en_button4.on_click = signal.Signal ()
        self.en_button4.signal_click.add (self.en_button4.on_click)
        self.en_button4.on_click += lambda _: self.enable_player(3)
        self.en_button4.set_enable_hitting (True)

	self.player_name4.on_click = signal.Signal ()
        self.player_name4.signal_click.add (self.player_name4.on_click)
        self.player_name4.on_click += lambda _: self.enable_keyboard(3)
        self.player_name4.set_enable_hitting (True)
        
	#Player5

        self.en_button5 = EnableButton(self.playerL5, theme.menu)
        self.player_name5 = PlayerName(self.playerL5, 'Player5', theme.player)
        self.player_color5 = ColorButton(self.playerL5, theme.menu, 4)
        self.player_pos5 = PositionButton(self.playerL5,4)

	self.en_button5.on_click = signal.Signal ()
        self.en_button5.signal_click.add (self.en_button5.on_click)
        self.en_button5.on_click += lambda _: self.enable_player(4)
        self.en_button5.set_enable_hitting (True)

	self.player_name5.on_click = signal.Signal ()
        self.player_name5.signal_click.add (self.player_name5.on_click)
        self.player_name5.on_click += lambda _: self.enable_keyboard(4)
        self.player_name5.set_enable_hitting (True)
        
	#Player6

        self.en_button6 = EnableButton(self.playerL6, theme.menu)
        self.player_name6 = PlayerName(self.playerL6, 'Player6', theme.player)
        self.player_color6 = ColorButton(self.playerL6, theme.menu, 5)
        self.player_pos6 = PositionButton(self.playerL6, 5)

	self.en_button6.on_click = signal.Signal ()
        self.en_button6.signal_click.add (self.en_button6.on_click)
        self.en_button6.on_click += lambda _: self.enable_player(5)
        self.en_button6.set_enable_hitting (True)

	self.player_name6.on_click = signal.Signal ()
        self.player_name6.signal_click.add (self.player_name6.on_click)
        self.player_name6.on_click += lambda _: self.enable_keyboard(5)
        self.player_name6.set_enable_hitting (True)

	
	#Action Layer
        
        self.start_button = widget.Button(self.actionL, None, 'data/icon/world-small.png', True, theme.menu)
        #self.load_button = Button(self.actionL, ui.String(self.actionL, unicode('Load')), theme.menu)
	self.quit_button = widget.Button(self.actionL, None, 'data/icon/quit-small.png', True, theme.menu)	

	self.start_button.signal_click.add (self.start_game)
        self.start_button.set_enable_hitting (True)

	self.quit_button.signal_click.add (self.quit_game)
        self.quit_button.set_enable_hitting (True)

	#self.load_button.on_click = signal.Signal ()
        #self.load_button.signal_click.add (self.load_button.on_click)
        #self.load_button.on_click += self.load_game
        #self.load_button.set_enable_hitting (True)

	self.load_profile('Default')

    #It creats a profile from the active information of the main menu

    def create_profile(self,name="Prove"): 
        
        self._profile = ConfNode()
        dic = {}
        for i in range(0,6):
            pinf = self.infoplayerL.get_child(i)
            if pinf._active:
                pdic = {}
                pdic['name'] = pinf.get_child(1).get_child(0)._sprite.GetText()
                pdic['color'] = COLOR [pinf.get_child(2)._col]
                pdic['position'] = pinf.get_child(3)._position
                pdic['enabled'] = True
                dic['player-' + str(i)] = pdic
                    
        dic['map'] = self.mapL.get_map()
        
        self._profile.fill(dic)   

    # Default profile of the standard risk game
    def default_prof(self):
        cfg = ConfNode (
            { 'player-0' :
              { 'name'     : 'Player1',
                'color'    : COLOR [0],
                'position' : 0,
                'enabled'  : True },
              'player-1' :
              { 'name'     : 'Player2',
                'color'    : COLOR [1],
                'position' : 1,
                'enabled'  : True },
              'player-2' :
              { 'name'     : 'Player3',
                'color'    : COLOR [2],
                'position' : 2,
                'enabled'  : True },
              'map' : 'doc/map/worldmap.xml' })

        GlobalConf ().path('profiles').adopt(cfg, 'Default')	
	
    #Read all profiles saved in the configuration files
    def load_listprof(self):
	l = []
	for i in GlobalConf ().path('profiles')._childs :
	     l.append(i)
	self._listprof = l
           
    #Load the information saved in the profile on the screen         
    def load_profile(self, name):
	
	for i in range(0,6):
	    self.disable_player(i)	
	
        index = 0

	for i in GlobalConf ().path('profiles').path(str(name)).childs() :

	    if i._name <> 'map':	    
		aux = self.infoplayerL.get_child(index)	    
		self.enable_player(index)
	    #else:
		#self.mapL.select(i.get_value())

	    for j in i.childs() :

		if j._name == 'color': 
		    aux.get_child(2).update(j.get_value()) 

		elif j._name == 'position':
		    aux.get_child(3).update(j.get_value())

		elif j._name == 'name':
		    del aux.get_child(1).children[0]
		    ui.String(aux.get_child(1), unicode(j.get_value()))

	    index = index + 1
	
    #Save the current profile in the configuration file
    def save_profile(self, name = 'Prove'): 
        
        if self.check_info() and not(self._listprof.__contains__(name)):
            self.create_profile()
	    GlobalConf ().path ('profiles').adopt (self._profile, name)
	    self._listprof.append(name)
	    self.profile_ComboBox.load(self._listprof)
	    
	    self.update_status("Profile saved")

	else:
	    self.update_status("Wrong information")

    #Delete the current profile from the configuration file
    def delete_profile(self,random):   
	name = self.profile_ComboBox.get_text().get_string()
	if name <> 'Default': 
	    GlobalConf ().path('profiles').remove(name)
	    self._listprof.remove(name)
	    self.profile_ComboBox.load(self._listprof)
	    self.update_status("Profile deleted")
	else:
	    self.update_status("Impossible to delete default profile")

    #Enable all info and actions related with the player pl    
    def enable_player(self, pl):

	aux = self.infoplayerL.get_child(pl)

	if aux._active:
	    aux._active = False
	else:
	    aux._active = True

	for j in range (0,4):
	    if aux._active:
	        aux.get_child(j).activate()
	    else:
	        aux.get_child(j).deactivate()

    def disable_player(self,pl):
	aux = self.infoplayerL.get_child(pl)
    	aux._active = False
	for j in range (0,4):
	    aux.get_child(j).deactivate()

    #Verify the information on the main menu in order to create a profile without mistakes    

    def check_info(self):  
	aux = 0
        lname = []
        lcol = []
        lpos = []
        
        for i in range(0,6):
            pinf = self.infoplayerL.get_child(i)
            if pinf._active:
		aux = aux+1
                pname = pinf.get_child(1).get_child(0)
                pcol = pinf.get_child(2)._col
                ppos = pinf.get_child(3)._position	
		
		if lname.__contains__(pname):
		    return False
		else:
		    lname.append(pname)

		if lpos.__contains__(ppos):
		    return False
		else:
		    lpos.append(ppos)

		if lcol.__contains__(pcol):
		    return False
		else:
		    lcol.append(pcol)

	if aux < 3:
	    return False 
	
        return True
    
    #Start game with the current profile
    def start_game(self, random):
        if self.check_info():
            self.create_profile()
	    self.on_start_game (self._profile)
	    self.update_status("New game")

        else:
	    self.update_status("Wrong information")
 
    def quit_game(self,random):
	self.on_quit_program()	

    def load_game(self, random):

	self.update_status("Not implemented yet")

    #Show messages on screen
    def update_status(self, str):	
	self.status.set_string(unicode(str))


    def enable_keyboard(self,pl):
	#TODO: Enable keyboard in order to modify players names and saved profiles 
	pass
	#if self.keyboard.get_visible():
	    #self.keyboard.set_position(500, 620)
	#else:
	    #self.keyboard.set_visible(True)

	

#  Extra Widgets

class PlayerName(LineEdit):
    def __init__(self, parent, str, theme):
	LineEdit.__init__(self, parent, ui.String(parent, unicode(str)),
                          theme.active.color,
                          theme.inactive.color,
                          theme.active.border,
                          theme.active.thickness)

class EnableButton(ui.Circle):

    def __init__(self, parent, theme, radius = 8):
	self.active_color = theme.active.color
	self.inactive_color = theme.inactive.color
	self.border_color = theme.active.border
	self._radius = radius
	ui.Circle.__init__(self, parent,
                           self._radius, self.active_color, 1,
                           self.border_color)

    def  activate(self):
	self._sprite = sf.Shape.Circle(self._radius,self._radius, self._radius, self.active_color, 1, self.border_color)
    def deactivate(self):
	self._sprite = sf.Shape.Circle(self._radius,self._radius, self._radius, self.inactive_color, 1, self.border_color)


class ColorButton(ui.Circle):
    _COLOR_NUM = 6
    _COLOR = COLOR

    
    def __init__(self, parent, theme, index, radius = 15):
        
        ui.Circle.__init__(self, parent, radius, sf.Color(127,127,127), 2, sf.Color.Black)
        self._col = index
	self._radius = radius
        self.active_color = self._COLOR[index]
	self.inactive_color = sf.Color(127,127,127)

	if self.parent._active:
		self._sprite = sf.Shape.Circle(self._radius, self._radius, self._radius, self.active_color, 2, sf.Color.Black)
        
        self.on_click = signal.Signal ()
        self.signal_click.add (self.on_click)
        self.on_click += self.next
        self.set_enable_hitting (True)
        
    def next(self,random):
	if self.parent._active:
	    self._col = (self._col+1)%self._COLOR_NUM
            self.active_color = self._COLOR[self._col]
	    self._sprite = sf.Shape.Circle(self._radius, self._radius,self._radius, self.active_color, 2, sf.Color.Black)

    def update(self,col):
        col = util.flip_dict (self._COLOR) [col]
	self._col = col
	self.active_color = self._COLOR[self._col]
	if self.parent._active:
	    self._sprite = sf.Shape.Circle(self._radius,self._radius, self._radius, self.active_color, 2, sf.Color.Black)

    def  activate(self):
	self._sprite = sf.Shape.Circle(self._radius,self._radius, self._radius, self.active_color, 2, sf.Color.Black)
    def deactivate(self):
	self._sprite = sf.Shape.Circle(self._radius,self._radius, self._radius, self.inactive_color, 2, sf.Color.Black)

class PositionButton(Button):
    _POS_NUM = 8
    _POS = {0: "  N ", 1: ' NE', 2:'  E ', 3: ' SE', 4:'  S ', 5:' SW', 6:'  W ', 7:' NW'}
     
    def __init__(self,parent,index):

        Button.__init__(self, parent, ui.String(parent, unicode('')), theme.player)
        self._position = index
	del self.children[0]

	ui.String(self,unicode(self._POS[self._position]))
	
	if self.parent._active:
		self.activate()
        
        self.on_click = signal.Signal ()
        self.signal_click.add (self.on_click)
        self.on_click += self.next
        self.set_enable_hitting (True)
        
    def next(self,random):
        self._position = (self._position+1)%self._POS_NUM
             
	if self.parent._active:
	    del self.children[0]
  	    ui.String(self,unicode(self._POS[self._position]))
        
    def update(self, pos):
	self._position = pos

	if self.parent._active:
	    del self.children[0]
  	    ui.String(self,unicode(self._POS[self._position]))

class ComboBox(ui.HBox):
    
    def __init__(self, parent, profiles, menu):
        
	ui.HBox.__init__(self, parent)
	
	self._prof = profiles
	self._index = 0
	self._menu = menu
	self._text = ui.String(self, unicode(self._prof[self._index]))
	self.padding_right = 12
	self.left = widget.Button(self, None,'data/icon/go-previous-small.png', True, theme.menu)
	self.prof_txt = Button(self, self._text, theme.menu)
	self.right = widget.Button(self, None,'data/icon/go-next-small.png', True, theme.menu)

	self.right.on_click = signal.Signal ()
        self.right.signal_click.add (self.right.on_click)
        self.right.on_click += self.next
        self.right.set_enable_hitting (True)

	self.left.on_click = signal.Signal ()
        self.left.signal_click.add (self.left.on_click)
        self.left.on_click += self.prev
        self.left.set_enable_hitting (True)

    def load(self,profiles):
	self._prof = profiles
	self._index = 0
	self._text.set_string(unicode(self._prof[self._index]))
	self._menu.load_profile(self._prof[self._index])

    def next(self,random):
        self._index = (self._index-1)%len(self._prof)
	self._text.set_string(unicode(self._prof[self._index]))
	self._menu.load_profile(self._prof[self._index])  
 
    def prev(self,random):
        self._index = (self._index+1)%len(self._prof)
	self._text.set_string(unicode(self._prof[self._index]))
	self._menu.load_profile(self._prof[self._index])

    def get_text(self):
	return self._text

class MapSelector(ui.HBox):

    def __init__(self, parent = None):

	ui.HBox.__init__(self, parent)
	self._path_img = 'doc/map/small/'
	self._path = 'doc/map/'

	self._listmaps = []
	self.init_list()

	self._num = len(self._listmaps)
	self._index = 0
	self.padding_right = 10

	self.left = widget.Button(self, None,'data/icon/go-previous-small.png', True, theme.menu)
	self._map = widget.Button(self, None, self._path_img + self._listmaps[self._index] + '_small.png', True, theme.menu)
	self.right = widget.Button(self, None,'data/icon/go-next-small.png', True, theme.menu)

	self.right.on_click = signal.Signal ()
        self.right.signal_click.add (self.right.on_click)
        self.right.on_click += self.next
        self.right.set_enable_hitting (True)
	self.right.set_position_rel (1, .1)

	self.left.on_click = signal.Signal ()
        self.left.signal_click.add (self.left.on_click)
        self.left.on_click += self.prev
        self.left.set_enable_hitting (True)
		
    def next(self,random):
        self._index = (self._index+1)%self._num
	self._map.set_image(self._path_img + self._listmaps[self._index] + '_small.png')
 
    def prev(self,random):
        self._index = (self._index-1)%self._num
	self._map.set_image(self._path_img + self._listmaps[self._index] + '_small.png')

    def select(self, new_map):
	img = new_map[len(self._path):-4]
	self._index = self._listmaps.index(img)
	self._map.set_image(self._path_img + self._listmaps[self._index] + '_small.png')

    def get_map(self):
	return self._path + self._listmaps[self._index] + '.xml'

    def init_list(self):
	l = listdir(self._path)
	for i in l:
	    if i[-4:] == '.xml':
		self._listmaps.append(i[:-4])


