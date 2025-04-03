"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from . import Object3D
from . import Mesh
from ..utils.matrix import Matrix
from numpy.linalg import inv

class Scene(Object3D):
    def __init__(self):
        super().__init__()
    
    def update(self, deltaTime):
        descendantList = self.getDescendantList()
        
        meshList = [x for x in descendantList if isinstance(x, Mesh)]
        
        for mesh in meshList:
            # Only update if the mesh is visible
            if mesh.visible:        
                mesh.update(deltaTime)
            

class Group(Object3D):
    def __init__(self):
        super().__init__()
        

class Camera(Object3D):
    def __init__(self, angleOfView=60,
                 aspectRatio=1, near=0.1, far=1000):
        super().__init__()
        self.projectionMatrix = Matrix.makePerspective(angleOfView,
                                                       aspectRatio,
                                                       near, far)
        self.viewMatrix = Matrix.makeIdentity()
    
    def updateViewMatrix(self):
        self.viewMatrix = inv(self.getWorldMatrix())