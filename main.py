import numpy as np
from scipy.spatial import Delaunay
from kitti_foundation import Kitti, Kitti_util
import kitti_foundation
import matplotlib.pyplot as plt
import polylidar
from polylidar import MatrixDouble, Polylidar3D
import time
import math
from polylidar.polylidarutil import (generate_test_points, plot_triangles, get_estimated_lmax,
                                     plot_triangle_meshes, get_triangles_from_list, get_colored_planar_segments, plot_polygons)

from polylidar.polylidarutil import (plot_polygons_3d, generate_3d_plane, set_axes_equal, plot_planes_3d,
                                     scale_points, rotation_matrix, apply_rotation)
velo_path = 'data/2011_09_26/velodyne_points/data'

velo = Kitti_util(frame=89, velo_path=velo_path)

frame = np.vstack(list(velo.velo_file))

print(frame.shape)
#x_range, y_range, z_range, scale = (-20, 20), (-20, 20), (-2, 2), 10
#topview_img = velo.velo_2_topview_frame(x_range=x_range, y_range=y_range, z_range=z_range)

points = frame
points_mat = MatrixDouble(np.array(points, dtype=np.float64), copy=True)
t1 = time.time()
#polylidar_kwargs = dict(lmax=1.8, min_triangles=20)
polylidar3d = Polylidar3D()#**polylidar_kwargs)
mesh, planes, polygons = polylidar3d.extract_planes_and_polygons(points_mat)
t2 = time.time()
print("Took {:.2f} milliseconds".format((t2 - t1) * 1000))
print("Should see two planes extracted, please rotate.")

triangles = np.asarray(mesh.triangles)
fig, ax = plt.subplots(figsize=(10, 10), nrows=1, ncols=1,
                       subplot_kw=dict(projection='3d'))
# plot all triangles
#for plane in planes:
plot_planes_3d(points, triangles, planes, ax, color=(0, 0, 1))
print(".")
#plot_polygons_3d(points, polygons, ax, color=(0.3, 0.3, 0.3))
print(".")
# plot points
#ax.scatter(*scale_points(points), c='k', s=0.1)
set_axes_equal(ax)
ax.view_init(elev=15., azim=-35)
plt.show()
print(input())

print("done")