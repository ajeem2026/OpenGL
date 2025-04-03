"""
Author: Liz Matthews
Code modified from Developing Graphics Frameworks
  with Python and OpenGL by Lee Stemkoski and
  Michael Pascale.
"""

from .objects import Moving
from .objects import Object3D
from .utils.vector import vec, magnitude, normalize
from .utils.matrix import Matrix
from .utils.definitions import EPSILON

from pygame.locals import *
import numpy as np

class MovementRig(Moving, Object3D):
    """A first-person perspective movement rig.
       WASD to move, ZX to ascend/descend, mouse
       movement to look around.
       
       WASD/ZX are oriented around the current look
       direction."""
       
    def __init__(self,
                 speed=2,
                 rotSpeed=np.radians(20)):
        
        super().__init__(speed, rotSpeed)
        Object3D.__init__(self)
        
        # Initialize attached Object3D
        self.lookAttachment = Object3D()
        self.children = [self.lookAttachment]
        self.lookAttachment.parent = self
        
        # Keep track of keys
        self.movement = { }
        for k in [K_w, K_a, K_s, K_d, K_q, K_e, K_z, K_x]:
            self.movement[k] = False
            
        self.velocityMap = {
            K_w : vec( 0, 0,-1),
            K_s : vec( 0, 0, 1),            
            K_a : vec(-1, 0, 0),            
            K_d : vec( 1, 0, 0),
            K_z : vec( 0,-1, 0),
            K_x : vec( 0, 1, 0)
        }
        
    # Override functions from Object3D class        
    def add(self, child):
        self.lookAttachment.add(child)
        
    def remove(self, child):
        self.lookAttachment.remove(child)
        
    def update(self, deltaTime):
        self.velocity = np.zeros((3))
        # Use the movement dictionary and velocity map to
        #  change the velocity
        
        
        """Algorithm to use Matrix Multiplication to Rotate Velocity
        """
        # Use the currently held keys to create a velocity vector with addition
        for key, pressed in self.movement.items():
            if pressed and key in self.velocityMap:
                self.velocity += self.velocityMap[key]
        
        #If the magnitude of the velocity vector without normalizing is greater than 0:
        if magnitude(self.velocity) > EPSILON:
            # Rotate velocity vector to match current rotation.
            
            #Create a rotation x and rotation y matrix
            x_rot = Matrix.makeRotationX(self.lookAttachment.rotation[0])
            y_rot = Matrix.makeRotationY(self.rotation[1])
            
            #Create a list from the velocity
            v= list(self.velocity)
            #Append 1.0 to the velocity list
            v.append(1.0)
            
            #Use matrix multiplication with X and Y (optionally just Y)
            XY= y_rot @ x_rot  

            
            #Set self.velocity to a numpy array of the velocity list, minus the last coordinate value
            self.velocity= np.array(v[:-1])
        
        super().update(deltaTime)
        
        
    def handleOtherInput(self, event, deltaTime):
        # Set the movement dictionary based on the movement
        #  keys
        if event.type in [KEYDOWN, KEYUP]:
            if event.key in self.movement:
                self.movement[event.key] = (event.type == KEYDOWN)
        # Set the rotation values based on mouse movement
        #  events
        elif event.type == MOUSEMOTION:
            #update Y rotation for turn
            #subtracting the relative x movement to match book key mapping 
            self.rotation[1] -= event.rel[0] * self.rotationalSpeed * deltaTime
            #update the lookAttachment's X rotation for look
            self.lookAttachment.rotation[0] += event.rel[1] * self.rotationalSpeed * deltaTime
        
    