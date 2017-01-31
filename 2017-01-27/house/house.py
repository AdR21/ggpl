""" workshop 10 """
from pyplasm import *
import numpy as np
import sys, os

sys.setrecursionlimit(1500)

pavTexture = "house/texture/pav4.jpg"
wallTexture = "house/texture/wall1.jpg"
wallStone = "house/texture/wall6.jpg"
doorTexture = "house/texture/wood.jpg"
metalTexture = "house/texture/metal.jpg"
glassTexture = "house/texture/glass.jpg"
roofTexture = "house/texture/roof.png"

zero = CUBOID([.0,.0,.0])
initStruct = STRUCT([zero])
levelHeight = [30.0,30.0,20.0,30.0,30.0,20.0]
heights = [60.0,20.0,3.5,60.0,20.0]

def countFileDirectory(path):
  i = 0
  for name in os.listdir(path):
      if not name.startswith('.'):
        i = i + 1
  return i

def readSvg(l,readingLevel,path):
  file = open("house/components/"+path+"/lines/level-"+str(l)+".lines","r")
  data = file.read()
  n = countFileDirectory("house/components/"+path+"/lines/")
  file.close()
  d = data.splitlines()
  readingLevel = readingLevel + [d]
  if l!=n-1:
    return readSvg(l+1,readingLevel,path)
  else:
    return readingLevel

levelBase = readSvg(0,[],"base")
levelExternal = readSvg(0,[],"esterno")
levelInternal = readSvg(0,[],"interno")
levelDoors = readSvg(0,[],"porte")
levelWindows = readSvg(0,[],"finestre")
levelStair = readSvg(0,[],"scale")

def parseLines(l,i, params):
  stringLine = params[l][i]
  splitLine = stringLine.split(",")
  arrayLine = np.array(splitLine, dtype=float)
  return arrayLine

#Creation first floor
def createFloor1(i,s1):
  if i < len(levelBase[0]):
    params = parseLines(0,i,levelBase)
    a_pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
    a_off = OFFSET([4.0, 5.5, 2.0])(a_pol)
    s2 = STRUCT([a_off, s1])
    return createFloor1(i+1,s2)
  else:
    s1 = SOLIDIFY(SKEL_2(s1))
    s1 = TEXTURE([pavTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(s1)
    return s1

#Creation external wall
def createExternalWalls(l,i,h,s1):
  if l <= len(levelExternal)-1:
    if i < len(levelExternal[l]):
      params = parseLines(l,i,levelExternal)
      a_pol = MKPOL([[[params[0],params[1],0.0],[params[0],params[3],0.0],[params[2],params[1],0.0],[params[2],params[3],0.0]],[[1,2,3,4]],[1]])
      a_off = OFFSET([3.0, 3.0, levelHeight[l]])(a_pol)
      if l==0:
        a_texture = TEXTURE([wallStone, TRUE, FALSE, 1, 1, 0, 2, 1])(a_off)
      else:
        if l==3:
          a_texture = TEXTURE([wallStone, TRUE, FALSE, 1, 1, 0, 6, 1])(a_off)
        else:
          a_texture = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 6, 1])(a_off)
      a_tras = STRUCT([T(3)(h), a_texture])
      s2 = STRUCT([a_tras, s1])
      return createExternalWalls(l,i+1,h,s2)
    else:
      h = h + levelHeight[l]
      return createExternalWalls(l+1,0,h,s1)
  else:
    return s1

#Creation internal wall
def createInternalWalls(l,i,h,s1):
  if l <= len(levelInternal)-1:
    if i < len(levelInternal[l]):
      params = parseLines(l,i,levelInternal)
      a_pol = MKPOL([[[params[0],params[1],0.0],[params[0],params[3],0.0],[params[2],params[1],0.0],[params[2],params[3],0.0]],[[1,2,3,4]],[1]])
      a_off = OFFSET([1.0, 1.0, levelHeight[l]])(a_pol)
      a_texture = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 2, 1])(a_off)
      a_tras = STRUCT([T(3)(h), a_texture])
      s2 = STRUCT([a_tras, s1])
      return createInternalWalls(l,i+1,h,s2)
    else:
      h = h + levelHeight[l]
      return createInternalWalls(l+1,0,h,s1)
  else:
    return s1

