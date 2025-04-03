"""
Author: Abid Jeem and Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from ..oGL.attribute import Attribute
from ..oGL.uniform import Uniform
from ..utils.vector import vec
from ..utils.matrix import Matrix

import numpy as np
from OpenGL.GL import *

class Object3D(object):        
    """As described in Developing Graphics Frameworks
       with Python and OpenGL by Lee Stemkoski and
       Michael Pascal.
       
       Edits include change to use absolute transformation
       values instead of accumulative values."""
       
    def __init__(self):
        self.parent   = None
        self.children = []
        self.rotation = vec(0,0,0)
        self.position = vec(0,0,0)
        self.scale    = vec(1,1,1)
    
    def update(self, deltaTime=0):
        """Stub method so that all objects can be called
           to update even if they do not need to update."""
        pass
        
    def add(self, child):
        self.children.append(child)
        child.parent = self
    
    def remove(self, child):
        self.children.remove(child)
        child.parent = None
    
    def getDescendantList(self):
        """Depth-first traversal to obtain a list of descendants."""
        descendants = []
        nodesToProcess = [self]
        while len(nodesToProcess) > 0:
            node = nodesToProcess.pop(0)
            descendants.append(node)
            nodesToProcess = node.children + nodesToProcess
            
        return descendants
    
    ## Absolute transformation calculation ##
    def getWorldMatrix(self):
        """Obtain the final transformation matrix based on all
           transforms in parent chain."""
        
        
        t = Matrix.makeIdentity()
        
        # create a new identity matrix
         # Note that you should set localCoord to False for all transformation calls in getWorldMatrix() for absolute transformations.
        
        # apply the scaling

        t=Matrix.scaleAsymmetric(t,self.scale[0],self.scale[1],self.scale[2],local=False)

        # rotations
        t=Matrix.rotate(t,self.rotation[0],self.rotation[1],self.rotation[2],local=False)

        
        # and translations, then return the copy. 
        t=Matrix.translate(t,self.position[0],self.position[1],self.position[2],local=False)
       
        if self.parent == None:
            return t
        else:
            return self.parent.getWorldMatrix() @ t
    
    ## Mutator methods to adjust absolute values for translations ##
        
    def setPosition(self,x,y=None,z=None):
        if y is None or z is None:
            x, y, z = x  
        self.position = vec(x, y, z)
        
    def setRotateX(self, angle):
        self.rotation[0] = angle
        
    def setRotateY(self, angle):
        self.rotation[1] = angle
        
    def setRotateZ(self, angle):
        self.rotation[2] = angle
    
    def setRotate(self,x,y,z):
        self.rotation= vec(x,y,z)
        
    def setScale(self,s):
        self.scale=vec(s,s,s)
        
    def setScaleAsymmetric(self,x,y,z):
        self.scale= vec(x,y,z)
    
        
    
        
        