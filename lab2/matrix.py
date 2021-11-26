import numpy as np
import math

def rotXMatrix(a):
    rads = math.pi/180 * a
    matrix = np.eye(4, dtype=float)
    matrix[1, 1] = math.cos(rads)
    matrix[1, 2] = math.sin(rads)
    matrix[2, 1] = -math.sin(rads)
    matrix[2, 2] = math.cos(rads)
    return matrix

def rotYMatrix(a):
    rads = math.pi/180 * a
    matrix = np.eye(4, dtype=float)
    matrix[0, 0] = math.cos(rads)
    matrix[0, 2] = -math.sin(rads)
    matrix[2, 0] = math.sin(rads)
    matrix[2, 2] = math.cos(rads)
    return matrix

def rotZMatrix(a):
    rads = math.pi/180 * a
    matrix = np.eye(4, dtype=float)
    matrix[0, 0] = math.cos(rads)
    matrix[0, 1] = math.sin(rads)
    matrix[1, 0] = -math.sin(rads)
    matrix[1, 1] = math.cos(rads)
    return matrix

def stretchingMatrix(a, b, c):
    matrix = np.eye(4, dtype=float)
    matrix[0, 0] = a
    matrix[1, 1] = b
    matrix[2, 2] = c
    return matrix

def transferMatrix(dx, dy, dz):
    matrix = np.eye(4, dtype=float)
    matrix[3, 0] = dx
    matrix[3, 1] = dy
    matrix[3, 2] = dz
    return matrix