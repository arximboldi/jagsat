#
#  Copyright (C) 2009, 2010 JAGSAT Development Team (see below)
#  
#  This file is part of JAGSAT.
#  
#  JAGSAT is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  
#  JAGSAT is distributed in the hope that it will be useful,
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


def prepare_data (world):
    return World (
        phase          = world.phase,
        round          = world.round,
        current_player = world.current_player.name,
        map            = world.map.file_name,
        use_on_move    = world.use_on_move,
        use_on_attack  = world.use_on_attack,
        regions        = map (
            lambda r: Region (name   = r.definition.name,
                              used   = r.used,
                              troops = r.troops,
                              owner  = r.owner.name),
            world.regions.itervalues ()),
        players        = map (
            lambda p: Player (name      = p.name,
                              color     = tuple (*p.color),
                              position  = p.position,
                              mission   = p.mission,
                              cards     = p.cards,
                              conquered = p.conquered)))

def restore_data (data):
    cfg   = ConfNode ({ 'map' : data.map })
    for i, p in enumerate (data.players):
        cfg.child ('player-%i'%i).fill ({
            'enabled'  : True,
            'name'     : p.name,
            'position' : p.position,
            'color'    : sf.Color (*p.color) })

    world = create_game (cfg)
    for dr in data.regions:
        r        = world.regions [dr]
        r.owner  = world.player [dr]
        r.troops = dr.troops
        r.used   = dr.used
        
def load_desc (filename):
    pass

def save_desc (filename):
    pass

def load_data (filename):
    pass

def save_data (filename):
    pass

class Storage (object):
    def __init__ (version = 1, **k):
        self.__dict__.update (k)
        self.version = version

class Region (Storage): pass
class Player (Storage): pass
class World  (Storage): pass
