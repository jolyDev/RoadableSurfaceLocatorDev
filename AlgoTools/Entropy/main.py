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

composite = data_manager.get_composite()
entropy_estimator = data_manager.entropy_calculator(composite)
composite.entropy = entropy_estimator.calc_entropy(lambda first, second: abs(first[0]**2) + abs(first[1] ** 2) + abs(first[2] ** 2))

plt.subplots(1,1, figsize = (13,3) )
plt.imshow(composite.pano)
plt.axis('off')
plt.show()

point_map = data_manager.velo_points_2_pano_info(data_manager.get_data())
#entropy_estimator = data_manager.entropy_calculatorX(point_map)
"""
entropy_estimator.calc_entropy(lambda first, second: abs(first.x - second.x)
                                                     + abs(first.y - second.y)
                                                     + abs(first.z - second.z))
                                                     """
#entropy_estimator.calc_entropy(lambda first, second: abs(first.dist))
drawDist(point_map)
print("done")