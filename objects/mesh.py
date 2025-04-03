"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from .object3D import Object3D
from OpenGL.GL import *

class Mesh(Object3D):
    """Basline mesh class for storing geometry
       and materials. Creates a VAO and associates
       variables."""
       
    def __init__(self, geometry, material):
        super().__init__()
        self.geometry = geometry
        self.material = material
        
        self.visible = True
        
        # Set up associations between attributes stored
        # in geometry and shader program stored in material
        self.vaoRef = glGenVertexArrays(1)
        glBindVertexArray(self.vaoRef)
        for variableName, attributeObject in geometry.attributes.items():
            attributeObject.associateVariable(material.programRef,
                                              variableName)
            
        # Unbind this vertex array object
        glBindVertexArray(0)