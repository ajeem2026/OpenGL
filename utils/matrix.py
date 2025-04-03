"""
Author: Abid Jeem and Liz Matthews
Code modified from Developing Graphics Frameworks
  with Python and OpenGL by Lee Stemkoski and
  Michael Pascale.
"""

import numpy as np


class Matrix(object):
    @staticmethod
    def makeIdentity():
        return np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]]).astype(float)

    @staticmethod
    def makeTranslation(x, y, z):
        return np.array([[1, 0, 0, x],
                         [0, 1, 0, y],
                         [0, 0, 1, z],
                         [0, 0, 0, 1]]).astype(float)

    @staticmethod
    def makeRotationX(angle):
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([[1, 0, 0, 0],
                         [0, c, -s, 0],
                         [0, s, c, 0],
                         [0, 0, 0, 1]]).astype(float)

    @staticmethod
    def makeRotationY(angle):
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([[c, 0, s, 0],
                         [0, 1, 0, 0],
                         [-s, 0, c, 0],
                         [0, 0, 0, 1]]).astype(float)

    @staticmethod
    def makeRotationZ(angle):
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([[c, -s, 0, 0],
                         [s,  c, 0, 0],
                         [0,  0, 1, 0],
                         [0,  0, 0, 1]]).astype(float)

    # Add a makeRotate() static method to the Matrix class which takes three angles and returns a rotational matrix combining the x, y, and z angles of rotation
    @staticmethod
    def makeRotate(x, y, z):
        # Multiply the matrices returned by Matrix.makeRotation{X|Y|Z}
        # such that x is applied first, then y, then z. Matrix multiplication goes right to left.
        return np.dot(Matrix.makeRotationZ(z), np.dot(Matrix.makeRotationY(y), Matrix.makeRotationX(x)))

    @staticmethod
    def makeScale(s):
        return np.array([[s, 0, 0, 0],
                         [0, s, 0, 0],
                         [0, 0, s, 0],
                         [0, 0, 0, 1]]).astype(float)

    # Add a makeScaleAsymmetric() static method to the Matrix class which takes three scalars and then returns a scaling matrix
    # based on different scaling factors for x, y, and z.
    @staticmethod
    def makeScaleAsymmetric(x, y, z):
        return np.array([[x, 0, 0, 0],
                         [0, y, 0, 0],
                         [0, 0, z, 0],
                         [0, 0, 0, 1]]).astype(float)

    @staticmethod
    def makePerspective(angleOfView=60, aspectRatio=1, near=0.1, far=1000):
        a = angleOfView * np.pi / 180.0
        d = 1.0 / np.tan(a/2)
        r = aspectRatio
        b = (far + near) / (near - far)
        c = 2*far*near / (near - far)
        return np.array([[d/r, 0, 0, 0],
                         [0, d, 0, 0],
                         [0, 0, b, c],
                         [0, 0, -1, 0]]).astype(float)

    # Add an applyMatrix() static method to the Matrix class which takes three parameters
    # The first parameter is the transform matrix on which the new matrix will be applied.
    # The second parameter is the matrix to apply.
    # The third parameter is if the transformation should be done with local coordinates, which changes the order in which multiplication is applied.

    @staticmethod
    def applyMatrix(transform_matrix, apply_matrix, local=False):
        if local:
            return np.dot(transform_matrix, apply_matrix)
        else:
            return np.dot(apply_matrix, transform_matrix)

    # Add static methods for all transformations that can be applied, using your new applyMatrix() method.
    # All of these methods should return the newly transformed matrix

    @staticmethod
    def translate(transform_matrix, x, y, z, local=False):
        return Matrix.applyMatrix(transform_matrix, Matrix.makeTranslation(x, y, z), local)

    @staticmethod
    def rotateX(transform_matrix, angle, local=False):
        return Matrix.applyMatrix(transform_matrix, Matrix.makeRotationX(angle), local)

    @staticmethod
    def rotateY(transform_matrix, angle, local=False):
        return Matrix.applyMatrix(transform_matrix, Matrix.makeRotationY(angle), local)

    @staticmethod
    def rotateZ(transform_matrix, angle, local=False):
        return Matrix.applyMatrix(transform_matrix, Matrix.makeRotationZ(angle), local)

    @staticmethod
    def rotate(transform_matrix, x, y, z, local=False):
        return Matrix.applyMatrix(transform_matrix, Matrix.makeRotate(x, y, z), local)

    @staticmethod
    def scale(transform_matrix, s, local=False):
        return Matrix.applyMatrix(transform_matrix, Matrix.makeScale(s), local)

    @staticmethod
    def scaleAsymmetric(transform_matrix, x, y, z, local=False):
        return Matrix.applyMatrix(transform_matrix, Matrix.makeScaleAsymmetric(x, y, z), local)

    @staticmethod
    def inverse(matrix):
        return np.linalg.inv(matrix)
