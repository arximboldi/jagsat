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
from model.world import create_game
from base import signal
from base.log import get_log
from ui.world import WorldComponent

from tf.gfx.widget.basic import Keyboard
from tf.signalslot import Signal
from tf.gfx import uiactions

_log = get_log (__name__)

_TITLE = unicode ('HONOR OF GREED')
_ACTIVE_COLOR = sf.Color.Red
_INACTIVE_COLOR = sf.Color(127,127,127)
_DISABLED_PLAYER = sf.Color(190,190,190)
_BORDER_COLOR = sf.Color.Black
_THICKNESS = 2
_THEME = {'active':_ACTIVE_COLOR,'inactive':_INACTIVE_COLOR,'border':_BORDER_COLOR,'thickness':_THICKNESS}
_THEME2 = {'active':_ACTIVE_COLOR,'inactive':_DISABLED_PLAYER,'border':_BORDER_COLOR,'thickness':_THICKNESS}


class MenuComponent (ui.VBox):
    
    def __init__ (self, parent = None):
        
        ui.VBox.__init__(self, parent)

	self.set_position(50,50)
        
        self._profile = None     # Profile used to create the game
        self._map = 'doc/map/worldmap.xml'   # Path of the selected map
	self._listprof = None    # List of profilessaved on the congifuration file
        #self._map = None        #Uncomment when map_selector will be done

        #Main Layer

        self.titleL = LineEdit(self, ui.String(self, _TITLE) , _ACTIVE_COLOR, _INACTIVE_COLOR, _BORDER_COLOR, _THICKNESS)
        self.profileL = ui.HBox(self)
        self.gameL = ui.HBox(self)
        self.actionL = ui.HBox(self)
	self.statusL = LineEdit(self, ui.String(self, unicode('')) , sf.Color(127,127,127), sf.Color.Black, sf.Color.Black, _THICKNESS)
	self.keyboard = Keyboard(self._layer)
	self.keyboard.set_position(500, 620)
	self.keyboard.set_visible(False)

	#Profile Layer
	self.default_prof()
	self.load_listprof()
	self.profile_ComboBox = ComboBox(self.profileL, self._listprof, self)
        self.profile_SaveButton = Button(self.profileL, ui.String(self.profileL, unicode('Save')), _THEME)
	self.profile_DeleteButton = Button(self.profileL, ui.String(self.profileL, unicode('Delete')), _THEME)

	self.profile_SaveButton.on_click = signal.Signal ()
        self.profile_SaveButton.signal_click.add (self.profile_SaveButton.on_click)
        self.profile_SaveButton.on_click += lambda _: self.save_profile()
        self.profile_SaveButton.set_enable_hitting (True)

        self.profile_DeleteButton.on_click = signal.Signal ()
        self.profile_DeleteButton.signal_click.add (self.profile_DeleteButton.on_click)
        self.profile_DeleteButton.on_click += lambda _: self.delete_profile()
        self.profile_DeleteButton.set_enable_hitting (True)
        

 	#Game Layer
        
        self.infoplayerL = ui.VBox(self.gameL)
        self.mapL = Map_selector(self.gameL)

	#Info Player Layer

	self.playerL1 = ui.HBox(self.infoplayerL)
	self.playerL2 = ui.HBox(self.infoplayerL)
	self.playerL3 = ui.HBox(self.infoplayerL)
	self.playerL4 = ui.HBox(self.infoplayerL)
	self.playerL5 = ui.HBox(self.infoplayerL)
	self.playerL6 = ui.HBox(self.infoplayerL)

	self.playerL1._active = True
	self.playerL2._active = True
	self.playerL3._active = True
	self.playerL4._active = False
	self.playerL5._active = False
	self.playerL6._active = False

	#Player1
        
        self.en_button1 = Button(self.playerL1, ui.String(self.playerL1, unicode('')), _THEME2)
        self.player_name1 = LineEdit(self.playerL1, ui.String(self.playerL1, unicode('Player1')), _ACTIVE_COLOR, _DISABLED_PLAYER, _BORDER_COLOR, _THICKNESS)
        self.player_color1 = ColorButton(self.playerL1, ui.String(self.playerL1, unicode('')), _THEME2, 0)
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

	self.en_button2 = Button(self.playerL2, ui.String(self.playerL2, unicode('')), _THEME2)
        self.player_name2 = LineEdit(self.playerL2, ui.String(self.playerL2, unicode('Player2')), _ACTIVE_COLOR, _DISABLED_PLAYER, _BORDER_COLOR, _THICKNESS)
        self.player_color2 = ColorButton(self.playerL2, ui.String(self.playerL2, unicode('')), _THEME2, 1)
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
        
        self.en_button3 = Button(self.playerL3, ui.String(self.playerL3, unicode('')), _THEME2)
        self.player_name3 = LineEdit(self.playerL3, ui.String(self.playerL3, unicode('Player3')), _ACTIVE_COLOR, _DISABLED_PLAYER, _BORDER_COLOR, _THICKNESS)
        self.player_color3 = ColorButton(self.playerL3, ui.String(self.playerL3, unicode('')), _THEME2, 2)
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

        self.en_button4 = Button(self.playerL4, ui.String(self.playerL4, unicode('')), _THEME2)
        self.player_name4 = LineEdit(self.playerL4, ui.String(self.playerL4, unicode('Player4')), _ACTIVE_COLOR, _DISABLED_PLAYER, _BORDER_COLOR, _THICKNESS)
        self.player_color4 = ColorButton(self.playerL4, ui.String(self.playerL4, unicode('')), _THEME2, 3)
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

        self.en_button5 = Button(self.playerL5, ui.String(self.playerL5, unicode('')), _THEME2)
        self.player_name5 = LineEdit(self.playerL5, ui.String(self.playerL5, unicode('Player5')), _ACTIVE_COLOR, _DISABLED_PLAYER, _BORDER_COLOR, _THICKNESS)
        self.player_color5 = ColorButton(self.playerL5, ui.String(self.playerL5, unicode('')), _THEME2, 4)
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

        self.en_button6 = Button(self.playerL6, ui.String(self.playerL6, unicode('')), _THEME2)
        self.player_name6 = LineEdit(self.playerL6, ui.String(self.playerL6, unicode('Player6')), _ACTIVE_COLOR, _DISABLED_PLAYER, _BORDER_COLOR, _THICKNESS)
        self.player_color6 = ColorButton(self.playerL6, ui.String(self.playerL6, unicode('')), _THEME2, 5)
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
        
        self.start_button = Button(self.actionL, ui.String(self.actionL,unicode('Start')), _THEME)
        self.load_button = Button(self.actionL, ui.String(self.actionL, unicode('Load')), _THEME)

	self.start_button.on_click = signal.Signal ()
        self.start_button.signal_click.add (self.start_button.on_click)
        self.start_button.on_click += self.start_game
        self.start_button.set_enable_hitting (True)

	self.load_button.on_click = signal.Signal ()
        self.load_button.signal_click.add (self.load_button.on_click)
        self.load_button.on_click += self.load_game
        self.load_button.set_enable_hitting (True)

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
                pdic['color'] = pinf.get_child(2)._col
                pdic['position'] = pinf.get_child(3)._position
                pdic['enabled'] = True
                dic['player-' + str(i)] = pdic
                    
        dic['map'] = self._map
        
        self._profile.fill(dic)   

    def default_prof(self):
        cfg = ConfNode (
            { 'player-0' :
              { 'name'     : 'Player1',
                'color'    : 0,
                'position' : 0,
                'enabled'  : True },
              'player-1' :
              { 'name'     : 'Player2',
                'color'    : 1,
                'position' : 1,
                'enabled'  : True },
              'player-2' :
              { 'name'     : 'Player3',
                'color'    : 2,
                'position' : 2,
                'enabled'  : True },
              'map' : 'doc/map/worldmap.xml' })

        GlobalConf ().path('profiles').adopt(cfg, 'Default')	
	

    def load_listprof(self):
	l = []
	for i in GlobalConf ().path('profiles')._childs :
	     l.append(i)
	self._listprof = l           
            
    def load_profile(self, name):
	
	for i in range(0,6):
	    self.disable_player(i)	
	
        index = 0
	
	for i in GlobalConf ().path('profiles').path(str(name)).childs() :
	    aux = self.infoplayerL.get_child(index)
	    
	    if i._name <> 'map':
		self.enable_player(index)

	    for j in i.childs() :

		if j._name == 'color': 
		    aux.get_child(2).update(j.get_value()) 

		elif j._name == 'position':
		    aux.get_child(3).update(j.get_value())

		elif j._name == 'name':
		    del aux.get_child(1).children[0]
		    ui.String(aux.get_child(1), unicode(j.get_value()))

	    index = index + 1
	
    
    def save_profile(self, name = 'Prove'): 
        
        if self.check_info() and name <> 'Default':
            self.create_profile()
	    GlobalConf ().path ('profiles').adopt (self._profile, name)
	    self._listprof.append(name)
	    self.profile_ComboBox.load(self._listprof)
	    
	    self.update_status("Profile saved")

	else:
	    self.update_status("Wrong information")

    def delete_profile(self, name = 'Prove'):   
	
	if name <> 'Default': 
	    GlobalConf ().path('profiles').remove(name)
	    self._listprof.remove(name)
	    self.profile_ComboBox.load(self._listprof)
	    self.update_status("Profile deleted")

        
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

	if self._map == None:
	    return False
        
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
    
    def start_game(self, random):
        if self.check_info():
            self.create_profile()


	    self.update_status("New game")

        else:
	    self.update_status("Wrong information")


    def load_game(self, random):

	self.update_status("Not implemented yet")

    def update_status(self, str):
	
	del self.statusL.children[0]
  	ui.String(self.statusL,unicode(str))

    def enable_keyboard(self,pl):

	if self.keyboard.get_visible():
	    self.keyboard.set_position(500, 620)
	else:
	    self.keyboard.set_visible(True)

	

