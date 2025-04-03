"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from ..oGL.attribute import Attribute

import numpy as np

class AbstractGeometry(object):
    """Abstract geometry which sets up attributes,
       applies matrices, merge with other geometry,
       and count vertices."""
       
    def __init__(self):
        self.attributes = {}        
        self.vertexCount = None
    
    def addAttribute(self, dataType, variableName, data):            
        self.attributes[variableName] = Attribute(dataType, data)
       
    def countVertices(self):
        """Separate counting method so that merge()
           can work.
        
           The number of vertices may be calculated from
           the length of any Attribute object's array
           of data."""
           
        attrib = list(self.attributes.values())[0]
        self.vertexCount = len(attrib.data)
    
    def applyMatrix(self, matrix, variableName="vertexPosition"):
        """Applies a transformation matrix to itself."""
        
        oldPositionData = self.attributes[variableName].data
        newPositionData = []
        for oldPos in oldPositionData:
            newPos = oldPos.copy()
            
            # Add homogeneous fourth coordinate, multiply,
            #  and remove 4th coord
            newPos.append(1)
            newPos = matrix @ newPos
            newPos = list(newPos[0:3])
            
            # Add to new data list
            newPositionData.append(newPos)
            self.attributes[variableName].data = newPositionData
            
            # New data must be uploaded
            self.attributes[variableName].uploadData()
    
    
    def merge(self, otherGeometry):
        for variableName, attributeObject in self.attributes.items():
            attributeObject.data += otherGeometry.attributes[variableName].data
            
            # New data must be uploaded
            attributeObject.uploadData()
            
        # Update the number of vertices
        self.countVertices()
        
