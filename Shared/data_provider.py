import numpy as np
from kitti_foundation import Kitti, Kitti_util

def get_data():
    velo_path = '../../data/2011_09_26/velodyne_points/data'

    velo = Kitti_util(frame=89, velo_path=velo_path)

    return np.vstack(list(velo.velo_file))


def normalize_depth(val, min_v, max_v):
    """
    print 'nomalized depth value'
    nomalize values to 0-255 & close distance value has high value. (similar to stereo vision's disparity map)
    """
    return (((max_v - val) / (max_v - min_v)) * 255).astype(np.uint8)


def normalize_val(val, min_v, max_v):
    """
    print 'nomalized depth value'
    nomalize values to 0-255 & close distance value has low value.
    """
    return (((val - min_v) / (max_v - min_v)) * 255).astype(np.uint8)


def in_h_range_points(m, n, fov):
    """ extract horizontal in-range points """
    return np.logical_and(np.arctan2(n, m) > (-fov[1] * np.pi / 180), \
                          np.arctan2(n, m) < (-fov[0] * np.pi / 180))


def in_v_range_points(m, n, fov):
    """ extract vertical in-range points """
    return np.logical_and(np.arctan2(n, m) < (fov[1] * np.pi / 180), \
                          np.arctan2(n, m) > (fov[0] * np.pi / 180))


def fov_setting(points, x, y, z, dist, h_fov, v_fov, auto_compute=True):
    """ filter points based on h,v FOV  """

    if auto_compute:
        return points

    if h_fov[1] == 180 and h_fov[0] == -180 and v_fov[1] == 2.0 and v_fov[0] == -24.9:
        return points

    if h_fov[1] == 180 and h_fov[0] == -180:
        return points[in_v_range_points(dist, z, v_fov)]
    elif v_fov[1] == 2.0 and v_fov[0] == -24.9:
        return points[in_h_range_points(x, y, h_fov)]
    else:
        h_points = in_h_range_points(x, y, h_fov)
        v_points = in_v_range_points(dist, z, v_fov)
        return points[np.logical_and(h_points, v_points)]


def velo_points_2_pano(points, v_res=0.42, h_res=0.35, v_fov=(-35, 15), h_fov=(-180, 180), depth=False):
    # Projecting to 2D
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    dist = np.sqrt(x ** 2 + y ** 2 + z ** 2)

    # project point cloud to 2D point map
    x_img = np.arctan2(-y, x) / (h_res * (np.pi / 180))
    y_img = -(np.arctan2(z, dist) / (v_res * (np.pi / 180)))

    """ filter points based on h,v FOV  """
    x_img = fov_setting(x_img, x, y, z, dist, h_fov, v_fov)
    y_img = fov_setting(y_img, x, y, z, dist, h_fov, v_fov)
    dist = fov_setting(dist, x, y, z, dist, h_fov, v_fov)

    x_size = int(np.ceil((h_fov[1] - h_fov[0]) / h_res))
    y_size = int(np.ceil((v_fov[1] - v_fov[0]) / v_res))

    # shift negative points to positive points (shift minimum value to 0)
    x_offset = h_fov[0] / h_res
    x_img = np.trunc(x_img - x_offset).astype(np.int32)
    y_offset = v_fov[1] / v_res
    y_fine_tune = 1
    y_img = np.trunc(y_img + y_offset + y_fine_tune).astype(np.int32)

    if depth == True:
        # nomalize distance value & convert to depth map
        dist = normalize_depth(dist, min_v=0, max_v=120)
    else:
        dist = normalize_val(dist, min_v=0, max_v=120)

    # array to img
    img = np.zeros([y_size + 1, x_size + 1], dtype=np.uint8)
    img[y_img, x_img] = dist

    return img

def get_composite(entropy_calc_functor=None):
    class Composite(object):
        pass

    composite = Composite()
    composite.points = get_data()
    composite.pano = velo_points_2_pano(composite.points)

    length = composite.pano.shape[0] * composite.pano.shape[1]
    # we expect 1 to 1 relationship between panorama depth view and actual 3d coords
    #assert length == composite.points.shape[0]

    composite.entropy = None # will be setted
    return composite

"""
Iterate through every pair of 4 pano pixels
and calculate entropy for each point

1---3
| /
*---2

entropy is a value that characterize form of each quad
entropy evaluator provided by client
"""

class entropy_calculator:
    def __init__(self, composite):
        self.composite = composite

    def pano_pixel_to_point(self, idx_x, idx_y):
        if idx_x > self.composite.pano.shape[0] or idx_y > self.composite.pano.shape[1]:
            return None

        return self.composite.points[idx_x * self.composite.pano.shape[0] + idx_y]

    def get_neighbours(self, idx_x, idx_y):
       return [self.pano_pixel_to_point(idx_x + 1, idx_y),     #1
               self.pano_pixel_to_point(idx_x, idx_y + 1),     #2
               self.pano_pixel_to_point(idx_x + 1, idx_y + 1)] #3

    def calc_entropy(self, calc_functor):
        entropy = np.zeros(self.composite.pano.shape)
        row = self.composite.pano.shape[0]
        col = self.composite.pano.shape[1]
        for row_idx in range(row):
            for col_idx in range(col):
                for neighbour in self.get_neighbours(row_idx, col_idx):
                    if neighbour is not None:
                        curr = self.pano_pixel_to_point(row_idx, col_idx)
                        entropy[row_idx][col_idx] = entropy[row_idx][col_idx] + calc_functor(curr, neighbour)

        return entropy


#def tie_data(point_cloud, pano_view):
#    data = []
#    data.points = np.ndarray
#    data.grid2d = np.ndarray
#    data.entropy = np.ndarray

#    for row in pano_view:
#        for pixel in row:
#            if pixel is not 0:
#                data.grid2d

    # todo impl