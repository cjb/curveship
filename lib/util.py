delta_x = (0, 0, 1, 0, -1)
delta_y = (0, -1, 0, 1, 0)
facings = {
    'stand': 0,
    'north': 1,
    'east': 2,
    'south': 3,
    'west': 4,
}

def dist(start, finish):
    sx, sy = start
    fx, fy = finish
    return abs(sx-fx)+abs(sy-fy)

def dir_of(start, finish):
    """
    Return a pair of directions suitable for going from start to finish.
    The first direction in the tuple is the one of larger distance. Both
    of the directions returned can be the same, if the target is lined up.
    """
    sx, sy = start
    fx, fy = finish
    hd, vd = 0, 0
    if sx > fx:
        hd = 4
    elif sx < fx:
        hd = 2
    if sy > fy:
        vd = 1
    elif sy < fy:
        vd = 3
    if hd == 0:
        hd = vd
    elif vd == 0:
        vd = hd
    if abs(sx-fx) > abs(sy-fy):
        return (hd, vd)
    else:
        return (vd, hd)

