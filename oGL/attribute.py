"""
Author: Liz Matthews
Code modified from Developing Graphics Frameworks
  with Python and OpenGL by Lee Stemkoski and
  Michael Pascale.
"""

from OpenGL.GL import *
import numpy as np

class Attribute(object):
    def __init__(self, dataType, data):
        # type of elements in data array:
        # int | float | vec2 | vec3 | vec4
        self.dataType = dataType
        
        # Array of data to be stored in buffer
        self.data = data
        
        # Reference of available buffer from GPU
        self.bufferRef = glGenBuffers(1)
        
        # Upload data immediately
        self.uploadData()
        
    
    def uploadData(self):
        """Upload this data to a GPU buffer"""
        
        # Convert numbers to 32 bit floats
        data = np.array(self.data).astype(np.float32)
        
        # Select buffer used by the following functions
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)
        
        # Store data in currently bound buffer
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)
    
        
    def associateVariable(self, programRef, variableName):
        """Associate variable in program with this buffer"""
        
        # Get reference for program variable with given
        #  name
        variableRef = glGetAttribLocation(programRef, variableName)
        
        # If the program does not reference the variable,
        #  then exit
        if variableRef == -1:
            return
        
        # Select buffer used by the following functions
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)
        
        # Specify how data will be read from the currently
        #  bound buffer into the specified variable
        if self.dataType == "int":
            glVertexAttribPointer(variableRef, 1, GL_INT,
                                  False, 0, None)
            
        elif self.dataType == "float":
            glVertexAttribPointer(variableRef, 1, GL_FLOAT,
                                  False, 0, None)
            
        elif self.dataType == "vec2":
            glVertexAttribPointer(variableRef, 2, GL_FLOAT,
                                  False, 0, None)
            
        elif self.dataType == "vec3":
            glVertexAttribPointer(variableRef, 3, GL_FLOAT,
                                  False, 0, None)
            
        elif self.dataType == "vec4":
            glVertexAttribPointer(variableRef, 4, GL_FLOAT,
                                  False, 0, None)
        else:
            raise Exception(f"Attribute {variableName} has unknown type {self.dataType}")
        
        # Indicate that data will be streamed to this variable
        glEnableVertexAttribArray(variableRef)
