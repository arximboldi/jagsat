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

"""
Note that
"""

from PySFML    import sf
from world     import create_game
from base.conf import ConfNode
from error     import ModelError
import pickle
import pprint

save_game_ext = 'cog'

class WorldIOError (ModelError): pass

def load_game (fname):
    try:
        fpick = open (fname, 'r')
        p = _make_world_unpickler (fpick)
        ret = p.load ()
        fpick.close ()
        return ret
    except None:
        raise WorldIOError ('Could not load game  %s' + fname) 

def save_game (world, fname):
    try:
        fpick = open (fname, 'w')
        p = _make_world_pickler (fpick)
        p.dump (world)
        fpick.close ()
    except None:
        raise WorldIOError ('Could not load game: %s' + fname) 

def _persistent_id (obj):
    if isinstance (obj, sf.Color):
        return 'sf.Color:%i,%i,%i,%i' % (obj.r, obj.g, obj.b, obj.a)
    return None

def _persistent_load (pid):
    if pid [:9] == "sf.Color:":
        return sf.Color (*map (int, pid [9:].split (',')))
    raise pickle.UnpicklingError, 'Invalid persistent id'

def _make_world_pickler (file):
    p = pickle.Pickler (file)
    p.persistent_id = _persistent_id
    return p

def _make_world_unpickler (file):
    p = pickle.Unpickler (file)
    p.persistent_load = _persistent_id
    return p

