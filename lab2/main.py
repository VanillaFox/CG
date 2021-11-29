import tkinter as tk
import math
import numpy as np
import matrix as mtx
import camera as cm
import roberts as rb
from functools import partial

class Object:
    def __init__(self):
        self.rotX = 0
        self.rotY = 0
        self.rotZ = 0
        self.dx = 0
        self.dy = 0
        self.dz = 0
        self.scale = 30
        self.points = []
        self.polygon = []
        self.readModel()

    def readModel(self):
        with open('trapeze.txt') as file:
            for line in file:
                label, *lineSplit = line.split()
                if label=='v':
                    self.points.append(np.array(list(map(float, lineSplit))+[1]))
                else:
                    self.polygon.append(list(map(int, lineSplit)))


def MVPMatrix(object):
    return mtx.ModelMatrix(object) @ camera.ViewMatrix() @ camera.projectionMatrix()


def OMVPMatrix(object):
    return mtx.ModelMatrix(object) @ camera.ViewMatrix() @ camera.orthogonalMatrix()


def redraw(event, object):
    camera.height = window.winfo_height()
    camera.width = window.winfo_width()
    camera.v_fov = camera.h_fov * (camera.height/camera.width)
    drawOrthogonalProjection(object)


def keyMove(event, object):
    if event.keycode==25:
        object.rotX -= 3
    elif event.keycode==38:
        object.rotY += 3
    elif event.keycode==39:
        object.rotX += 3
    elif event.keycode==40:
        object.rotY -= 3
    else:
        print(event.keycode)
        return
    drawOrthogonalProjection(object)


def drawLine(a, b):
    canvas.create_line(a[0], a[1], b[0], b[1], width=2)


def drawOrthogonalProjection(object):
    canvas.delete("all")
    robAlgo = rb.RobertsAlgo(object.points @ mtx.ModelMatrix(object), object.polygon, camera.ViewMatrix(), camera.position)
    vertex = object.points @ OMVPMatrix(object)
    for i in range(len(object.polygon)):
        if robAlgo[i] < 0:
            continue
        for j in range(len(object.polygon[i])):
            drawLine(vertex[object.polygon[i][j]], vertex[object.polygon[i][(j+1)%len(object.polygon[i])]])


def drawPerspectiveProjection(object):
    vertex = object.points @ MVPMatrix()
    vertex /= vertex[:, -1].reshape(-1, 1)
    vertices_indices = np.all(~((vertex > 1) | (vertex < -1)), axis=-1)
    vertex = vertex @ camera.toScreenMatrix()

    for i in range(len(polygon)):
        for j in range(len(polygon[i])):
            a = vertex[object.polygon[i][j]]
            b = vertex[object.polygon[i][(j+1)%len(object.polygon[i])]]
            if not(a and b):
                continue
            drawLine(a, b)


if __name__=="__main__":
    window = tk.Tk()
    canvas = tk.Canvas(window, bg = "pink")
    window.columnconfigure(0, weight=2, minsize=550)
    window.rowconfigure(0, weight=2, minsize=550)
    canvas.grid(row=0, column=0, sticky="nsew")
    trapeze = Object()
    camera = cm.Camera()
    window.geometry("700x700+550+150")
    window.minsize(window.winfo_width(), window.winfo_height())
    drawOrthogonalProjection(trapeze)
    window.bind("<Key>", partial(keyMove, object=trapeze))
    window.bind("<Configure>", partial(redraw, object=trapeze))
    window.mainloop()