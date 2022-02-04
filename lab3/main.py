import tkinter as tk
import math
import numpy as np
import matrix as mtx
import camera as cm
from functools import partial
import gen_horseshoe as gen

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
        self.normal = []
        self.readModel()
        self.scretchStartModel(sx, sy, sz)

    def EqSurfaces(self):
        D = np.array([[-1],[-1],[-1]])
        matrixV = []
        curMatrix = (self.points @ mtx.ModelMatrix(self))
        for i in range(len(self.polygon)):
            cur = curMatrix[self.polygon[i][:3]][:3, :3]
            matrix = np.linalg.inv(cur) @ D
            matrixV.append(matrix)
        matrixV = np.array(matrixV)
        return matrixV

    def readModel(self):
        self.startPoints = []
        self.polygon = []
        with open('figure/horseshoe.txt') as file:
            for line in file:
                label, *lineSplit = line.split()
                if label=='v':
                    self.startPoints.append(np.array(list(map(float, lineSplit))+[1]))
                elif label=='f':
                    self.polygon.append(list(map(lambda x: int(x)-1, lineSplit)))

    def scretchStartModel(self, sx, sy, sz):
        self.points = self.startPoints @ mtx.stretchingMatrix(sx, sy, sz)

def StartModel(event, object):
    gen.genModel(R=scaleR.get(), r=scaler.get(), ringCount=scaleRingCount.get(), ringsPoints=scaleRingPoints.get())
    object.readModel()
    changeStartModel(object)

def OMVPMatrix(object):
    return mtx.ModelMatrix(object) @ camera.ViewMatrix() @ camera.orthogonalMatrix()

def redraw(event, object):
    camera.height = canvas.winfo_height()
    camera.width = canvas.winfo_width()
    camera.v_fov = camera.h_fov * (camera.height/camera.width)
    drawOrthogonalProjection(object)

def changeStartModel(object):
    object.scretchStartModel(sx=scaleX.get(), sy=scaleY.get(), sz=scaleZ.get())
    drawOrthogonalProjection(object)

def evChangeStartModel(event, object):
    changeStartModel(object)

def changeScaleModel(event, object):
    object.scale = scale.get()
    drawOrthogonalProjection(object)

def keyMove(event, object):
    if event.keycode==25:
        object.rotX += 3
    elif event.keycode==38:
        object.rotY -= 3
    elif event.keycode==39:
        object.rotX -= 3
    elif event.keycode==40:
        object.rotY += 3
    else:
        print(event.keycode)
        return
    drawOrthogonalProjection(object)

