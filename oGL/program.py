"""
Author: Liz Matthews
"""

from .openGLUtils import OpenGLUtils
from os.path import join

class Program(object):
    SHADER_FOLDER = join("modules", "shaders")
    
    @staticmethod
    def build(vShaderFiles, fShaderFiles):
    
        if type(vShaderFiles) == str:
            vShaderFiles = [vShaderFiles]
        if type(fShaderFiles) == str:
            fShaderFiles = [fShaderFiles]
            
        vShaderCode = ""
        for vShaderFile in list(vShaderFiles):
            vfp = open(join(Program.SHADER_FOLDER, vShaderFile), "r")
            vShaderCode += vfp.read()
            vfp.close()
            
        fShaderCode = ""
        for fShaderFile in list(fShaderFiles):
            ffp = open(join(Program.SHADER_FOLDER, fShaderFile), "r")
            fShaderCode += ffp.read()
            ffp.close()
        
        ref = OpenGLUtils.initializeProgram(vShaderCode,
                                            fShaderCode)
        return ref
    
