"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from .abstract import AbstractMaterial

class BasicMaterial(AbstractMaterial):
    """Contains basic shader codes."""
    
    def __init__(self):
        super().__init__("basic.vert", "basic.frag")
        self.addUniform("vec3", "baseColor", [1.0, 1.0, 1.0])
        self.addUniform("bool", "useVertexColors", False)
        self.locateUniforms()
        