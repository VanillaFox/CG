import tkinter as tk
import math
import numpy as np
import matrix as mtrx
import camera as cmr
startVertex = []
polygon = []
rotX = 0
rotY = 0
rotZ = 0
camera = cmr.Camera()
# def RobertsAlgo():
#     for 

def readModel():
    global startVertex, polygon
    file = open('cube.txt')
    for line in file:
        lineSplit = line.split()
        if lineSplit[0]=='v':
            startVertex.append([int(lineSplit[1]), int(lineSplit[2]), int(lineSplit[3]), 1])
        else:
            polygon.append([int(lineSplit[1]), int(lineSplit[2]), int(lineSplit[3]), int(lineSplit[4])])


def redraw(event):
    print("HERE")
    print(camera.height, camera.width)
    drawModel()

def keyMove(event):
    global rotX, rotY, rotZ
    if event.keycode==25:
        rotX += 5
    elif event.keycode==39:
        rotX -= 5
    elif event.keycode==38:
        rotY -= 5
    elif event.keycode==40:
        rotY += 5
    else:
        print(event.keycode)
        return
    drawModel()

def drawModel():
    global startVertex, polygon
    global rotX, rotY, camera
    canvas.delete("all")
    # Model = Rotate * Scale * Translate
    # finalModel =  modelMatrix * vertex
    matrix = np.eye(4, dtype=float)

    if rotX!=0:
        matrix = matrix@mtrx.rotXMatrix(rotX)
    if rotY!=0:
        matrix = matrix@mtrx.rotYMatrix(rotY)
    matrix = matrix
    matrix =  matrix @ camera.viewMatrix() @camera.projectionMatrix()
    vertexes = startVertex @ matrix
    vertexes /= vertexes[:, -1].reshape(-1, 1)
    vertices_indices = np.all(~((vertexes > 1) | (vertexes < -1)), axis=-1)
    vertexes = vertexes @ camera.toScreenMatrix()
    vertexes = vertexes[:, :2]
    for i in range(len(polygon)):
        for j in range(len(polygon[i])):
            if not(vertices_indices[polygon[i][j]] and vertices_indices[polygon[i][(j+1)%4]]):
                continue 
            vert1 = vertexes[polygon[i][j]]
            vert2 = vertexes[polygon[i][(j+1)%4]]
            canvas.create_line(vert1[0], vert1[1], vert2[0], vert2[1], width=2)
 
if __name__=="__main__":
    rotX = 0
    rotY = 0
    rotZ = 0
    camera = cmr.Camera()
    window = tk.Tk()
    window.geometry("700x700+550+150")
    window.columnconfigure(0, weight=2, minsize=550)
    window.rowconfigure(0, weight=2, minsize=550)
    readModel()
    canvas = tk.Canvas(window, bg="pink")
    canvas.grid(row=0, column=0, sticky="nsew")
    window.update()
    canvas.update()
    drawModel()
    window.minsize(window.winfo_width(), window.winfo_height())
    window.bind("<Configure>", redraw)
    window.bind("<Key>", keyMove)
    window.mainloop()