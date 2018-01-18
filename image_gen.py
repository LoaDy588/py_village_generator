from PIL import Image, ImageDraw
import random
import utils

class Image_gen:
    def __init__(self):
        # default values
        self.IMG_SIZE = (800, 800)
        self.COLORS = {
                       "grass": (65, 152, 10),
                       "tree": (3, 114, 0),
                       "road": (238, 182, 70),
                       "river": (37, 108, 155),
                       "house": (91, 70, 17),
                       "castle0": (117, 117, 117),
                       "castle1": (175, 175, 175)
                      }
        self.COLOR_VARIATION = 10
        self.CASTLE_TOWER_SIZE = 20
        self.CASTLE_WALL_THICKNESS = 6
        self.RIVER_WIDTH = 10
        self.ROAD_WIDTH = 3
        self.TREE_SIZE = 7
        self.HOUSE_SIZE = 7
        self.FOREST_DENSITY = 24
        self.VILLAGE_DENSITY = 5
        self.CELL_ORIGINS = []
        self.GRID = (0, 0)
        self.CELL_X = 0
        self.CELL_Y = 0
        self.MAP = []
        self.GRID_LINES = True

    def draw_map(self, map_data, output):
        """
        Create image from map data.

        ARGUMENTS:
        map_data - map data from Map_gen
        output - output file for image
        """
        # calculate cell origins and size, setup map
        self.GRID = (len(map_data), len(map_data[0]))
        self.__calculate_cells()
        self.MAP = map_data

        # setup image
        img = Image.new('RGB', self.IMG_SIZE, self.COLORS["grass"])
        draw = ImageDraw.Draw(img)

        # draw every cell
        for x in range(self.GRID[0]):
            for y in range(self.GRID[1]):
                self.__draw_cell(draw, img, x, y)
        if self.GRID_LINES:
            self.__grid(draw)
        img.save(output)

    def __draw_cell(self, draw, img, x, y):
        """
        Draw cell. Private.

        Calls respective function to draw each variant. Variants can be layered,
        depends on map generator.
        """
        if self.MAP[x][y]["river"]:
            self.__river(draw, x, y)
        if self.MAP[x][y]["castle"]:
            self.__castle(draw, x, y)
        if self.MAP[x][y]["village"]:
            self.__village(draw, img, x, y)
        if self.MAP[x][y]["road"]:
            self.__road(draw, x, y)
        if self.MAP[x][y]["forest"]:
            self.__forest(draw, img, x, y)

    def __calculate_cells(self):
        # some initial calculations for determining cell size and origins
        self.CELL_X = round(self.IMG_SIZE[0]/self.GRID[0])
        self.CELL_Y = round(self.IMG_SIZE[1]/self.GRID[1])
        for x in range(self.GRID[0]):
            temp = []
            for y in range(self.GRID[1]):
                temp.append((x*self.CELL_X, y*self.CELL_Y))
            self.CELL_ORIGINS.append(temp)

    def __grid(self, draw):
        """Draws grid on the map."""
        # get spacing of X and Y axis lines
        x_lines = [self.CELL_ORIGINS[x][0][0] for x in range(self.GRID[0])]
        y_lines = [self.CELL_ORIGINS[0][y][1] for y in range(self.GRID[1])]
        # draw the grid lines
        for x in x_lines:
            draw.line(((x, 0), (x, self.IMG_SIZE[1]-1)),
                      width=1, fill=(0, 0, 0))
        for y in y_lines:
            draw.line(((0, y), (self.IMG_SIZE[0]-1, y)),
                      width=1, fill=(0, 0, 0))

    def __river(self, draw, x, y):
        """Draws river in the cell. Private."""
        # get possible suitable neighbor directions
        possible = self.__filter_neighbors(x, y, ["river"])
        # get start and end points of river
        start = utils.dir_to_point(possible[0], self.CELL_ORIGINS[x][y],
                                   self.CELL_X, self.CELL_Y)
        end = utils.dir_to_point(possible[1], self.CELL_ORIGINS[x][y],
                                 self.CELL_X, self.CELL_Y)
        # draw the river
        draw.line((start, end), fill=self.COLORS["river"], width=self.RIVER_WIDTH)

    def __road(self, draw, x, y):
        """Draws road in the cell. Private."""
        # get possible suitable neighbor directions
        possible = self.__filter_neighbors(x, y, ("village", "road", "castle"))
        # get start and end points of road
        start = utils.dir_to_point(possible[0], self.CELL_ORIGINS[x][y],
                                   self.CELL_X, self.CELL_Y)
        end = utils.dir_to_point(possible[1], self.CELL_ORIGINS[x][y],
                                 self.CELL_X, self.CELL_Y)
        # draw the road
        draw.line((start, end), fill=self.COLORS["road"], width=self.RIVER_WIDTH)

    def __forest(self, draw, img, pos_x, pos_y):
        """Draw forest in the cell. Private."""
        # get suitable density for the cell
        if len(self.__filter_neighbors(pos_x, pos_y, ["forest"])) <= 3:
            density = round(self.FOREST_DENSITY/2)
        if self.MAP[pos_x][pos_y]["river"]:
            density = round(self.FOREST_DENSITY/4)
        if self.MAP[pos_x][pos_y]["castle"]:
            density = round(self.FOREST_DENSITY/2)
        else:
            density = self.FOREST_DENSITY
        # start planting trees
        counter = 0
        limiter = 0
        while counter <= density and limiter <= 100:
            limiter += 1
            # get random coords in the cell
            x = random.randint(0, self.CELL_X-1)
            y = random.randint(0, self.CELL_Y-1)
            dx = x + self.TREE_SIZE
            dy = y + self.TREE_SIZE
            start = (self.CELL_ORIGINS[pos_x][pos_y][0]+x,
                     self.CELL_ORIGINS[pos_x][pos_y][1]+y)
            end = (self.CELL_ORIGINS[pos_x][pos_y][0]+dx,
                   self.CELL_ORIGINS[pos_x][pos_y][1]+dy)
            # check if tree is inside picture and on grass, if no start again
            if end[0] > self.IMG_SIZE[0]-1 or end[1] > self.IMG_SIZE[1]-1:
                continue
            if not img.getpixel(start) == self.COLORS["grass"]:
                continue
            # randomize the color a bit
            color = list(self.COLORS["tree"])
            color_r = random.randint(-self.COLOR_VARIATION, self.COLOR_VARIATION)
            for index in range(len(color)):
                color[index] += color_r
            # draw the tree
            draw.ellipse((start, end), fill=tuple(color))
            counter += 1

    def __village(self, draw, img, pos_x, pos_y):
        """Draws village in cell. Private."""
        # get directions of suitable neighbor cells
        directions = self.__filter_neighbors(pos_x, pos_y, ("village",
                                             "road", "castle"))
        # draw streets and get their end points.
        road_ends = self.__village_roads(draw, pos_x, pos_y, directions)
        # draw houses
        self.__village_houses(draw, img, pos_x, pos_y, road_ends)

    def __village_houses(self, draw, img, pos_x, pos_y, road_ends):
        """Draws village houses in cell. Private."""
        mid_cell = utils.midpoint(self.CELL_ORIGINS[pos_x][pos_y],
                                  (self.CELL_ORIGINS[pos_x][pos_y][0]+self.CELL_X,
                                  self.CELL_ORIGINS[pos_x][pos_y][1]+self.CELL_Y))
        counter = 0
        limiter = 0
        while counter <= self.VILLAGE_DENSITY and limiter <= 100:
            limiter += 1
            # generate random house in cell
            x = random.randint(0, self.CELL_X-1)
            y = random.randint(0, self.CELL_Y-1)
            dx = x + self.HOUSE_SIZE
            dy = y + self.HOUSE_SIZE
            start = (self.CELL_ORIGINS[pos_x][pos_y][0]+x,
                     self.CELL_ORIGINS[pos_x][pos_y][1]+y)
            end = (self.CELL_ORIGINS[pos_x][pos_y][0]+dx,
                   self.CELL_ORIGINS[pos_x][pos_y][1]+dy)
            # check if house in image on grass and not crossing road
            if end[0] > self.IMG_SIZE[0]-1 or end[1] > self.IMG_SIZE[1]-1:
                continue
            if not img.getpixel(start) == self.COLORS["grass"]:
                continue
            if not img.getpixel(end) == self.COLORS["grass"]:
                continue
            if not utils.same_side(start, end, mid_cell, road_ends):
                continue
            # randomize the color a bit
            color = list(self.COLORS["house"])
            color_r = random.randint(-self.COLOR_VARIATION, self.COLOR_VARIATION)
            for index in range(len(color)):
                color[index] += color_r
            # draw the house
            draw.rectangle((start, end), fill=tuple(color))
            counter += 1

    def __village_roads(self, draw, pos_x, pos_y, directions):
        """Draw village streets in cell. Private."""
        # get middle of cell
        mid_cell = utils.midpoint(self.CELL_ORIGINS[pos_x][pos_y],
                                  (self.CELL_ORIGINS[pos_x][pos_y][0]+self.CELL_X,
                                  self.CELL_ORIGINS[pos_x][pos_y][1]+self.CELL_Y))
        road_ends = []
        # for every direction, draw a road and save its endpoint
        for direction in directions:
            if 0 in direction:
                end = utils.dir_to_point(direction, self.CELL_ORIGINS[pos_x][pos_y],
                                         self.CELL_X, self.CELL_Y)
                road_ends.append(end)
                draw.line((mid_cell, end), fill=self.COLORS["road"],
                          width=self.ROAD_WIDTH)
        return road_ends

    def __castle(self, draw, pos_x, pos_y):
        """Draw castle in cell. Private."""
        # for some reason doesnt draw castles on edges. No idea why.
        neighbors = self.__filter_neighbors(pos_x, pos_y, ["castle"])
        mid_cell = utils.midpoint(self.CELL_ORIGINS[pos_x][pos_y],
                                  (self.CELL_ORIGINS[pos_x][pos_y][0]+self.CELL_X,
                                   self.CELL_ORIGINS[pos_x][pos_y][1]+self.CELL_Y))
        if len(neighbors) == 8:  # inside castle
            start = self.CELL_ORIGINS[pos_x][pos_y]
            end = (self.CELL_ORIGINS[pos_x][pos_y][0]+self.CELL_X,
                   self.CELL_ORIGINS[pos_x][pos_y][1]+self.CELL_Y)
            draw.rectangle((start, end), fill=self.COLORS["castle0"])
            return
        elif len(neighbors) == 3 or len(neighbors) == 5:  # corners and walls
            for direction in neighbors:  # inside
                end = utils.dir_to_point(direction, self.CELL_ORIGINS[pos_x][pos_y],
                                         self.CELL_X, self.CELL_Y)
                if 0 not in direction:
                    draw.rectangle((mid_cell, end), fill=self.COLORS["castle0"])
            for direction in neighbors:  # walls
                end = utils.dir_to_point(direction, self.CELL_ORIGINS[pos_x][pos_y],
                                         self.CELL_X, self.CELL_Y)
                if 0 in direction:
                    if (-direction[0], -direction[1]) in neighbors or len(neighbors)==3:
                        draw.line((mid_cell, end), fill=self.COLORS["castle1"],
                                  width=self.CASTLE_WALL_THICKNESS)
            self.__castle_tower(draw, mid_cell)
        else:  # dont draw other variants - should not appear
            return

    def __castle_tower(self, draw, point):
        """Draw castle tower on point. Private."""
        start = (point[0]-round(self.CASTLE_TOWER_SIZE/2),
                 point[1]-round(self.CASTLE_TOWER_SIZE/2))
        end = (point[0]+round(self.CASTLE_TOWER_SIZE/2),
               point[1]+round(self.CASTLE_TOWER_SIZE/2))
        draw.ellipse((start, end), fill=self.COLORS["castle1"])

    def __filter_neighbors(self, x, y, filters):
        """
        Go through neighbors and filter them according to filter.

        Returns list of vectors aiming at filtered neighbors.

        Private method.
        """
        possible = []
        # special checks for cells in corners
        if x == 0 and y == 0:
            possible.append((-1, -1))
            directions = ((0, 1), (1, 1), (1, 0))
        elif x == 0 and y == self.GRID[1]-1:
            possible.append((-1, 1))
            directions = ((0, -1), (1, -1), (1, 0))
        elif x == self.GRID[0]-1 and y == 0:
            possible.append((1, -1))
            directions = ((-1, 0), (-1, 1), (0, 1))
        elif x == self.GRID[0]-1 and y == self.GRID[1]-1:
            possible.append((1, 1))
            directions = ((-1, 0), (-1, -1), (0, -1))
        # special checks for cells on edges
        elif x == 0:
            possible.append((-1, 0))
            directions = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
        elif y == 0:
            possible.append((0, -1))
            directions = ((-1, 1), (0, 1), (1, 1), (1, 0), (-1, 0))
        elif x == self.GRID[0]-1:
            possible.append((1, 0))
            directions = ((-1, 1), (0, 1), (0, -1), (-1, -1), (-1, 0))
        elif y == self.GRID[1]-1:
            possible.append((0, 1))
            directions = ((1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0))
        else:
            directions = ((-1, 1), (0, 1), (1, 1), (1, 0),
                          (1, -1), (0, -1), (-1, -1), (-1, 0))
        # filter the neighbors
        for item in filters:
            for direction in directions:
                if self.MAP[x+direction[0]][y+direction[1]][item]:
                    possible.append(direction)
        return possible
