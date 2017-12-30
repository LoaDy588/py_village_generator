import random
import utils


class Map_gen:
    def __init__(self):
        # default values
        self.GRID_X = 20
        self.GRID_Y = 20
        self.VILLAGE_SIZE = 10
        self.FOREST_COUNT = 1
        self.FOREST_SIZE = 200
        self.RIVER = True
        self.CASTLE = True
        self.CASTLE_SIZE = 3
        self.map = []

        # village and castle points for path finding purposes
        self.__castle_points = []
        self.__village_points = []

        # create empty map
        for x in range(self.GRID_X):
            temp = []
            for y in range(self.GRID_Y):
                temp.append({"forest": False, "village": False, "castle": False,
                             "river": False, "road": False})
            self.map.append(temp)

    def clear_map(self):
        """Clear stored map data."""
        self.map = []
        for x in range(self.GRID_X):
            temp = []
            for y in range(self.GRID_Y):
                temp.append({"forest": False, "village": False, "castle": False,
                             "river": False, "road": False})
            self.map.append(temp)

    def create_map(self):
        """Create map."""
        if self.RIVER:
            self.__create_river()
        if self.CASTLE:
            self.__create_castle()
        self.__create_village()
#        self.__create_roads()  # might support in future
        for i in range(self.FOREST_COUNT):
            self.__create_forest()

        return self.map

    def __create_river(self):
        """
        Create random river going from edge to edge on a map.

        Private method.
        """
        # pick random direction
        directions = {"E": (1, 0), "N": (0, 1), "W": (-1, 0), "S": (0, -1)}
        dir_rand = "NSEW"[random.randint(0, 3)]
        direction = directions[dir_rand]
        river_points = []

        # pick random start point of the river
        if dir_rand == "E":
            start = (0, random.randint(1, self.GRID_Y-2))
            max_length = self.GRID_X
        elif dir_rand == "N":
            start = (random.randint(1, self.GRID_X-2), 0)
            max_length = self.GRID_Y
        elif dir_rand == "W":
            start = (self.GRID_X-1, random.randint(1, self.GRID_Y-2))
            max_length = self.GRID_X
        elif dir_rand == "S":
            start = (random.randint(1, self.GRID_X-2), self.GRID_Y-1)
            max_length = self.GRID_Y

        # generate river
        side_step = 0
        current = start
        for i in range(1, max_length+1):
            river_points.append(current)
            # stop generation if river touches edge
            if (current[0] == self.GRID_X-1 or current[0] == 0) and i != 1:
                break
            if (current[1] == self.GRID_Y-1 or current[1] == 0) and i != 1:
                break
            # calculate next point
            side_step = random.randint(-1, 1)
            if dir_rand == "E" or dir_rand == "W":
                current = (current[0]+direction[0], current[1]+side_step)
            elif dir_rand == "N" or dir_rand == "S":
                current = (current[0]+side_step, current[1]+direction[1])

        # put river points on map
        for point in river_points:
            self.map[point[0]][point[1]]["river"] = True

    def __create_castle(self):
        """
        Randomly place a castle in a map.

        Private method.
        """
        # find a random origin point which doesn't sit on a river
        start_x = random.randint(0, self.GRID_X-1)
        start_y = random.randint(0, self.GRID_Y-1)
        while self.map[start_x][start_y]["river"]:
            self.__create_castle()
            return

        # create endpoint.
        end_x = start_x + self.CASTLE_SIZE - 1
        end_y = start_y + self.CASTLE_SIZE - 1

        # test if castle sits in the field and not on river
        if start_x > self.GRID_X-1 or start_y > self.GRID_Y-1:
            self.__create_castle()
            return
        if end_x > self.GRID_X-1 or end_y > self.GRID_Y-1:
            self.__create_castle()
            return
        if self.map[end_x][end_y]["river"]:
            self.__create_castle()
            return

        # get points of the castle and put them on map
        castle_points = utils.get_rectangle((start_x, start_y), (end_x, end_y))
        for point in castle_points:
            # start again if river inside castle
            if self.map[point[0]][point[1]]["river"]:
                self.__create_castle()
                return

        for point in castle_points:
            self.map[point[0]][point[1]]["castle"] = True

    def __create_village(self):
        """
        Create randomly shaped, randomly placed village in a map.

        Private method.
        """
        # find suitable random start point for village
        start_x = random.randint(0, self.GRID_X-1)
        start_y = random.randint(0, self.GRID_Y-1)
        if self.map[start_x][start_y]["river"]:
            self.__create_village()
            return
        while self.map[start_x][start_y]["castle"]:
            self.__create_village()
            return

        # generate points of village
        village_points = []
        for i in range(self.VILLAGE_SIZE):
            if i == 0:
                village_points.append((start_x, start_y))
            else:
                # get neighbors of current points and pick random suitable
                neighbors = utils.get_neighbors(village_points,
                                                (self.GRID_X, self.GRID_Y))
                point = neighbors[random.randint(0, len(neighbors)-1)]
                while self.map[point[0]][point[1]]["river"]:
                    point = neighbors[random.randint(0, len(neighbors)-1)]
                    neighbors.remove(point)
                while self.map[point[0]][point[1]]["castle"]:
                    point = neighbors[random.randint(0, len(neighbors)-1)]
                    neighbors.remove(point)
                village_points.append(point)

        # put village points on map
        for point in village_points:
            self.map[point[0]][point[1]]["village"] = True

    def __create_forest(self):
        """
        Create randomly shaped, randomly placed forest in a map.

        Private method.
        """
        # find suitable start point
        start_x = random.randint(0, self.GRID_X-1)
        start_y = random.randint(0, self.GRID_Y-1)
        if self.map[start_x][start_y]["castle"]:
            self.__create_forest()
            return

        # generate points of forest
        forest_points = []
        for i in range(self.FOREST_SIZE):
            if i == 0:
                forest_points.append((start_x, start_y))
            else:
                # get neighbors of current points and pick random suitable one
                neighbors = utils.get_neighbors(forest_points,
                                                (self.GRID_X, self.GRID_Y))
                point = neighbors[random.randint(0, len(neighbors)-1)]
                while self.map[point[0]][point[1]]["castle"]:
                    point = neighbors[random.randint(0, len(neighbors)-1)]
                    neighbors.remove(point)
                while self.map[point[0]][point[1]]["village"]:
                    point = neighbors[random.randint(0, len(neighbors)-1)]
                    neighbors.remove(point)
                forest_points.append(point)

        # put points on map
        for point in forest_points:
            self.map[point[0]][point[1]]["forest"] = True
