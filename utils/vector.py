"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

import numpy as np
from math import sqrt
from .definitions import EPSILON

def magnitude(vector):    
    """Give the magnitude of a vector."""
    return np.linalg.norm(vector)

def normalize(vector):
    """Normalize a numpy array."""
    mag = magnitude(vector)
    if mag == 0.0:
        return vec(1,0,0)
    return vector / mag

def lerp(a, b, percent):
    """Linearly interpolate between a and b given a percent."""
    return (1.0 - percent)*a + percent*b

def smerp(a, b, percent):
    """Smooth interpolation."""
    percent = min(1.0, max(0.0, percent))
    x = (2*percent) - 1
    y = (3/4)*x-(1/4)*(x**3)+(1/2)
    smoothPercent = 3*percent**2 - 2*percent**3
    return a + y*(b-a)

def vec(x, y=None, z=None):
    """Make a numpy vector of x, y, z."""
    if not(y is None) and not(z is None):
        return np.array((x,y,z), dtype=np.float32)
    else:
        return np.array(x, dtype=np.float32)

def posDot(v,w):
    dot = np.dot(v,w)
    return max(0.0, dot)


if __name__ == '__main__':
    print(getConeAbout(vec(0,1,0), np.pi / 4, 2))
