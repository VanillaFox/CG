import math
import numpy as np
class Camera:
    def __init__(self):
        self.position = [0, 0, -9, 1.]
        self.forward = [0, 0, -1, 1]
        self.up = [0, 1, 0, 1]
        self.right = [1, 0, 0, 1]
        self.h_fov = math.pi/3
        self.height = 700
        self.width = 700
        self.v_fov = self.h_fov * (self.height/self.width)
        self.near_plane = 0.1
        self.far_plan = 100
    
    def viewMatrix(self):
        x, y, z, w = self.position
        rx, ry, rz, rw = self.right
        fx, fy, fz, fw = self.up
        ux, uy, uz, uw = self.forward
        matrix = np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [-x, -y, -z, 1]
        ])
        return matrix

    def projectionMatrix(self):
        right = math.tan(self.h_fov/2)
        left = -right
        top = math.tan(self.v_fov/2)
        bottom = -top

        m00 = 2/(right-left)
        m11 = 2/(top-bottom)
        m22 = (self.far_plan + self.near_plane)/(self.far_plan -self.near_plane)
        m32 = -2 * self.near_plane * self.far_plan/(self.far_plan -self.near_plane)

        matrix = np.array([
            [m00, 0, 0, 0],
            [0, m11, 0, 0],
            [0, 0, m22, 1],
            [0, 0, m32, 0]
        ])
        return matrix

    def toScreenMatrix(self):
        matrix = np.eye(4, dtype=float)
        matrix[0, 0] = self.width//2
        matrix[1, 1] = -self.height//2
        matrix[3, 0] = self.width//2
        matrix[3, 1] = self.height//2
        return matrix