"""
Author: Liz Matthews
Code modified from Developing Graphics Frameworks
  with Python and OpenGL by Lee Stemkoski and
  Michael Pascale.
"""

from OpenGL.GL import *
from .objects.mesh import Mesh

class Renderer(object):
    """Handles the rendering of all meshes in the scene."""
    
    def __init__(self, clearColor=[0,0,0]):
        glEnable( GL_DEPTH_TEST )
        
        # Required for antialiasing
        glEnable( GL_MULTISAMPLE )
        glClearColor(clearColor[0], clearColor[1], clearColor[2], 1)
        
    def render(self, scene, camera):
        # Clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Update camera view
        camera.updateViewMatrix()
        
        # Extract list of all Mesh objects in scene
        descendantList = scene.getDescendantList()        
        meshList = [x for x in descendantList if isinstance(x, Mesh)]
        
        for mesh in meshList:
            
            # Only try to render if the mesh is visible.
            if mesh.visible:            
                glUseProgram(mesh.material.programRef)
                
                # Bind VAO
                glBindVertexArray(mesh.vaoRef)
                
                # Update uniform values stored outside of material
                mesh.material.uniforms["modelMatrix"].data = mesh.getWorldMatrix()
                mesh.material.uniforms["viewMatrix"].data = camera.viewMatrix
                mesh.material.uniforms["projectionMatrix"].data = camera.projectionMatrix
                
                # Update uniforms stored in material
                for variableName, uniformObject in mesh.material.uniforms.items():
                    uniformObject.uploadData()
                    
                # Update render settings
                mesh.material.updateRenderSettings()
                glDrawArrays(mesh.material.settings["drawStyle"],
                             0, mesh.geometry.vertexCount)