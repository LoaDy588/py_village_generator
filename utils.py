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
    """Return all points of rectangle contained by origin and end."""
    size_x = abs(origin[0]-end[0])+1
    size_y = abs(origin[1]-end[1])+1
    rectangle = []
    for x in range(size_x):
        for y in range(size_y):
            rectangle.append((origin[0]+x, origin[1]+y))
    return rectangle


def same_side(pointA, pointB, origin, ends):
    """
    Returns true if both points are on same side of all vectors.

    ARGUMENTS:
    """
    sigA = []
    sigB = []
    for end in ends:
        tempA = (((end[0]-origin[0])*(pointA[1]-origin[1]))
                 - ((end[1]-origin[1])*(pointA[0]-origin[0])))
        tempB = (((end[0]-origin[0])*(pointB[1]-origin[1]))
                 - ((end[1]-origin[1])*(pointB[0]-origin[0])))
        sigA.append(signum(tempA))
        sigB.append(signum(tempB))
    if sigA == sigB:
        return True
    else:
        False


def signum(number):
    """Self-explanatory."""
    if(number < 0): return -1
    elif(number > 0): return 1
    else: return 0


def midpoint(a, b):
    """Calculate midpoint between two points."""
    middle = []
    for i in range(len(a)):
        middle.append(round((a[i]+b[i])/2))
    return tuple(middle)


def dir_to_point(direction, cell_origin, size_x, size_y):
    """
    Translate direction of neighbor to
    point of shared corner or middle of shared side.
    """
    # needs some heavy rewriting, is ugly.
    if direction == (-1, 1):
        return (cell_origin[0], cell_origin[1]+size_y-1)
    elif direction == (1, 1):
        return (cell_origin[0]+size_x-1, cell_origin[1]+size_y-1)
    elif direction == (1, -1):
        return (cell_origin[0]+size_x-1, cell_origin[1])
    elif direction == (-1, -1):
        return (cell_origin[0], cell_origin[1])
    elif direction == (0, 1):
        return midpoint((cell_origin[0], cell_origin[1]+size_y-1),
                        (cell_origin[0]+size_x-1, cell_origin[1]+size_y-1))
    elif direction == (1, 0):
        return midpoint((cell_origin[0]+size_x-1, cell_origin[1]),
                        (cell_origin[0]+size_x-1, cell_origin[1]+size_y-1))
    elif direction == (0, -1):
        return midpoint((cell_origin[0], cell_origin[1]),
                        (cell_origin[0]+size_x-1, cell_origin[1]))
    elif direction == (-1, 0):
        return midpoint((cell_origin[0], cell_origin[1]),
                        (cell_origin[0], cell_origin[1]+size_y-1))
