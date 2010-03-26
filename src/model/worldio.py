#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
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

