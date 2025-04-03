"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from . import Mesh
from ..geometry import AbstractGeometry
from ..materials import LineMaterial

class AxesHelper(Mesh):
    """Creates an XYZ axis at the origin."""
    
    def __init__(self, axisLength=1, lineWidth=1,
                 axisColors=[[1,0,0],[0,1,0],[0,0,1]] ):
        geo = AbstractGeometry()
        
        positionData = [[0,0,0], [axisLength,0,0],
                        [0,0,0], [0,axisLength,0],
                        [0,0,0], [0,0,axisLength]]
        colorData = [axisColors[0], axisColors[0],
                     axisColors[1], axisColors[1],
                     axisColors[2], axisColors[2]]
        
        geo.addAttribute("vec3", "vertexPosition", positionData)
        geo.addAttribute("vec3", "vertexColor", colorData)
        
        geo.countVertices()
        
        mat = LineMaterial({
                    "useVertexColors": True,
                    "lineWidth": lineWidth,
                    "lineType": "segments"
        })
        
        # initialize the mesh
        super().__init__(geo, mat)
    
    
class GridHelper(Mesh):
    """Creates a planar grid."""
    
    def __init__(self, size=10, divisions=10,
                gridColor=[0,0,0],
                centerColor=[0.5,0.5,0.5],
                lineWidth=1):
        
        geo = AbstractGeometry()
        mat = LineMaterial({
                "useVertexColors": 1,
                "lineWidth": lineWidth,
                "lineType": "segments"
        })
        positionData = []
        colorData = []
        
        # Create range of values
        values = []
        deltaSize = size/divisions
        for n in range(divisions+1):
            values.append(-size/2 + n * deltaSize)
            
        # Add vertical lines
        for x in values:
            positionData.append([x, -size/2, 0])
            positionData.append([x, size/2, 0])
            if x == 0:
                colorData.append(centerColor)
                colorData.append(centerColor)
            else:
                colorData.append(gridColor)
                colorData.append(gridColor)
                
        # Add horizontal lines
        for y in values:
            positionData.append([-size/2, y, 0])
            positionData.append([ size/2, y, 0])
            if y == 0:
                colorData.append(centerColor)
                colorData.append(centerColor)
            else:
                colorData.append(gridColor)
                colorData.append(gridColor)
                
        geo.addAttribute("vec3", "vertexPosition", positionData)
        geo.addAttribute("vec3", "vertexColor", colorData)
        
        geo.countVertices()
        
        # Initialize the mesh
        super().__init__(geo, mat)