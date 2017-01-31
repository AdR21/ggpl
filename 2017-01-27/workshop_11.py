""" workshop 11 """
from pyplasm import *
import numpy as np
import sys, os

sys.path.append("house")
import house

sys.setrecursionlimit(1500)

grassTexture = "texture/grass.jpg"
asphaltTexture = "texture/asphalt.jpg"
pavTexture = "texture/pav4.jpg"

zero = CUBOID([.0,.0,.0])
initStruct = STRUCT([zero])
level_height = [30.0,30.0,20.0,30.0,30.0,20.0]
heights = [60.0,20.0,3.5,60.0,20.0]

def countFileDirectory(path):
  i = 0
  for name in os.listdir(path):
      if not name.startswith("."):
        i = i + 1
  return i

#Reads the svg files
def readSvg(l,reading_level,path):
  file = open("components/"+path+"/lines/level-"+str(l)+".lines","r")
  data = file.read()
  n = countFileDirectory("components/"+path+"/lines/")
  file.close()
  d = data.splitlines()
  reading_level = reading_level + [d]
  if l!=n-1:
    return readSvg(l+1,reading_level,path)
  else:
    return reading_level

levelBase = readSvg(0,[],"base")
levelStreet = readSvg(0,[],"strade")
levelHouse = readSvg(0,[],"case")
levelCurve = readSvg(0,[],"curve")

def parseLines(l,i, params):
  string_line = params[l][i]
  split_line = string_line.split(",")
  array_line = np.array(split_line, dtype=float)
  return array_line

#Creates the base of suburban neighborhood
def createGarden(i,s1):
  if i < len(levelBase[0]):
    params = parseLines(0,i,levelBase)
    a_pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
    a_off = OFFSET([4.0, 5.5, 5.0])(a_pol)
    s2 = STRUCT([a_off, s1])
    return createGarden(i+1,s2)
  else:
    s1 = SOLIDIFY(SKEL_2(s1))
    s1 = TEXTURE([grassTexture, TRUE, FALSE, 1, 1, 0, 10, 1])(s1)
    return s1

#Creates the roads curves
def createCurves(i,s1):
  if i < len(levelCurve[0]):
    curveExt1 = parseLines(0,i,levelCurve)
    curveExt2 = parseLines(0,i+1,levelCurve)
    curveInt1 = parseLines(1,i,levelCurve)
    curveInt2 = parseLines(1,i+1,levelCurve)
    ce = BEZIER(S1)([[curveExt1[2],curveExt1[3]],[curveExt1[0],curveExt1[1]],[curveExt2[0],curveExt2[1]]])
    ci = BEZIER(S1)([[curveInt1[2],curveInt1[3]],[curveInt1[0],curveInt1[1]],[curveInt2[0],curveInt2[1]]])
    c = MAP(BEZIER(S2)([ce,ci]))(PROD([INTERVALS(1)(10),INTERVALS(1)(10)]))
    c = OFFSET([0.0, 0.0, 3.0])(c)
    s1 = STRUCT([s1,c])
    return createCurves(i+2,s1)
  else:
    return s1

#Creates the roads 
def createRoads(l,i,s1):
  if l <= len(levelStreet)-1:
    if i < len(levelStreet[l]):
      params = parseLines(l,i,levelStreet)
      a_pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
      a_off = OFFSET([0.0, 0.0, 0.0])(a_pol)
      s2 = STRUCT([a_off, s1])
      return createRoads(l,i+1,s2)
    else:
      s1 = SOLIDIFY(SKEL_2(s1))
      s1 = STRUCT([T(3)(5.0),s1])
      s1 = TEXTURE([asphaltTexture, TRUE, FALSE, 1, 1, 0, 10, 10])(s1)
      return createRoads(l+1,0,s1)
  else:
    return s1   
      #curve = createCurves(0,0,initStruct)
      #s1 = SOLIDIFY(s1)
      #curve = SOLIDIFY(curve)
      #s1 = UNION([s1,curve])
      #s1 = STRUCT([s1,curve])
      #s1 = STRUCT([T(3)(5.0),s1])
      #s1 = TEXTURE([asphaltTexture, TRUE, FALSE, 1, 1, 0, 1, 10])(s1)
      #return s1
"""
def createRoads(i,s1):
  if i < len(levelStreet[0]):
    params = parseLines(0,i,levelStreet)
    a_pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
    a_off = OFFSET([0.0, 0.0, 3.0])(a_pol)
    s2 = STRUCT([a_off, s1])
    return createRoads(i+1,s2)
  else:
    curve = createCurves(0,initStruct)
    s1 = SOLIDIFY(s1)
    s1 = STRUCT([s1,curve])
    s1 = STRUCT([T(3)(5.0),s1])
    s1 = TEXTURE([asphaltTexture, TRUE, FALSE, 1, 1, 0, 16, 16])(s1)
    return s1
"""
#Creates the houses bases
def createHouseBase(i,s1):
  if i < len(levelHouse[0]):
    params = parseLines(0,i,levelHouse)
    a_pol = POLYLINE([[params[0],params[1]],[params[2],params[3]]])
    a_off = OFFSET([0.0, 0.0, 3.0])(a_pol)
    s1 = STRUCT([a_off, s1])
    return createHouseBase(i+1,s1)
  else:
    s1 = STRUCT([T(2)(3.0),s1])
    s1 = SOLIDIFY(SKEL_2(s1))
    s1 = TEXTURE([pavTexture, TRUE, FALSE, 1, 1, 0, 1, 10])(s1)
  return s1

def createHouseBase2(i,s1):
  if i < len(levelHouse[0]):
    params = parseLines(0,i,levelHouse)
    h2 = house.createMoreHouse(0,initStruct,0.0)
    h2 = STRUCT([T([1,2,3])([params[0]-180.00,params[1]-220.0,2.0]),h2])
    s1 = STRUCT([h2, s1])
    return createHouseBase2(i+4,s1)
  else:
    return s1

#Creates and places the houses 
def createHouses():
  garden_level = createGarden(0,initStruct)
  street_level = createRoads(0,0,initStruct)
  #street_level = createRoads(0,initStruct)
  house_level = createHouseBase(0,initStruct)
  house_level2 = createHouseBase2(3,initStruct)
  house=STRUCT([initStruct,T(3)(0.0),garden_level])
  house=STRUCT([house,T(3)(2.0),street_level])
  house=STRUCT([house,T(3)(2.0),house_level])
  house=STRUCT([house,T(3)(2.0),house_level2])
  return house

#Creates the total suburban neighborhood
def createSuburbanNeighborhood(i,s1,d):
  if i < 1:
    h = createHouses()
    h1=STRUCT([T(1)(d),h])
    h2=STRUCT([T(1)(d+1520),h])
    h3=STRUCT([T(2)(d+1910),h])
    h4=STRUCT([T([1,+2])([d+1520,d+1910]),h])
    s1= STRUCT([h1,h2,h3,h4,s1])
    return createSuburbanNeighborhood(i+1,s1,d+2000.0)
  else:
    VIEW(s1)

createSuburbanNeighborhood(0,initStruct,0.0)
