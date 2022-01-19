from math import *
import numpy as np

INVALID_POINT_CONST = -1.0

def points_dist(a, b):
    dist = a.dist / 2 + b.dist / 2
    if dist == 0:
        return INVALID_POINT_CONST

    return sqrt(abs(a.x - b.x) ** 2 + abs(a.y - b.y) ** 2) / dist

def z_diff_fading(a, b):
    return sqrt(abs(a.z - b.z))

def equal_points(a, b):
    if a == b:
        return INVALID_POINT_CONST
    else:
        return 0

def dist_diff(a, b) -> float:
    if a.dist == b.dist and a.dist == 0:
        return INVALID_POINT_CONST

    return max(a.dist, b.dist) - min(a.dist, b.dist)

#unused
def z_diff_exp(a, b) -> float:
    return (a.z - b.z) ** 4

"""
def z_diff_exp(a, b) -> float:
    assert False

def z_diff_exp(a, b) -> float:
    assert False

def z_diff_exp(a, b) -> float:
    assert False
"""

class EntropyFucktor:
    def __init__(self, calc_functor, k = 1):
        self.calc_functor = calc_functor
        self.k = k

def getEntropyFactors():
    return [ EntropyFucktor(points_dist),
             EntropyFucktor(z_diff_fading, 100),
             EntropyFucktor(equal_points),
             EntropyFucktor(dist_diff),
             ]
