import math
import numpy as np

def genModel(ringCount=15, ringsPoints=9, R=5, r=2):
    with open('horseshoe.txt', 'w') as file:
        stepI = 200/ringCount
        stepJ = 360/ringsPoints
        curcyrcle = []
        for i in np.arange(90, 290, stepI):
            for j in np.arange(0, 360, stepJ):
                x = (R+r*math.cos(math.pi/180 * j))*math.sin(math.pi/180 * i)
                y = (R+r*math.cos(math.pi/180 * j))*math.cos(math.pi/180 * i)
                z = r*math.sin(math.pi/180 * j)
                point = [x, y, z]
                curcyrcle.append(point)
        curcyrcle = np.array(curcyrcle)
        for i in range(len(curcyrcle)):
            l = ['v ', str(curcyrcle[i][0]), ' ', str(curcyrcle[i][1]), ' ', str(curcyrcle[i][2]), '\n']
            file.writelines(l)
        
        for i in range(ringCount-1):
            l = []
            for j in range(ringsPoints):
                l.append('f ')
                l.append(str(j + i*ringsPoints))
                l.append(' ')
                l.append(str(j+(i+1)*ringsPoints))
                l.append(' ')
                l.append(str((j+1)%ringsPoints + (i+1)*ringsPoints))
                l.append(' ')
                l.append(str((j+1)%ringsPoints + i*ringsPoints))
                l.append('\n')
                file.writelines(l)
                l.clear()
        r = []
        l = ['f']
        for i in range(ringsPoints):
            l.append(' ')
            l.append(str(i))
            r.append(str(i + (ringCount-1)*ringsPoints))
            r.append(' ')
        r.reverse()
        r.insert(0, 'f')
        l.append('\n')
        r.append('\n')
        file.writelines(l)
        file.writelines(r)