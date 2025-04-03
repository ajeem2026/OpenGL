"""
Author: Abid Jeem and Liz Matthews
"""

from ..utils.vector import vec, lerp
import numpy as np
import random
import math


def randomColor(u, v, uMaxIndex, vMaxIndex):
    return vec(random.random(), random.random(), random.random())


def rainbowGradient(uIndex, vIndex, uMaxIndex, vMaxIndex, orientation="u", wrap=False):
    # The six colors to fade between are (1,0,0), (1,1,0), (0,1,0), (0,1,1), (0,0,1), and (1,0,1)
    colors = [
        (1, 0, 0),
        (1, 1, 0),
        (0, 1, 0),
        (0, 1, 1),
        (0, 0, 1),
        (1, 0, 1)
    ]
    # If wrap is true, then append the first color from the list to the end of the list.
    if wrap:
        colors.append(colors[0])

    # The parameter orientation indicates whether the u or v index will be used to control the fading

    """The algorithm to pick the start and end colors for fading is:
    """
    # Calculate the percentage as the index divided by the maximum index
    # u* or v* depending on the orientation
    if orientation == "u" and uMaxIndex != 0:
        percent = uIndex/uMaxIndex
    elif orientation == "v" and vMaxIndex != 0:
        percent = vIndex/vMaxIndex
    else:
        return 0

    # Scale the percentage based on the length of the colors minus one
    scale = percent*(len(colors)-1)

    # Starting index is the floor of the scaled percentage
    startIndex = math.floor(scale)

   # Ending index is starting index plus one
    endIndex = startIndex+1

   # lerp() percentage is the floating point remainder of the percentage minus the starting index
    lerp_percent = scale-startIndex

    startColor = vec(*colors[startIndex])
    endColor = vec(*colors[endIndex])

    return lerp(startColor, endColor, lerp_percent)
