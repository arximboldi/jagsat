#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base.log import get_log

_log = get_log (__name__)


def create_missions (world):
    """
    Given a world object, creates all the missions appropiate for its
    map and players.
    """
    return MissionCreator (world).missions


class MissionCreator (object):
    
    def __init__ (self, world = None, *a, **k):
        assert world
        super (MissionCreator, self).__init__ (*a, **k)

        self._missions = []
        self.map = world.map
        self.players = world.ordered_players ()
        self.n = len (self.map.regions)

        self.create_player_missions ()
        self.create_country_missions ()
        self.create_continent_missions ()

    @property
    def missions (self):
        return self._missions

    def create_player_missions (self):
        """
        Mission: kill any of the other players
            - kill_other_player missions uses 'player' as key
            - Generates one mission per player
            - Adds default mission
        """
        for p in self.players:
            self._missions.append (Mission ({'player' : p},\
                                                [self.n*57/100, 1]))

    def create_country_missions (self):
        """
        - Mission 1: to conquer 57% of map regions with at least one 
        single troop per region
        - Mission 2: to conquer 43% of map regions with at least 2 troops
        in each region
        """
        self._missions.append (Mission ({'region' : self.n*57/100}, 1))
        self._missions.append (Mission ({'region' : self.n*43/100}, 2))

    def create_continent_missions (self):
        """
        Possible continent missions will include a list of continents which
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
                    _log.debug ("Generated mission[2]: "+\
                                 continents[i].name+" "+\
                                 continents[j].name)

                    l = [continents[i], continents[j]]
                    self._missions.append (Mission ({'continent' : l}))

                elif sum < min:
                    for k in range(j+1, len(continents)):
                        sum2 = sum + len(continents[k].regions)
                        
                        if sum2 > min and sum2 < max:
                            _log.debug ("Generated mission[3]: "+\
                                         continents[i].name+" "+\
                                         continents[j].name+" "+\
                                         continents[k].name)
                            l = [continents[i],continents[j],continents[k]]
                            self._missions.append (Mission (\
                                                    {'continent' : l})) 


class Mission (object):
    """
    There are three type of missions {continent, country, player}:
        - continent     -> goal is a list of continents to conquer
        - region        -> goal is a number of regions
        - player        -> player is the name of the player
    The extra parameter refers to special issues in some missions
    """
    def __init__ (self,
                  mission = None,
                  extra = None,
                  *a, **k):
        assert mission
        if extra:
            self.extra = True
        else:
            self.extra = False
        super (Mission, self).__init__ (*a, **k)

        # Primary type and goal
        self.type = mission.keys()[0]
        self.goal = mission.values()[0]
        # Extra information to acomplish the mission
        if self.extra:
            self.info = extra

        # Dictionary of missions
        self.mission = mission       
        if self.is_player ():
            self.add_default_mission ()

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

    def add_default_mission (self):
        """
        When a player has to kill himself or a death player, he will
        have to acomplish the default mission which is to conquer
        57% of the total regions.
        """
        # Add to mission dictionary the number of regions
        self.mission['region'] = self.info.pop(0)

        # Stores in info the number of troops per region to acomplish
        # 'region' mission
        self.info = self.info [0]

    def check_mission (self, gworld):
        if self.is_player ():
            success = self.check_mission_player (gworld)
        if self.is_region ():
            success = self.check_mission_region (gworld)
        if self.is_continent ():
            success = self.check_mission_continent (gworld)

        return success

    def pre_check_mission (self, gworld):
        # Check if the player-to-kill is alive
        if self.is_player ():
            world = gworld
            alive = False
            # TODO: Player life test should be make elsewhere and stored.
            for r in world.regions.itervalues ():
                if r.owner.position == self.goal.position:
                    alive = True
            # If the player-to-kill is dead removes that mission
            if not alive or\
               world.current_player.position == self.goal.position:
                self.mission.pop('player')
                self.type = self.mission.keys()[0]
                self.goal = self.mission.values()[0]

    def check_mission_player (self, gworld):
        world = gworld
        success = True

        for r in world.regions.itervalues ():
            # If our player-to-kill has a region we didn't succeded
            if r.owner.position == self.goal.position:
                success = False
        return success


    def check_mission_region (self, gworld):
        success = False
        world = gworld

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

    def check_mission_continent (self, gworld):
        world = gworld
        success = True

        # Get list of regions player owns
        regions = filter (lambda r: r.owner == world.current_player,\
                        world.regions.values ())

        # Foreach continent I have to conquer
        for c in self.goal:
            # Check if the player has all the regions in that continent
            if len(c.regions) != len (filter (
                lambda r:r.definition.continent.name == c.name, regions)):
                success = False
        
        return success

    @property
    def description (self):
        return self.str_mission ()
    
    def str_mission (self):
        if self.is_player ():
            mission_str = "Eliminate player:\n"
            mission_str += self.goal.name
            mission_str += ".\nIf that player is dead,\nconquer "
            mission_str += str (self.mission['region'])
            mission_str += " regions\nwith at least "
            mission_str += str (self.info)
            mission_str += " troops\non each"

        if self.is_region ():
            mission_str = "Conquer "
            mission_str += str(self.mission['region'])
            mission_str += " regions\nwith at least "
            mission_str += str(self.info)
            mission_str += " troops\non each"

        if self.is_continent ():
            mission_str = "Conquer\n"+self.goal[0].name
            for i in range (1,len(self.goal)):
                if i < len(self.goal)-1:
                    mission_str += ",\n"+self.goal[i].name
                else:
                    mission_str += "\nand\n"+self.goal[i].name

        return mission_str
