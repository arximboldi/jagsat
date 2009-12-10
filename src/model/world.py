#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base.changer import InstChanger
from base.observer import make_observer
from map import load_map


def create_game (cfg):
    """
    Creates a game from a ConfNode containing the following childs:
      - player-X: with X \in [0, 5], contains the properties for
        player number X. See create_player.
      - map: Contains the path to the map file.
    """
    
    players = []
    for i in range (0, 6):
        pcfg = cfg.child ('player-' + str (i))
        if pcfg.child ('enabled').value:
            players.append (create_player (pcfg))

    map_ = load_map (cfg.child ('map').value)
    
    return World (map_, players)


def create_player (cfg):
    """
    Creates a player from a ConfNode containing the following childs:
      - color: The color of the player.
      - position: The position of the player.
    """
    return Player (cfg.child ('name').value,
                   cfg.child ('color').value,
                   cfg.child ('position').value)


class World (object):

    def __init__ (self, map_ = None, players = None, *a, **k):
        assert map_
        super (World, self).__init__ (*a, **k)

        self.map     = map_
        self._players = {} if players is None \
                           else dict ((p.name, p) for p in players)
        self._regions = dict ((r.name, Region (r)) for r in map_.regions.itervalues ())
        
    def region (self, name):
        return self._regions [name]

    def iterregions (self):
        return self._regions.itervalues ()


RegionSubject, RegionListener = \
    make_observer (['on_set_region_troops',
                    'on_set_region_used',
                    'on_set_region_owner'],
                   'Region', __name__)

class Region (RegionSubject):
    
    troops = InstChanger ('on_set_region_troops', 0)
    used   = InstChanger ('on_set_region_used', 0)
    owner  = InstChanger ('on_set_region_owner')
    
    def __init__ (self, definition = None, *a, **k):
        assert definition
        super (Region, self).__init__ (*a, **k)
        
        self.definition = definition

PlayerSubject, PlayerListener = \
    make_observer (['on_set_player_troops'])

class Player (PlayerSubject):

    troops = InstChanger ('on_set_player_troops', 0)
    
    def __init__ (self,
                  name = 'Unnamed',
                  color = None,
                  position = None,
                  objective = None,
                  *a, **k):
        super (Player, self).__init__ (*a, **k)
                
        self.name       = name
        self.color      = color
        self.position   = position
        self.objective  = None
        self.cards      = []

