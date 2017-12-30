from map_gen import Map_gen
from image_gen import Image_gen

# generators init
mg = Map_gen()
ig = Image_gen()

# map generator settings
mg.GRID_X = 20  # size of grid to generate map on
mg.GRID_Y = 20
mg.VILLAGE_SIZE = 35
mg.FOREST_COUNT = 1
mg.FOREST_SIZE = 200
mg.RIVER = True
mg.CASTLE = True
mg.CASTLE_SIZE = 3

# image generator settings
ig.IMG_SIZE = (400, 400)
ig.COLORS = {
               "grass": (65, 152, 10),
               "tree": (3, 114, 0),
               "road": (238, 182, 70),
               "river": (37, 108, 155),
               "house": (91, 70, 17),
               "castle0": (117, 117, 117),
               "castle1": (175, 175, 175)
              }
ig.COLOR_VARIATION = 10
ig.CASTLE_TOWER_SIZE = 10
ig.CASTLE_WALL_THICKNESS = 3
ig.RIVER_WIDTH = 5
ig.ROAD_WIDTH = 2
ig.TREE_SIZE = 6
ig.HOUSE_SIZE = 5
ig.FOREST_DENSITY = 4
ig.VILLAGE_DENSITY = 2
ig.GRID_LINES = False

# image creation
data = mg.create_map()
ig.draw_map(data, "map.bmp")
