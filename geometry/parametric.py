"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from . import AbstractGeometry
from .primitives import*
from .colorFuncs import randomColor, rainbowGradient
import math 
from ..utils.matrix import Matrix
import numpy as np

class AbstractParametric(AbstractGeometry):
    """Abstract parametric class for parametric geometry.
       Expects a surface function which defines the surface
       of the shape. *Start, *End, and *Resolution define
       how much of the shape is created and at what level
       of detail."""
       
    def __init__(self, uStart, uEnd, uResolution,
                       vStart, vEnd, vResolution,
                       surfaceFunction,
                       colorFunction=None):
        super().__init__()
        
        # Generate set of points based on the function
        deltaU = (uEnd - uStart) / uResolution
        deltaV = (vEnd - vStart) / vResolution
        positions = []
        for uIndex in range(uResolution+1):
            vArray = []
            for vIndex in range(vResolution+1):
                u = uStart + uIndex * deltaU
                v = vStart + vIndex * deltaV
                vArray.append(surfaceFunction(u,v))
            positions.append(vArray)
            
        # Store vertex data
        positionData = []
        colorData = []
        
        # Default vertex colors
        C1, C2, C3 = [1,0,0], [0,1,0], [0,0,1]
        C4, C5, C6 = [0,1,1], [1,0,1], [1,1,0]
        cIndex = 0
        
        # Group vertex data into triangles
        for xIndex in range(uResolution):
            for yIndex in range(vResolution):        
                # Position data
                pA = positions[xIndex+0][yIndex+0]
                pB = positions[xIndex+1][yIndex+0]
                pC = positions[xIndex+1][yIndex+1]
                pD = positions[xIndex+0][yIndex+1]
                
                positionData += [ pA.copy(), pB.copy(),
                                  pC.copy(), pA.copy(),
                                  pC.copy(), pD.copy() ]
                # Color data
                if colorFunction == None:
                    colorData += [C1,C2,C3, C4,C5,C6]
                else:
                    cA = colorFunction(xIndex,  yIndex,   len(positions), len(positions[xIndex]))
                    cB = colorFunction(xIndex+1,yIndex,   len(positions), len(positions[xIndex]))
                    cC = colorFunction(xIndex+1,yIndex+1, len(positions), len(positions[xIndex]))
                    cD = colorFunction(xIndex,  yIndex+1, len(positions), len(positions[xIndex]))
                    
                    colorData += [cA, cB, cC,
                                  cA, cC, cD]           
                
        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
        self.countVertices()

## Some parametric shapes ##


class PlaneGeometry(AbstractParametric):
    def __init__(self, width=1, height=1,
                 widthSegments=8, heightSegments=8):
        
        def S(u,v):
            return [u, v, 0]
        
        super().__init__(-width/2, width/2,
                         widthSegments,
                         -height/2, height/2,
                         heightSegments, S,
                         randomColor)

class EllipsoidGeometry(AbstractParametric):
    def __init__(self, width=1, height=1, depth=1,
             radiusSegments=32, heightSegments=16):
        def S(u,v):
            return [ width/2 * np.sin(u) * np.cos(v),
                    height/2 * np.sin(v),
                    depth/2 * np.cos(u) * np.cos(v) ]
        super().__init__(0, 2*np.pi,
                         radiusSegments,
                         -np.pi/2, np.pi/2,
                         heightSegments, S)

class SphereGeometry(EllipsoidGeometry):
    def __init__(self, radius=1,
             radiusSegments=32,
             heightSegments=16):
        super().__init__(2*radius,
                        2*radius,
                        2*radius,
                        radiusSegments,
                        heightSegments)

class RainbowBowlGeometry(AbstractParametric):
    def __init__(self, radius=1, uResolution=32, vResolution=16):
        
        def S(u, v):
            #here, i used std spherical coords 
            return [ radius * np.cos(u) * np.cos(v),
                     radius * np.sin(v),
                     radius * np.sin(u) * np.cos(v) ]
        
        super().__init__(0, 2*np.pi, uResolution,
                         -np.pi/2, 0, vResolution,
                         S,
                         rainbowGradient)
    
class CylindricalGeometry(AbstractParametric):
    def __init__(self, radiusTop=1, radiusBottom=1,
                 height=1, radialSegments=32,
                 heightSegments=4, closedTop=True,
                 closedBottom=True):
        def S(u,v):
            return [ (v*radiusTop + (1-v)*radiusBottom) * np.sin(u),
                    height * (v - 0.5),
                    (v*radiusTop + (1-v)*radiusBottom) * np.cos(u) ]
        super().__init__(0, 2*np.pi,
                         radialSegments,
                         0, 1,
                         heightSegments,
                         S)
        
        if closedTop:
            topGeometry = PolygonGeometry(radialSegments,
                                          radiusTop)
            transform = Matrix.makeTranslation(0, height/2, 0) @ Matrix.makeRotationY(-math.pi/2) @ Matrix.makeRotationX(-math.pi/2)
            topGeometry.applyMatrix(transform)
            self.merge(topGeometry)
            
        if closedBottom:
            bottomGeometry = PolygonGeometry(radialSegments,
                                             radiusBottom)
            transform = Matrix.makeTranslation(0, -height/2, 0) @ Matrix.makeRotationY(-math.pi/2) @ Matrix.makeRotationX(math.pi/2)
            bottomGeometry.applyMatrix(transform)
            self.merge(bottomGeometry)
    
class CylinderGeometry(CylindricalGeometry):
    def __init__(self, radius=1, height=1,
                 radialSegments=32,
                 heightSegments=4,
                 closed=True):
        super().__init__(radius, radius,
                         height, radialSegments,
                         heightSegments, closed, closed)
        
class PrismGeometry(CylindricalGeometry):
    def __init__(self, radius=1, height=1,
                 sides=6, heightSegments=4,
                 closed=True):
        super().__init__(radius, radius,
                         height, sides,
                         heightSegments, closed, closed)

class ConeGeometry(CylindricalGeometry):
    def __init__(self, radius=1, height=1,
                 radialSegments=32, heightSegments=4,
                 closed=True):
        super().__init__(0, radius, height,
                         radialSegments, heightSegments,
                         False, closed)

class PyramidGeometry(CylindricalGeometry):
    def __init__(self, radius=1, height=1,
                 sides=4, heightSegments=4,
                 closed=True):
        super().__init__(0, radius, height,
                         sides, heightSegments,
                         False, closed)
    