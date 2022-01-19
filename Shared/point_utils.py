import numpy as np
import copy

class PointInfo:
    def __init__(self, x, y, z, dist):
        self.x = x
        self.y = y
        self.z = z
        self.dist = dist
        self.entropy = 0

def ExtractDist(point_map):
    dist = np.zeros((len(point_map), len(point_map[0])))

    for x in range(len(point_map)):
        for y in range(len(point_map[x])):
            dist[x][y] = point_map[x][y].dist

    return dist

def ExtractEntropy(point_map):
    entropy = np.zeros((len(point_map), len(point_map[0])))

    for x in range(len(point_map)):
        for y in range(len(point_map[x])):
            entropy[x][y] = point_map[x][y].entropy

    return entropy

def EntropyRemoveOutOfBounds(point_map, min, max, invert=True):
    #filtered = np.copy(point_map)
    filtered = np.full(shape=point_map.shape, fill_value=PointInfo(0,0,0,0), dtype='O')
    for x in range(len(point_map)):
        for y in range(len(point_map[x])):
            is_in_bounds = True
            entropy = point_map[x][y].entropy
            if invert:
                is_in_bounds = entropy < min or entropy > max
            else:
                is_in_bounds = entropy >= min and entropy <= max

            if is_in_bounds:
                filtered[x][y] = copy.deepcopy(point_map[x][y])

    return filtered



"""
Iterate through every pair of 4 pano pixels
and calculate entropy for each point

1---3
| /
*---2

entropy is a value that characterize form of each quad
entropy evaluator provided by client
"""
def CalcEntropy(point_map, entropy):
    def pano_pixel_to_point(point_map, x, y):
        if x >= len(point_map) or y >= len(point_map[x]):
            return None

        return point_map[x][y]

    def get_neighbours(point_map, x, y):
       return [pano_pixel_to_point(point_map, x + 1, y),     #1
               pano_pixel_to_point(point_map, x, y + 1),     #2
               pano_pixel_to_point(point_map, x + 1, y + 1)] #3

    result = np.copy(point_map)
    for x in range(len(point_map)):
        for y in range(len(point_map[x])):
            for neighbour in get_neighbours(point_map, x, y):
                if neighbour is not None:
                    result[x][y].entropy = result[x][y].entropy + entropy.calc_functor(point_map[x][y], neighbour)

    return result

def DropEntropy(point_map):
    for x in range(len(point_map)):
        for y in range(len(point_map[x])):
            point_map[x][y].entropy = 0

    return point_map

def CreateEntropyBackGround(point_map):
    result = np.copy(point_map)
    for x in range(len(point_map)):
        for y in range(len(point_map[x])):
            if point_map[x][y].entropy < 0:
                result[x][y].entropy = -10

    return result