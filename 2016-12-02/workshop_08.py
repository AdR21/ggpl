#workshop_08

"""Reproduction of house plan"""

from pyplasm import *
import numpy as np

"""Texture"""
bricksTexture = "texture/bricks.jpg"
wallTexture = "texture/wall.jpg"

"""Structure initial"""
init = CUBOID([.0,.0,.0])
initStruct = STRUCT([init])

"""Function that reads .lines file to extract the points"""
def readFile(l):
	file = open("lines/level_"+str(l)+".lines","r")
	data = file.read()
	file.close()
	return data.splitlines()

"""Contour map"""
lev1 = readFile(1)
"""Map with doors"""
lev2 = readFile(2)
"""Map with the windows and doors"""
lev3 = readFile(3)
"""Map with door jambs"""
lev4 = readFile(4)

"""Array with levels"""
level = [lev1,lev2,lev3,lev4,lev1]

"""Height of each floor """
levelHeight = [0.0,30.0,30.0,20.0,0.0]		

"""Function that reads the points and builds all levels of the plant """
def housePlan(l,i,h,s1):
	#Cycle levels
	if l <= len(level)-1:
		#Cycle the points of each of a floor wall
		if i < len(level[l])-1:
			#Take the point of a wall
			wall = level[l][i]
			#It inserts them into an array by splitting the comma
			wallSplit = wall.split(",")
			#Transform each element from string to float
			wallNumber = np.array(wallSplit, dtype=float)
			#creates the wall (1D) joining the points extracted from the lines in his position
			#wallNumber[0] --> x1
			#wallNumber[1] --> y1
			#wallNumber[2] --> x2
			#wallNumber[3] --> y2
			#[wallNumber[0],wallNumber[1]] --> x1,y1
			#[wallNumber[0],wallNumber[3]] --> x1,y2
			#[wallNumber[2],wallNumber[1]] --> x2,y1
			#[wallNumber[2],wallNumber[3]] --> x2,y1
			wallPol = MKPOL([[[wallNumber[0],wallNumber[1],0.0],[wallNumber[0],wallNumber[3],0.0],[wallNumber[2],wallNumber[1],0.0],[wallNumber[2],wallNumber[3],0.0]],[[1,2,3,4]],[1]])
			#It gives the wall the height referred to the plan that I am creating
			wallOff = OFFSET([1.5, 1.5, levelHeight[l]])(wallPol)
			#Texture to the wall
			wallText = TEXTURE([wallTexture, TRUE, FALSE, 1, 1, 0, 6, 1])(wallOff)
			#Translates the plan to make it place over the previous plan by h
			wallTranslate = STRUCT([T(3)(h), wallText])
			s2 = STRUCT([wallTranslate, s1])
			#Re-executes the function to create a new wall
			return housePlan(l,i+1,h,s2)
		else:
			#Calculates the overall height to position the new plan
			h = h + levelHeight[l]
			#Re-executes the function to create a new plan
			return housePlan(l+1,0,h,s1)
	else:
		VIEW(s1)

housePlan(0,0,0.0,initStruct)
