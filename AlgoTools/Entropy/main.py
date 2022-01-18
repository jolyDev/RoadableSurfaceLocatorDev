import Shared.data_provider as data_manager
import numpy as np
import matplotlib.pyplot as plt

def drawEntropy(point_map):
    entropy_map = np.zeros((len(point_map), len(point_map[0])))

    for x in range(len(point_map)):
        for y in range(len(point_map[x])):
            entropy_map[x][y] = point_map[x][y].entropy

    plt.subplots(1, 1)
    plt.imshow(entropy_map)
    plt.axis('off')
    plt.show()

def drawDist(point_map):
    entropy_map = np.zeros((len(point_map), len(point_map[0])))

    for x in range(len(point_map)):
        for y in range(len(point_map[x])):
            entropy_map[x][y] = point_map[x][y].dist

    plt.subplots(1, 1)
    plt.imshow(entropy_map)
    plt.axis('off')
    plt.show()

def drawClassic():
    plt.subplots(1, 1)
    plt.imshow(data_manager.velo_points_2_pano(data_manager.get_data()))
    plt.axis('off')
    plt.show()

def drawHistogram(point_map):
    entropy_map = np.zeros((len(point_map), len(point_map[0])))
    for x in range(len(point_map)):
        for y in range(len(point_map[x])):
            if point_map[x][y].entropy < 20000: # chop extra values
                entropy_map[x][y] = point_map[x][y].entropy

    plt.hist(entropy_map.flatten(), bins=150)
    plt.show()

def chopPointMap(point_map, min, max, inverted=False):
    #chopped = np.array(point_map, copy=True)
    chopped = np.full(shape=(point_map.shape[0], point_map.shape[1]), fill_value=data_manager.PointInfo(0, 0, 0, 0), dtype='O')
    for x in range(len(chopped)):
        for y in range(len(chopped[x])):
            entropy = point_map[x][y].entropy
            if inverted:
                if entropy < min or entropy > max: # chop extra values
                    chopped[x][y] = point_map[x][y]
                    chopped[x][y].entropy = chopped[x][y].entropy - 1000
            else:
                if entropy >= min and entropy <= max: # chop extra values
                    chopped[x][y] = point_map[x][y]
                    chopped[x][y].entropy = chopped[x][y].entropy - 1000

    return chopped

point_map = data_manager.velo_points_2_pano_info(data_manager.get_data())
entropy_estimator = data_manager.entropy_calculatorX(point_map)

functor = lambda first, second: abs(first.x - second.x) ** 2 \
                                + abs(first.y - second.y) ** 2\
                                + abs(first.z - second.z) ** 2
#entropy_estimator.calc_entropy(functor)
#drawClassic()
entropy_estimator.calc_entropy(lambda first, second: abs(first.dist))
#drawEntropy(point_map)
drawHistogram(point_map)
drawEntropy(chopPointMap(point_map, 35, 75))
#drawEntropy(chopPointMap(point_map, 0, 0))
print("done")