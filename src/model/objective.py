#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base.log import get_log
from world import create_game
from base.conf   import ConfNode

_log = get_log (__name__)

# This ConfNode is here just for testing issues
# TODO: delete this cfg = ...
cfg = ConfNode (
            { 'player-0' :
              { 'name'     : 'jp',
                'color'    : (255, 0, 0),
                'position' : 2,
                'enabled'  : True },
              'player-2' :
              { 'name'     : 'pj',
                'color'    : (0, 255, 0),
                'position' : 4,
                'enabled'  : True },
              'map' : '../doc/map/worldmap.xml' })

def create_objectives (cfg):
    """
    Creates a list of objectives from a ConfNode containing the 
    following childs:
      - player-X: with X \in [0, 5], contains the properties for
        player number X. See create_player.
      - map: Contains the path to the map file.
    """
    world = create_game (cfg)
    return Objective (world)
    
class Objective (object):
    
    def __init__ (self, world = None, *a, **k):
        assert world
        super (Objective, self).__init__ (*a, **k)

        self._objectives = []
        self.map = world.map
        self.players = world.ordered_players ()
        self.n = len (self.map.regions)

        self.create_player_objectives ()
        self.create_country_objectives ()
        self.create_continent_objectives ()

    @property
    def objectives (self):
        return self._objectives

    def create_player_objectives (self):
        """
        Objective: kill any of the other players
            - kill_other_player objectives uses 'player' as key
            - Generates one objective per player
            - Adds default objective
        """
        for p in self.players:
            self._objectives.append (ObjectiveDef ({'player' : p},\
                                                [self.n*57/100, 1]))

    def create_country_objectives (self):
        """
        - Objective 1: to conquer 57% of map regions with at least one 
        single troop per region
        - Objective 2: to conquer 43% of map regions with at least 2 troops
        in each region
        """
        self._objectives.append (ObjectiveDef ({'region' : self.n*57/100}, 1))
        self._objectives.append (ObjectiveDef ({'region' : self.n*43/100}, 2))

    def create_continent_objectives (self):
        """
        Possible continent objectives will include a list of continents which
        sum of regions should be between 35% and 43% of the total number
        of regions
        """
        continents = self.map.continents.values ()

        # Get max/min bounds
        min = self.n * 35 / 100
        max = self.n * 43 / 100

        for i in range (len (continents)):
            for j in range (i+1, len (continents)):
                sum = len (continents[i].regions) +\
                      len (continents[j].regions)
                
                if sum > min and sum < max:
                    _log.debug ("Generated objective[2]: "+\
                                 continents[i].name+" "+\
                                 continents[j].name)

                    l = [continents[i], continents[j]]
                    self._objectives.append (ObjectiveDef ({'continent' : l}))

                elif sum < min:
                    for k in range(j+1, len(continents)):
                        sum2 = sum + len(continents[k].regions)
                        
                        if sum2 > min and sum2 < max:
                            _log.debug ("Generated objective[3]: "+\
                                         continents[i].name+" "+\
                                         continents[j].name+" "+\
                                         continents[k].name)
                            l = [continents[i],continents[j],continents[k]]
                            self._objectives.append (ObjectiveDef (\
                                                    {'continent' : l})) 


class ObjectiveDef (object):
    """
    There are three type of objectives {continent, country, player}:
        - continent     -> goal is a list of continents to conquer
        - region        -> goal is a number of regions
        - player        -> player is the name of the player
    The extra parameter refers to special issues in some objectives
    """
    def __init__ (self,
                  objective = None,
                  extra = None,
                  *a, **k):
        assert objective
        if extra:
            self.extra = True
        else:
            self.extra = False
        super (ObjectiveDef, self).__init__ (*a, **k)

        # Primary type and goal
        self.type = objective.keys()[0]
        self.goal = objective.values()[0]
        # Extra information to acomplish the objective
        if self.extra:
            self.info = extra

        # Dictionary of objectives
        self.objective = objective       
        if self.is_player ():
            self.add_default_objective ()

    def is_player (self):
        if self.type == 'player':
            return True
        else:
            return False

    def is_continent (self):
        if self.type == 'continent':
            return True
        else:
            return False

    def is_region (self):
        if self.type == 'region':
            return True
        else:
            return False

    def has_extra (self):
        return self.extra

    def add_default_objective (self):
        """
        When a player has to kill himself or a death player, he will
        have to acomplish the default objective which is to conquer
        57% of the total regions.
        """
        # Add to objective dictionary the number of regions
        self.objective['region'] = self.info.pop(0)

        # Stores in info the number of troops per region to acomplish
        # 'region' objective
        self.info = self.info [0]

    def check_objective (self, game):
        if self.is_player ():
            success = self.check_objective_player (game)
        if self.is_region ():
            success = self.check_objective_region (game)
        if self.is_continent ():
            success = self.check_objective_continent (game)

        return success

    def check_if_alive (self, game):
        # Check if the player-to-kill is alive
        if self.is_player ():
            world = game.world
            alive = False
            for r in world.regions.itervalues ():
                if r.owner.position == self.goal.position:
                    alive = True
            # If the player-to-kill is dead removes that mission
            if not alive:
                self.objective.pop['player']
                self.type = self.objective.keys()[0]
                self.goal = self.objective.values()[0]

    def check_objective_player (self, game):
        world = game.world
        success = True
        for r in world.regions.itervalues ():
            # If our player-to-kill has a region we didn't succeded
            if r.owner.position == self.goal.position:
                success = False
        return success


    def check_objective_region (self, game):
        success = False
        world = game.world

        # Get list of regions player owns
        regions = filter (lambda r: r.owner == world.current_player,\
                        world.regions.values ())

        # Check we have all the regions needed 
        if len (regions) >= self.goal:
            i = 0
            # Count how many regions don't have enough troops
            for r in regions:
                if r.troops < self.info: 
                    i += 1
            # Check if the mission is acomplish
            if len(regions) - i >= self.goal:
                success = True 

        return success

    def check_objective_continent (self, game):
        wold = game.world
        success = True

        # Get list of regions player owns
        regions = filter (lambda r: r.owner == world.current_player,\
                        world.regions.values ())

        # Foreach continent I have to conquer
        for c in self.goal:
            # Check if the player has all the regions in that continent
            if len(c.regions) != len (filter (lambda r: r.continent == c,\
                                                regions)):
                success = False

        return success
    
    def str_objective (self):
        if self.is_player ():
            objective_str = "Eliminate player "
            objective_str += self.goal.name
            objective_str += ". If that player is dead, conquer "
            objective_str += str (self.objective['region'])
            objective_str += " regions with at least "
            objective_str += str (self.info)
            objective_str += " troops on each"

        if self.is_region ():
            objective_str = "Conquer "
            objective_str += str(self.objective['region'])
            objective_str += " regions with at least "
            objective_str += str(self.info)
            objective_str += " troops on each"

        if self.is_continent ():
            objective_str = "Conquer "+self.goal[0].name
            for i in range (1,len(self.goal)):
                if i < len(self.goal)-1:
                    objective_str += ", "+self.goal[i].name
                else:
                    objective_str += " and "+self.goal[i].name

        return objective_str