"""
Author: Liz Matthews
Code modified from Developing Graphics Frameworks
  with Python and OpenGL by Lee Stemkoski and
  Michael Pascale.
"""

from OpenGL.GL import *

class Uniform(object):
    def __init__(self, dataType, data):
        # type of data:
        #  int | bool | float | vec2 | vec3 | vec4 | mat4
        self.dataType = dataType
        
        self.data = data
        
        self.variableRef = None
    
    def locateVariable(self, programRef, variableName):
        self.variableRef = glGetUniformLocation(programRef,
                                                variableName)
    
    def uploadData(self):
        if self.variableRef == -1:
            return
        
        if self.dataType == "int":
            glUniform1i(self.variableRef, self.data)
        elif self.dataType == "bool":
            glUniform1i(self.variableRef, self.data)
        elif self.dataType == "float":
            glUniform1f(self.variableRef, self.data)
        elif self.dataType == "vec2":
            glUniform2f(self.variableRef, self.data[0], self.data[1])
        elif self.dataType == "vec3":
            glUniform3f(self.variableRef, self. data[0],
                        self.data[1], self.data[2])
        elif self.dataType == "vec4":
            glUniform4f(self.variableRef, self.data[0],
                        self.data[1], self.data[2], self.data[3])
        elif self.dataType == "mat4":
            glUniformMatrix4fv(self.variableRef, 1, GL_TRUE, self.data)
        