#  Extra Widgets

class ColorButton(Button):
    _COLOR_NUM = 6
    _COLOR = {0: sf.Color.White, 1: sf.Color.Blue, 2: sf.Color.Red, 3: sf.Color.Yellow, 4: sf.Color.Green, 5: sf.Color.Magenta}

    
    def __init__(self, parent, str, theme, index):
        
        Button.__init__(self, parent, str, theme)
        self._col = index
        self.active_color = self._COLOR[index]
	if self.parent._active:
		self.activate()
        
        self.on_click = signal.Signal ()
        self.signal_click.add (self.on_click)
        self.on_click += self.next
        self.set_enable_hitting (True)
        
    def next(self,random):
        self._col = (self._col+1)%self._COLOR_NUM
        self.active_color = self._COLOR[self._col]
	if self.parent._active:
	    self.activate()

    def update(self,col):
	self._col = col
	self.active_color = self._COLOR[self._col]
	if self.parent._active:
	    self.activate()
               
    
class PositionButton(Button):
    _POS_NUM = 8
    _POS = {0: "  N ", 1: ' NE', 2:'  E ', 3: ' SE', 4:'  S ', 5:' SW', 6:'  W ', 7:' NW'}
     
    def __init__(self,parent,index):

        Button.__init__(self, parent, ui.String(parent, unicode('')), _THEME2)
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

	self.left = Button(self, ui.String(self, unicode('<')), _THEME)
	self.prof_txt = Button(self, ui.String(self, unicode(self._prof[self._index])), _THEME)
	self.right = Button(self, ui.String(self, unicode('>')), _THEME)

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
	del self.prof_txt.children[0]
	ui.String(self.prof_txt,unicode(self._prof[self._index]))
	self._menu.load_profile(self._prof[self._index])

    def next(self,random):
        self._index = (self._index-1)%len(self._prof)
	del self.prof_txt.children[0]
	ui.String(self.prof_txt,unicode(self._prof[self._index]))
	self._menu.load_profile(self._prof[self._index])  
 
    def prev(self,random):
        self._index = (self._index+1)%len(self._prof)
	del self.prof_txt.children[0]
	ui.String(self.prof_txt,unicode(self._prof[self._index])) 
	self._menu.load_profile(self._prof[self._index])

class Map_selector():
    
    def __init__(self, parent = None):
        pass