#Creation a door
def createDoor(elem, j, h, door):
  if j < 13:
    build = MKPOL([[[elem[0],elem[1],0.0],[elem[2],elem[3],0.0]],[[1,2]],[1]])
    if not j%2:
      buildOffset = OFFSET([3.5, 3.5, 8.5])(build)
      buildTexture = TEXTURE([doorTexture, TRUE, FALSE, 1, 1, 0, 6, 1])(buildOffset)
      buildTras = STRUCT([T([3])([h]), buildTexture])
      h = h + 8.5
    else:
      buildOffset = OFFSET([3.5, 3.5, 0.5])(build)
      buildTexture = TEXTURE([doorTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(buildOffset)
      buildTras = STRUCT([T([3])([h]), buildTexture])
      h = h + 0.5
    door = STRUCT([buildTras,door])
    return createDoor(elem, j+1, h, door)
  else:
    return door

#Creation handle's door
def createHandle(elem,s1):
  handle = MKPOL([[[elem[0],elem[1],0.0],[elem[2],elem[3],0.0]],[[1,2]],[1]])
  handle0 = OFFSET([8.0, 1.0, 1.0])(handle)
  if (elem[0]-elem[2]<1.0) & (elem[0]-elem[2]>-1.0):
    handle_0 = STRUCT([T([1,2,3])([-2.0,1.0,31.0]), handle0])
    handle_1 = STRUCT([T([1,2,3])([-2.0,3.0,31.0]), handle0])
    handle1 = OFFSET([1.0, 1.5, 1.0])(handle)
    handle_2 = STRUCT([T([1,2,3])([5.0,1.0,31.0]), handle1])
    handle_3 = STRUCT([T([1,2,3])([5.0,6.0,31.0]), handle1])
    handle_01 = DIFF([handle_0,handle_1])
    handle_23 = DIFF([handle_2,handle_3])
    handle_23_2 = STRUCT([T([1])([-8.0]), handle_23])
  else:
    handle = MKPOL([[[elem[0],elem[1],0.0],[elem[2],elem[3],0.0]],[[1,2]],[1]])
    handle0 = OFFSET([1.0, 8.0, 1.0])(handle)
    handle_0 = STRUCT([T([1,2,3])([1.0,-2.0,31.0]), handle0])
    handle_1 = STRUCT([T([1,2,3])([3.0,-2.0,31.0]), handle0])
    handle1 = OFFSET([1.0, 1.5, 1.0])(handle)
    handle_2 = STRUCT([T([1,2,3])([1.0,5.0,31.0]), handle1])
    handle_3 = STRUCT([T([1,2,3])([6.0,5.0,31.0]), handle1])
    handle_01 = DIFF([handle_0,handle_1])
    handle_23 = DIFF([handle_2,handle_3])
    handle_23_2 = STRUCT([T([2])([-8.0]), handle_23])
  handle_all = STRUCT([handle_01,handle_23,handle_23_2])
  handle_all = TEXTURE([metalTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(handle_all)
  s1 = STRUCT([s1,handle_all])
  return s1

#Creation all doors
def createDoors(l,i,h,s1):
  if l <= len(levelDoors)-1:
    if i < len(levelDoors[l]):
      params = parseLines(l,i,levelDoors)
      d = createDoor(params, 0, h, initStruct)
      hand = createHandle(params,initStruct)
      hand = STRUCT([T([3])([h]), hand])
      finalStruct = STRUCT([d, s1, hand])
      return createDoors(l,i+1,h,finalStruct)
    else:
      h = h + 80.0 
      return createDoors(l+1,0,h,s1)
  else:
    return s1

#Creation a window
def createWindow(params,h):
  q1 = MKPOL([[[params[0],params[1],0.0],[params[2],params[3],0.0]],[[1,2]],[1]])
  q1 = OFFSET([3.5, 3.5, 30.0])(q1)
  #q1 = STRUCT([T(3)(5.0), q1])
  q1 = TEXTURE([glassTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(q1)
  q1 = MATERIAL([0,1.36,2.55,0.5,  0,1,0,0.5, 0,0,1,0, 0,0,0,0.5, 100])(q1)
  if (params[0]-params[2]<1.0) & (params[0]-params[2]>-1.0):
    if params[1]<params[3]:
      q2 = MKPOL([[[params[0],params[1]-2.0,0.0],[params[2],params[3]+2.0,0.0]],[[1,2]],[1]])
      q2 = OFFSET([3.5, 3.5, 40.0])(q2)
    else:
      q2 = MKPOL([[[params[0],params[1]+2.0,0.0],[params[2],params[3]-2.0,0.0]],[[1,2]],[1]])
      q2 = OFFSET([3.5, 3.5, 40.0])(q2)
  if (params[1]-params[3]<1.0) & (params[1]-params[3]>-1.0):
    if params[0]<params[2]:
      q2 = MKPOL([[[params[0]-2.0,params[1],0.0],[params[2]+2.0,params[3],0.0]],[[1,2]],[1]])
      q2 = OFFSET([3.5, 3.5, 40.0])(q2)
    else:
      q2 = MKPOL([[[params[0]+2.0,params[1],0.0],[params[2]-2.0,params[3],0.0]],[[1,2]],[1]])
      q2 = OFFSET([3.5, 3.5, 40.0])(q2)
  q2 = STRUCT([T(3)(-3.5), q2])
  q2 = TEXTURE([pavTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(q2)
  q = DIFFERENCE([q2,q1])
  q = TEXTURE([pavTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(q)
  allWindow = STRUCT([q,q1])
  allWindow = STRUCT([T(3)(h), allWindow])
  return allWindow

#Creation all windows
def createWindows(l,i,h,s1):
  if l <= len(levelWindows)-1:
    if i < len(levelWindows[l]):
      params = parseLines(l,i,levelWindows)
      w = createWindow(params,h)
      finalStruct = STRUCT([w, s1])
      return createWindows(l,i+1,h,finalStruct)
    else:
      h = h + 80.0
      return createWindows(l+1,0,h,s1)
  else:
    return s1

#Creation the roof
def createRoof(i,s1):
  params = parseLines(0,i,levelBase)
  if i==0:
    truss = MKPOL([[[params[0],params[1],0.0],[params[2],params[3],0.0],[(params[2]+params[0])/2,(params[3]+params[1])/2,30.0]],[[1,2,3]],[1]])
    roof_frame = MKPOL([[[params[0],params[1]],[(params[2]+params[0])/2-30.0,(params[3]+params[1])/2]],[[1,2]],[1]])
    truss = OFFSET([-3.0, 0.0, 0.0])(truss)
  else:
    truss = MKPOL([[[params[0],params[1],0.0],[params[2],params[3],0.0],[(params[2]+params[0])/2,(params[3]+params[1])/2,30.0]],[[1,2,3]],[1]])
    roof_frame = MKPOL([[[params[0],params[1]],[(params[2]+params[0])/2-30.0,(params[3]+params[1])/2]],[[1,2]],[1]])
    truss = OFFSET([3.0, 0.0, 0.0])(truss)
  truss = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 2, 1])(truss)
  roof_height = levelBase[0][3]
  roof_height_split = roof_height.split(",")
  roof_height_number = np.array(roof_height_split, dtype=float)
  roof_height = roof_height_number[2] - roof_height_number[0]
  roof = STRUCT([T([1,3])([roof_height_number[0]-8,params[0]-1]),(ROTATE([1,3])(-PI/2)(PROD([roof_frame,Q(roof_height+10)])))])
  roof = OFFSET([3.0, 3.0, 3.0])(roof)
  roof = TEXTURE([roofTexture, TRUE, FALSE, 1, 1, 0, 2, 1])(roof)
  s2 = STRUCT([truss, s1])
  s2 = STRUCT([roof, s2])
  return s2

#Creation second floor
def createFloor2(i,base,s1):
  if i < len(levelStair[0]):
    params = parseLines(0,i,levelStair)
    a_pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
    a_off = OFFSET([4.0, 5.5, 2.0])(a_pol)
    s2 = STRUCT([a_off, s1])
    return createFloor2(i+1,base,s2)
  else:
    s1 = SOLIDIFY(SKEL_2(s1))
    s1 = DIFF([base,s1])
    s1 = TEXTURE([pavTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(s1)
  return s1

#Creation stair
def createStair(tempLength,tempHeight,s1):
  params = parseLines(0,0,levelStair)
  params2 = parseLines(0,2,levelStair)
  height = 80.0
  height_step = 5.44
  steps=height/height_step
  steps=height/steps
  length_step = 13.0
  #length = steps*length_step
  length = (params2[3]-params2[0])
  build = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
  buildOffset = OFFSET([5.0, length_step, height_step])(build)
  traslation=STRUCT([T([1,2,3])([0.5,tempLength+length_step,tempHeight]),buildOffset])
  tempLength=tempLength + length_step/2
  tempHeight=tempHeight + height_step
  s1=STRUCT([traslation,s1])
  if tempHeight < height:
    return createStair(tempLength, tempHeight, s1)
  else:
    s1 = TEXTURE([pavTexture, TRUE, FALSE, 1, 1, 0, 1, 1])(s1)
    s1=STRUCT([traslation,s1])
  return s1

#Creation the house
def buildHouse():
  floor1Level = createFloor1(0,initStruct)
  floor2Level = createFloor2(0,floor1Level,initStruct)
  externalLevel = createExternalWalls(0,0,0.0,initStruct)
  internalLevel = createInternalWalls(0,0,0.0,initStruct)
  doorsLevel = createDoors(0,0,0.0,initStruct)
  windowsLevel = createWindows(0,0,30.0,initStruct)
  roofLevel1 = createRoof(0,initStruct)
  roofLevel2 = createRoof(2,initStruct)
  stairsLevel = createStair(0.0,0.0,initStruct)
  house=STRUCT([floor1Level,T(3)(3.0),externalLevel])
  house=STRUCT([house,T(3)(3.5),stairsLevel])
  house=STRUCT([house,T(3)(3.5),internalLevel])
  house=STRUCT([house,T(3)(83.0),floor2Level])
  house=STRUCT([house,T(3)(163.0),floor1Level])
  house=STRUCT([house,T(3)(3.0),doorsLevel])
  house=STRUCT([house,T(3)(3.0),windowsLevel])
  house=STRUCT([house,T(3)(163.0),roofLevel1])
  house=STRUCT([house,T(3)(163.0),roofLevel2])
  return house

def createMoreHouse(i,s1,d):
  if i < 1:
    h1=STRUCT([T([1,2,3])([d,0.0,0.0]),buildHouse()])
    s1= STRUCT([h1, s1])
    return createMoreHouse(i+1,s1,d+600.0)
  else:
    return s1