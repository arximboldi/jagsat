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

save_game_ext = 'cog'


class WorldIOError (ModelError): pass

def load_game (fname):
    try:
        p = _make_world_unpickler (fname)
        return p.load ()
    except None:
        raise WorldIOError ('Could not load game  %s' + fname) 

def save_game (world, fname):
    try:
        p = _make_world_pickler (fname)
        p.dump (world)
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

def _make_world_pickler (filename):
    p = pickle.Pickler (open (filename, 'wb'))
    p.persistent_id = _persistent_id
    return p

def _make_world_unpickler (filename):
    p = pickle.Unpickler (open (filename, 'rb'))
    p.persistent_load = _persistent_id
    return p

