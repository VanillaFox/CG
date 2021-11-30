import tkinter as tk
import math
import numpy as np
import matrix as mtx
import camera as cm
import roberts as rb
from functools import partial

class Object:
    def __init__(self, sx, sy, sz):
        self.rotX = 0
        self.rotY = 0
        self.rotZ = 0
        self.dx = 0
        self.dy = 0
        self.dz = 0
        self.scale = 1
        self.startPoints = []
        self.points = []
        self.polygon = []
        self.readModel()
        self.scretchStartModel(sx, sy, sz)

    def readModel(self):
        with open('trapeze.txt') as file:
            for line in file:
                label, *lineSplit = line.split()
                if label=='v':
                    self.startPoints.append(np.array(list(map(float, lineSplit))+[1]))
                else:
                    self.polygon.append(list(map(int, lineSplit)))

    def scretchStartModel(self, sx, sy, sz):
        self.points = self.startPoints @ mtx.stretchingMatrix(sx, sy, sz)


def MVPMatrix(object):
    return mtx.ModelMatrix(object) @ camera.ViewMatrix() @ camera.projectionMatrix()


def OMVPMatrix(object):
    return mtx.ModelMatrix(object) @ camera.ViewMatrix() @ camera.orthogonalMatrix()


def redraw(event, object):
    camera.height = canvas.winfo_height()
    camera.width = canvas.winfo_width()
    camera.v_fov = camera.h_fov * (camera.height/camera.width)
    drawOrthogonalProjection(object)


def changeStartModel(event, object):
    object.scretchStartModel(sx=scaleX.get(), sy=scaleY.get(), sz=scaleZ.get())
    drawOrthogonalProjection(object)

def changeScaleModel(event, object):
    object.scale = scale.get()
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
    window.title("Trapeze")
    window.columnconfigure(0, weight=4, minsize=550)
    window.columnconfigure([1, 2], weight=1, minsize=10)
    window.rowconfigure([0, 1, 2, 3], weight=1, minsize=100)
    canvas = tk.Canvas(window, bg='grey')
    frame = tk.Frame(window, relief="sunken", borderwidth=3)

    labelscaleX = tk.Label(master=frame, text='X')
    labelscaleY = tk.Label(master=frame, text='Y')
    labelscaleZ = tk.Label(master=frame, text='Z')
    labelscale = tk.Label(master=frame, text='Scale')

    scaleX = tk.Scale(frame, orient='horizontal', resolution=1, from_=1, to=100)
    scaleY = tk.Scale(frame, orient='horizontal', resolution=1, from_=1, to=100)
    scaleZ = tk.Scale(frame, orient='horizontal', resolution=1, from_=1, to=100)
    scale = tk.Scale(frame, orient='horizontal', resolution=1, from_=1, to=100)

    canvas.grid(row=0, column=0, sticky="nsew", rowspan=4)
    frame.grid(row=0, column=1, sticky="nsew", rowspan=4, columnspan=2)
    labelscaleX.grid(row=0, column=1, sticky="nsew")
    scaleX.grid(row=0, column=2, sticky="nsew")
    labelscaleY.grid(row=1, column=1, sticky="nsew") 
    scaleY.grid(row=1, column=2, sticky="nsew")
    labelscaleZ.grid(row=2, column=1, sticky="nsew")
    scaleZ.grid(row=2, column=2, sticky="nsew")
    labelscale.grid(row=3, column=1, sticky="nsew")
    scale.grid(row=3, column=2, sticky="nsew", columnspan=3)
    
    scaleX.set(10)
    scaleY.set(10)
    scaleZ.set(10)
    
    window.geometry("+550+150")
    window.update()
    window.minsize(window.winfo_width(), window.winfo_height())

    camera = cm.Camera(canvas)
    trapeze = Object(sx=scaleX.get(), sy=scaleY.get(), sz=scaleZ.get())
    drawOrthogonalProjection(trapeze)
    
    scaleX.bind("<ButtonRelease-1>", partial(changeStartModel, object=trapeze))
    scaleY.bind("<ButtonRelease-1>", partial(changeStartModel, object=trapeze))
    scaleZ.bind("<ButtonRelease-1>", partial(changeStartModel, object=trapeze))
    scale.bind("<ButtonRelease-1>", partial(changeScaleModel, object=trapeze))
    window.bind("<Key>", partial(keyMove, object=trapeze))
    window.bind("<Configure>", partial(redraw, object=trapeze))
    window.mainloop()