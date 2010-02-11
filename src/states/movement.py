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
from model.world import Region
from ui.world import RegionComponent
from model.map import RegionDef
from model.map import MapContentHandler

ui2 = intermediate

THEME = { 'active' : sf.Color.Blue,
          'inactive' : sf.Color.Red, 
          'border' : sf.Color.Green,
          'thickness' : 2 }

class Movement (State):
    
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
	self.regions = comp._regions
	

	#self.regions = comp._regions   

	for x in comp._regions:
        	x.on_click += lambda ev, x=x: self.set_reference_region ( x )
		
		print (x)

		
		#x._fill_color = sf.Color (255, 255, 255)
		#x._rebuild_sprite ()		
	#for y in comp._RegionDef:
		#pass	

#Still need to separate clicks and complete other funcitons aswell

    def set_reference_region(self,x):
    	print ("This is the reference region")
	x._fill_color = sf.Color (255, 255, 255)
	x._rebuild_sprite ()	
	
	if x.model.definition in x.model.definition.neighbours:
   		print "We are neighbours!"
	else:
  		print "Too far man!" 



	#print ("Region neighbours are:" + region.model.definition.neighbours)

	#self.regions.neighbours	

	print (x)
	#print ("X.name " + x.name)
	
    def move_troops(ra,rb,n):
	if can_move_troops(ra,rb,n): 
		do_move_troops(ra,rb,n)
	else:
		#Show message 	
		print("Show message")
		

    def can_move_troops(ra,rb,n):
	self._do_link_line	

	pass

    def do_move_troops(ra,rb,n):
	pass


	




