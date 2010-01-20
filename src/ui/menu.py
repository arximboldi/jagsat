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
from base.conf import ConfNode
from model.world import create_game
from base import signal
from base.log import get_log
from ui.world import WorldComponent

_log = get_log (__name__)

_TITLE = unicode ('Title of the Game')
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
        #self._map = None        #Uncomment when map_selector will be done

        #Main Layer

        self.titleL = LineEdit(self, ui.String(self, _TITLE) , _ACTIVE_COLOR, _INACTIVE_COLOR, _BORDER_COLOR, _THICKNESS)
        self.profileL = ui.HBox(self)
        self.gameL = ui.HBox(self)
        self.actionL = ui.HBox(self)
	self.statusL = LineEdit(self, ui.String(self, unicode('')) , sf.Color(127,127,127), sf.Color.Black, sf.Color.Black, _THICKNESS)

	#Profile Layer

	self.profile_ComboBox = ComboBox(self.profileL)
        self.profile_SaveButton = Button(self.profileL, ui.String(self.profileL, unicode('Save')), _THEME)
	self.profile_DeleteButton = Button(self.profileL, ui.String(self.profileL, unicode('Delete')), _THEME)

	self.profile_SaveButton.on_click = signal.Signal ()
        self.profile_SaveButton.signal_click.add (self.profile_SaveButton.on_click)
        self.profile_SaveButton.on_click += self.save_profile
        self.profile_SaveButton.set_enable_hitting (True)

        self.profile_DeleteButton.on_click = signal.Signal ()
        self.profile_DeleteButton.signal_click.add (self.profile_DeleteButton.on_click)
        self.profile_DeleteButton.on_click += self.delete_profile
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
        self.en_button1.on_click += self.enable_player
        self.en_button1.set_enable_hitting (True)

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
        self.en_button2.on_click += self.enable_player
        self.en_button2.set_enable_hitting (True)
	
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
        self.en_button3.on_click += self.enable_player
        self.en_button3.set_enable_hitting (True)
        
	#Player4

        self.en_button4 = Button(self.playerL4, ui.String(self.playerL4, unicode('')), _THEME2)
        self.player_name4 = LineEdit(self.playerL4, ui.String(self.playerL4, unicode('Player4')), _ACTIVE_COLOR, _DISABLED_PLAYER, _BORDER_COLOR, _THICKNESS)
        self.player_color4 = ColorButton(self.playerL4, ui.String(self.playerL4, unicode('')), _THEME2, 3)
        self.player_pos4 = PositionButton(self.playerL4, 3)

	self.en_button4.on_click = signal.Signal ()
        self.en_button4.signal_click.add (self.en_button4.on_click)
        self.en_button4.on_click += self.enable_player
        self.en_button4.set_enable_hitting (True)
        
	#Player5

        self.en_button5 = Button(self.playerL5, ui.String(self.playerL5, unicode('')), _THEME2)
        self.player_name5 = LineEdit(self.playerL5, ui.String(self.playerL5, unicode('Player5')), _ACTIVE_COLOR, _DISABLED_PLAYER, _BORDER_COLOR, _THICKNESS)
        self.player_color5 = ColorButton(self.playerL5, ui.String(self.playerL5, unicode('')), _THEME2, 4)
        self.player_pos5 = PositionButton(self.playerL5,4)

	self.en_button5.on_click = signal.Signal ()
        self.en_button5.signal_click.add (self.en_button5.on_click)
        self.en_button5.on_click += self.enable_player
        self.en_button5.set_enable_hitting (True)
        
	#Player6

        self.en_button6 = Button(self.playerL6, ui.String(self.playerL6, unicode('')), _THEME2)
        self.player_name6 = LineEdit(self.playerL6, ui.String(self.playerL6, unicode('Player6')), _ACTIVE_COLOR, _DISABLED_PLAYER, _BORDER_COLOR, _THICKNESS)
        self.player_color6 = ColorButton(self.playerL6, ui.String(self.playerL6, unicode('')), _THEME2, 5)
        self.player_pos6 = PositionButton(self.playerL6, 5)

	self.en_button6.on_click = signal.Signal ()
        self.en_button6.signal_click.add (self.en_button6.on_click)
        self.en_button6.on_click += self.enable_player
        self.en_button6.set_enable_hitting (True)

	
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
	#self.load_button.on_click += self.enable_aux
        self.load_button.set_enable_hitting (True)


    #It creats a profile from the active information of the main menu

    def create_profile(self,name="Default"): 
        
        self._profile = ConfNode()
        dic = {}
        for i in range(0,6):
            pinf = self.infoplayerL.get_child(i)
            if pinf._active:
                pdic = {}
                pdic['name'] = pinf.get_child(1).get_child(0)
                pdic['color'] = pinf.get_child(2)._col
                pdic['position'] = pinf.get_child(3)._position
                pdic['enabled'] = True
                dic['player-' + str(i)] = pdic
                    
        dic['map'] = self._map
        
        self._profile.fill(dic)
                    
            
    def load_profile(self):
        pass
    
    def save_profile(self, random):
        
        if self.check_info():
            self.create_profile()
	    self.update_status("It should save the profile")

	else:
	    self.update_status("Wrong information")

    def delete_profile(self, random):

	self.update_status("It should eliminate the profile")

        
    def enable_player(self, random):
	for i in range (0,6):  
	    aux = self.infoplayerL.get_child(i)
	    for j in range (0,4):
		if aux._active:
		    aux.get_child(j).activate()
		else:
		    aux.get_child(j).deactivate()

    def enable_aux(self, random):
	if self.playerL1._active:
	    self.playerL1._active = False
	else:
	    self.playerL1._active = True
    
    #Verify the information on the main menu in order to create a profile without mistakes    

    def check_info(self):  

        lname = []
        lcol = []
        lpos = []

	if self._map == None:
	    return False
        
        for i in range(0,6):
            pinf = self.infoplayerL.get_child(i)
            if pinf._active:
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
                
        return True
    
    def start_game(self, random):
        if self.check_info():
            self.create_profile()

	    world = create_game (self._profile)
	    view = self._layer.get_view()
	    layer = ui.Layer(view)
            comp = WorldComponent (layer, world)

	    self.update_status("New game")

        else:
	    self.update_status("Wrong information")


    def load_game(self, random):

	self.update_status("It should open a new window in order to load the game")

    def update_status(self, str):
	
	del self.statusL.children[0]
  	ui.String(self.statusL,unicode(str))



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
        
 

class ComboBox():
    
    def __init__(self, parent = None):
        pass 
    
    
class Map_selector():
    
    def __init__(self, parent = None):
        pass

