"""
Author: Liz Matthews
Code modified from Developing Graphics Frameworks
  with Python and OpenGL by Lee Stemkoski and
  Michael Pascale.
"""

from OpenGL.GL import *

class OpenGLUtils(object):
    """Static methods to load and compile OpenGL shaders
       and link to create programs
    """
    @staticmethod
    def initializeShader(shaderCode, shaderType):
        # Specify required OpenGL/GLSL version
        shaderCode = '#version 330\n' + shaderCode
        
        # Create empty shader object and return reference
        #  value
        shaderRef = glCreateShader(shaderType)
        
        # Stores the source code in the shader
        glShaderSource(shaderRef, shaderCode)
        
        # Compiles source code previously stored in the
        #  shader object
        glCompileShader(shaderRef)
        
        # Queries whether shader compile was successful
        compileSuccess = glGetShaderiv(shaderRef,
                                       GL_COMPILE_STATUS)
        
        if not compileSuccess:
            # Retrieve error message
            errorMessage = glGetShaderInfoLog(shaderRef)
            
            # Free memory used to store shader program
            glDeleteShader(shaderRef)
            
            # Convert byte string to character string
            errorMessage = '\n' + errorMessage.decode('utf-8')
            
            raise Exception(errorMessage)
        
        # Compilation was successful
        return shaderRef
    
    @staticmethod
    def initializeProgram(vertexShaderCode,
                          fragmentShaderCode):
        
        vertexShaderRef = OpenGLUtils.initializeShader(
                                        vertexShaderCode,
                                        GL_VERTEX_SHADER)
        fragmentShaderRef = OpenGLUtils.initializeShader(
                                        fragmentShaderCode,
                                        GL_FRAGMENT_SHADER)
        # Create empty program object and store reference
        #  to it
        programRef = glCreateProgram()
        
        # Attach previously compiled shader programs
        glAttachShader(programRef, vertexShaderRef)
        glAttachShader(programRef, fragmentShaderRef)
        
        # Link vertex shader to fragment shader
        glLinkProgram(programRef)
        
        # Queries whether program link was successful
        linkSuccess = glGetProgramiv(programRef, GL_LINK_STATUS)
        
        if not linkSuccess:
            # Retrieve error message
            errorMessage = glGetProgramInfoLog(programRef)
            
            # Free memory used to store program
            glDeleteProgram(programRef)
            
            # Convert byte string to character string
            errorMessage = '\n' + errorMessage.decode('utf-8')
            
            raise Exception(errorMessage)
        
        # Linking was successful!
        return programRef

    
    @staticmethod
    def printSystemInfo():
        print(f"  Vendor: {glGetString(GL_VENDOR).decode('utf-8')}")
        print(f"Renderer: {glGetString(GL_RENDERER).decode('utf-8')}")
        print(f"OpenGL version supported: {glGetString(GL_VERSION).decode('utf-8')}" )
        print(f"  GLSL version supported: {glGetString(GL_SHADING_LANGUAGE_VERSION).decode('utf-8')}")