def torgb(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

def drawOrthogonalProjection(object):
    canvas.delete("all")
    #transformedVertices = modelVertices * model * view * projection
    vertex = object.points @ OMVPMatrix(object)
    # sorting polygons on the z axis
    object.polygon = sorted(object.polygon, key=lambda x: vertex[x[2]][2])
    for i in range(len(object.polygon)):
        vec1 = np.array(vertex[object.polygon[i][0]]-vertex[object.polygon[i][1]])[:3]
        vec2 = np.array(vertex[object.polygon[i][2]]-vertex[object.polygon[i][1]])[:3]
        normal = np.cross(vec1, vec2)
        normal = normal/math.sqrt(normal @ normal)
        # view vector
        pos = camera.position
        pos = pos/math.sqrt(pos @ pos)
        pos = pos @ normal
        if pos > 0:      
            points = []
            for j in range(len(object.polygon[i])):
                points.append(vertex[object.polygon[i][j]][0])
                points.append(vertex[object.polygon[i][j]][1])
            canvas.create_polygon(points, fill=torgb(int(155*pos), int(185*pos), int(115*pos)))

if __name__=="__main__":
    window = tk.Tk()
    window.title("Software rendering")
    window.columnconfigure(0, weight=5, minsize=550)
    window.columnconfigure([1, 2], weight=1, minsize=10)
    window.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7], weight=1, minsize=100)
    canvas = tk.Canvas(window, bg = '#F2DDC1')
    frame = tk.Frame(window, relief="sunken", borderwidth=3)

    labelscaleX = tk.Label(master=frame, text='X')
    labelscaleY = tk.Label(master=frame, text='Y')
    labelscaleZ = tk.Label(master=frame, text='Z')
    labelscale = tk.Label(master=frame, text='Scale')
    labelR = tk.Label(master=frame, text='R')
    labelr = tk.Label(master=frame, text='r')
    labelRingCount = tk.Label(master=frame, text='Rings count')
    labelRingPoints = tk.Label(master=frame, text='Points count')

    scaleX = tk.Scale(frame, orient='horizontal', resolution=1, from_=1, to=100)
    scaleY = tk.Scale(frame, orient='horizontal', resolution=1, from_=1, to=100)
    scaleZ = tk.Scale(frame, orient='horizontal', resolution=1, from_=1, to=100)
    scale = tk.Scale(frame, orient='horizontal', resolution=1, from_=1, to=100)
    scaleR = tk.Scale(frame, orient='horizontal', resolution=1, from_=1, to=100)
    scaler = tk.Scale(frame, orient='horizontal', resolution=1, from_=1, to=100)
    scaleRingCount = tk.Scale(frame, orient='horizontal', resolution=1, from_=1, to=50)
    scaleRingPoints = tk.Scale(frame, orient='horizontal', resolution=1, from_=1, to=100)

    canvas.grid(row=0, column=0, sticky="nsew", rowspan=8)
    frame.grid(row=0, column=1, sticky="nsew", rowspan=8, columnspan=2)
    labelscaleX.grid(row=0, column=1, sticky="nsew")
    scaleX.grid(row=0, column=2, sticky="nsew")
    labelscaleY.grid(row=1, column=1, sticky="nsew") 
    scaleY.grid(row=1, column=2, sticky="nsew")
    labelscaleZ.grid(row=2, column=1, sticky="nsew")
    scaleZ.grid(row=2, column=2, sticky="nsew")
    labelscale.grid(row=3, column=1, sticky="nsew")
    scale.grid(row=3, column=2, sticky="nsew")
    labelR.grid(row=4, column=1, sticky="nsew")
    scaleR.grid(row=4, column=2, sticky="nsew")
    labelr.grid(row=5, column=1, sticky="nsew")
    scaler.grid(row=5, column=2, sticky="nsew")
    labelRingCount.grid(row=6, column=1, sticky="nsew")
    scaleRingCount.grid(row=6, column=2, sticky="nsew")
    labelRingPoints.grid(row=7, column=1, sticky="nsew")
    scaleRingPoints.grid(row=7, column=2, sticky="nsew")

    scaleX.set(25)
    scaleY.set(25)
    scaleZ.set(25)
    scaleR.set(5)
    scaler.set(2)
    scaleRingCount.set(15)
    scaleRingPoints.set(9)
    
    window.geometry("+550+150")
    window.update()
    window.minsize(window.winfo_width(), window.winfo_height())

    camera = cm.Camera(canvas)
    gen.genModel()
    trapeze = Object(sx=scaleX.get(), sy=scaleY.get(), sz=scaleZ.get())
    drawOrthogonalProjection(trapeze)
    
    scaleX.bind("<ButtonRelease-1>", partial(evChangeStartModel, object=trapeze))
    scaleY.bind("<ButtonRelease-1>", partial(evChangeStartModel, object=trapeze))
    scaleZ.bind("<ButtonRelease-1>", partial(evChangeStartModel, object=trapeze))
    scale.bind("<ButtonRelease-1>", partial(changeScaleModel, object=trapeze))
    scaleR.bind("<ButtonRelease-1>", partial(StartModel, object=trapeze))
    scaler.bind("<ButtonRelease-1>", partial(StartModel, object=trapeze))
    scaleRingCount.bind("<ButtonRelease-1>", partial(StartModel, object=trapeze))
    scaleRingPoints.bind("<ButtonRelease-1>", partial(StartModel, object=trapeze))
    window.bind("<Key>", partial(keyMove, object=trapeze))
    window.bind("<Configure>", partial(redraw, object=trapeze))
    window.mainloop()