#workshop_07

"""Reproduction of windows and doors"""

from pyplasm import *

"""Function to create colors from RGB"""
def intRGBColor(values):
    return Color4f([values[0]/255.0,values[1]/255.0,values[2]/255.0,1.0])


""" xArray = array corresponds to the x
    yArray = array corresponds to the y
    slot = array of arrays that determines which cells are glass and such wooden"""

#window1
xArray = [0.0,0.1,0.5,0.6,1.0,1.1]
yArray = [0.0,0.1,1.025,1.1,1.275,1.4]
slot = [[1,1,1,1,1],[1,0,0,0,1],[1,1,1,1,1],[1,0,0,0,1],[1,1,1,1,1]]

#window2
#xArray = [0.0,0.1,0.525,0.575,1.0,1.1]
#yArray = [0.0,0.1,0.425,0.475,0.825,0.875,1.225,1.3]
#slot = [[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1]]

#door1
#xArray = [0.0,0.2,0.4,0.425,0.625,0.825]
#yArray = [0.0,0.4,0.65,0.7,0.95,1.0,1.25,1.3,1.55,1.6,1.85,2.05]
#slot = [[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1]]

""" Initial structure"""
init = QUOTE([.0,.0])
initStruct = STRUCT([init])

"""Function to create a window"""
def ggpl_window(i, j, partStruct):
    if j != len(yArray)-1:
        if  i != len(xArray)-1:
            if slot[j][i]==0:
                x = COLOR(intRGBColor([178,255,255]))(CUBOID([xArray[i+1]-xArray[i],yArray[j+1]-yArray[j],0.01]))
                struct = STRUCT([T([1,2,3])([xArray[i],yArray[j],0.1/3]), x])
            else:
                x = COLOR(BROWN)(CUBOID([xArray[i+1]-xArray[i],yArray[j+1]-yArray[j],0.1]))
                struct = STRUCT([T([1,2])([xArray[i],yArray[j]]), x])
            partStruct = STRUCT([partStruct,struct])
            return ggpl_window(i+1, j, partStruct)
        else:
            return ggpl_window(0, j+1, partStruct)
    else:
        VIEW(partStruct)

"""Function to create a door"""
def ggpl_door(i, j, partStruct):
    if j != len(yArray)-1:
        if  i != len(xArray)-1:
            if slot[j][i]==0:
                x = COLOR(intRGBColor([157,161,170]))(CUBOID([xArray[i+1]-xArray[i],yArray[j+1]-yArray[j],0.01]))
                struct = STRUCT([T([1,2,3])([xArray[i],yArray[j],0.1/3]), x])
            else:
                x = COLOR(intRGBColor([166,100,046]))(CUBOID([xArray[i+1]-xArray[i],yArray[j+1]-yArray[j],0.1]))
                struct = STRUCT([T([1,2])([xArray[i],yArray[j]]), x])
            partStruct = STRUCT([partStruct,struct])
            return ggpl_door(i+1, j, partStruct)
        else:
            return ggpl_door(0, j+1, partStruct)
    else:
        VIEW(partStruct)


ggpl_window(0, 0, initStruct)
#ggpl_door(0, 0, initStruct)



