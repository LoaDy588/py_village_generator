def get_neighbors(coords, fieldsize):
    """
    Find neighbors of coords in a field.

    ARGUMENTS:
    coords - in format [x, y]
    fieldsize - size of the field, tuple (x_size, y_size)

    RETURNS:
    list of neighbors, where each neighbor has format [x, y]
    """
    neighbors = []
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    # for every direction, get neighbor coords, append to list
    for coord in coords:
        for vector in directions:
            neighbor = []
            x = coord[0] + vector[0]
            y = coord[1] + vector[1]
            neighbor.append(x)
            neighbor.append(y)
            if neighbor[0] > fieldsize[0]-1 or neighbor[1] > fieldsize[1]-1:
                continue
            if neighbor[0] < 0 or neighbor[1] < 0:
                continue
            if tuple(neighbor) in coords:
                continue
            if neighbor not in neighbors:
                neighbors.append(tuple(neighbor))
    return neighbors


def get_rectangle(origin, end):
    size_x = abs(origin[0]-end[0])+1
    size_y = abs(origin[1]-end[1])+1
    rectangle = []
    for x in range(size_x):
        for y in range(size_y):
            rectangle.append((origin[0]+x, origin[1]+y))
    return rectangle


def find_outer(points):
    return "foo"

def find_nearest_points(tuple1, tuple2):
    return "foo"


def get_path(origin, end, direction, prefered):
    return "foo"
