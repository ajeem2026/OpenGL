"""
Author: Liz Matthews
Code modified from Developing Graphics Frameworks
  with Python and OpenGL by Lee Stemkoski and
  Michael Pascale.
"""

from modules.oGL.base import Base
from modules.renderer import Renderer
from modules.objects import Group, Scene, Camera, MovingMesh, AxesHelper, GridHelper
from modules.geometry import BoxGeometry, RainbowBowlGeometry, SphereGeometry, PyramidGeometry
from modules.geometry import PlaneGeometry

from modules.movementRig import MovementRig
from modules.materials import SurfaceMaterial

import pygame
import numpy as np


class Main(Base):
    def handleOtherInput(self, event):
        self.rig.handleOtherInput(event, self.deltaTime)

    def initialize(self):
        print("Initializing program...")

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio=self.aspectRatio)

        self.rig = MovementRig()
        self.rig.add(self.camera)

        # The following does not work until part 2 is completed

        self.rig.setPosition([1, 1, 4])
        self.scene.add(self.rig)

        axes = AxesHelper(axisLength=2)
        self.scene.add(axes)
        grid = GridHelper(size=20, gridColor=[1, 1, 1],
                          centerColor=[1, 1, 0])
        grid.setRotateX(-np.pi/2)
        self.scene.add(grid)

        geometry = BoxGeometry()
        material = SurfaceMaterial({"useVertexColors": True})
        mesh = MovingMesh(geometry, material)
        mesh.setRotVel((0.0337, 0.0514, 0))
        mesh.setPosition([0, 1, -4])
        self.scene.add(mesh)

        # ====== FIRST ASSIGNMENT SCENE ADDITIONS=========================
        # Randomly colored floor
        # Set the parametric resolution low so the colors don't get too noisy

        # to add floor
        floor = PlaneGeometry(width=20, height=20,
                              widthSegments=10, heightSegments=10)
        floorMat = SurfaceMaterial({"useVertexColors": True})
        floorMesh = MovingMesh(floor, floorMat)
        floorMesh.setPosition([1, 0, 1])
        floorMesh.setRotateX(-np.pi/2)
        self.scene.add(floorMesh)

        # =======
        # A blue table

        # Made from several boxes SO USE BOXGEO
        # Use a Group object to organize the table as a single object in the world.

        table = Group()
        tableGeo = BoxGeometry(width=4, height=0.2, depth=2)
        # bleu color table
        tableMat = SurfaceMaterial(
            {"useVertexColors": False, "baseColor": [0, 0, 1]})
        tableMesh = MovingMesh(tableGeo, tableMat)

        tableMesh.setPosition([0, 1.5, 0])
        table.add(tableMesh)

        # TABLE LEGGS
        legGeo = BoxGeometry(width=0.2, height=1, depth=0.2)
        # Distinguish the legs by setting them to a slightly different blue color
        legMat = SurfaceMaterial(
            {"useVertexColors": False, "baseColor": [0, 0, 0.5]})

        # four legs at corners 
        for X in [1, -1]:
            for Z in [1, -1]:
                leg = MovingMesh(legGeo, legMat)
                leg.setPosition([X * 1.9, 1, Z * 0.9])
                table.add(leg)
        self.scene.add(table)

        # =======
        # RainbowBowl

        bowlGeo = RainbowBowlGeometry(
            radius=0.8, uResolution=32, vResolution=16)
        bowlMat = SurfaceMaterial(
            {"useVertexColors": True, "doubleSide": True})
        bowlMesh = MovingMesh(bowlGeo, bowlMat)

        # bowl on the table
        bowlMesh.setPosition([0, 2.6, 0])

        bowlMesh.setRotateX(0)
        table.add(bowlMesh)

        # =======
        # Bowl Shapes

        smallSphere = SphereGeometry(
            radius=0.3, radiusSegments=16, heightSegments=8)
        smallSphereMat = SurfaceMaterial(
            {"useVertexColors": False, "baseColor": [1, 0, 0]})
        smallSphereMesh = MovingMesh(smallSphere, smallSphereMat)
        smallSphereMesh.setPosition([0.2, 0.2, 0])
        bowlMesh.add(smallSphereMesh)

        smallBox = BoxGeometry(width=0.4, height=0.4, depth=0.4)
        smallBoxMat = SurfaceMaterial(
            {"useVertexColors": False, "baseColor": [0, 1, 0]})
        smallBoxMesh = MovingMesh(smallBox, smallBoxMat)

        smallBoxMesh.setPosition([-0.3, 0.1, 0.3])
        bowlMesh.add(smallBoxMesh)

        # =======
        # Pyramid

        pyramid = PyramidGeometry(
            radius=1, height=1.5, sides=4, heightSegments=4, closed=True)
        pyMat = SurfaceMaterial(
            {"useVertexColors": False, "baseColor": [0.5, 0, 0.5]})
        pyMesh = MovingMesh(pyramid, pyMat)

        pyMesh.setPosition([4, 2, 0])
        pyMesh.setRotVel((0.0337, 0.0514, 0))

        self.scene.add(pyMesh)

        print("Initialization done!")

    def update(self):
        """Most of the work is in scene, rig, and renderer!"""

        self.scene.update(self.deltaTime)
        self.rig.update(self.deltaTime)
        self.renderer.render(self.scene, self.camera)


if __name__ == '__main__':
    Main(fullScreen=True).run()
