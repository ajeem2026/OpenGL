"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from ..oGL.openGLUtils import OpenGLUtils
from ..oGL.program import Program
from ..oGL.uniform import Uniform
from OpenGL.GL import *

class AbstractMaterial(object):
    """Abstract baseline material. Stores uniforms,
       draw style, program reference. Can create a program
       from a list of shader files or be given an external
       program reference."""
    def __init__(self, vShaderFiles=["basic.vert"],
                       fShaderFiles=["basic.frag"],
                       programRef=None):
        if programRef:
            self.programRef = programRef
        else:
            self.programRef = Program.build(vShaderFiles, fShaderFiles)
        
        # Uniform objects indexed by name of associated variable in shader
        self.uniforms = {}
        
        # Guaranteed uniforms for all shaders
        self.uniforms["modelMatrix"] = Uniform("mat4", None)
        self.uniforms["viewMatrix"] = Uniform("mat4", None)
        self.uniforms["projectionMatrix"] = Uniform("mat4", None)
        
        # OpenGL render settings indexed by variable name     
        self.settings = {}
        self.settings["drawStyle"] = GL_TRIANGLES
        
    def addUniform(self, dataType, variableName, data):
        self.uniforms[variableName] = Uniform(dataType, data)
    
    def locateUniforms(self):
        for variableName, uniformObject in self.uniforms.items():
            uniformObject.locateVariable(self.programRef,
                                         variableName )
            
    def updateRenderSettings(self):
        pass
    
    # Convenience method for setting multiple material "properties"
    # (uniform and render setting values) from a dictionary
    def setProperties(self, properties):
        for name, data in properties.items():
            # Update uniforms
            if name in self.uniforms.keys():
                self.uniforms[name].data = data
                
            # Update render settings
            elif name in self.settings.keys():
                self.settings[name] = data
                
            # Unknown property type
            else:
                raise Exception(f"Material has no property named: {name}")
            
