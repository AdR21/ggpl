#workshop_09

"""Reproduction of house roof given a non-regular polygon"""

from pyplasm import *

"""Texture"""
roofTexture = "texture/roof.png"
floorTexture = "texture/floor.jpg"

par = 0.2

"""x, y coordinates of the polygon no regular plan"""

x = [
  1.0,  #0
  3.0,  #1
  4.0,  #2
  5.0,  #3
  8.0,  #4
  10.0, #5
  14.0, #6
  16.0, #7
  19.0, #8
  20.0, #9
  21.0, #10
  23.0  #11
]

y = [
  1.0,  #0
  3.0,  #1
  4.0,  #2
  5.0,  #3
  7.0,  #4
  10.0, #5
  12.0  #6
]

z = [
  0.0,  #0
  2.0   #1
]

vertsStruct = [
  [x[2],y[0],z[0]], #1 ---> external
  [x[0],y[2],z[0]], #2
  [x[0],y[6],z[0]], #3
  [x[11],y[6],z[0]], #4
  [x[11],y[2],z[0]], #5
  [x[9],y[0],z[0]], #6
  [x[6],y[0],z[0]], #7
  [x[6],y[3],z[0]], #8
  [x[5],y[3],z[0]], #9
  [x[5],y[0],z[0]], #10
  [x[3],y[1],z[1]], #11 ---> internal
  [x[1],y[3],z[1]], #12
  [x[1],y[5],z[1]], #13
  [x[10],y[5],z[1]], #14
  [x[10],y[3],z[1]], #15
  [x[8],y[1],z[1]], #16
  [x[7],y[1],z[1]], #17
  [x[7],y[4],z[1]], #18
  [x[4],y[4],z[1]], #19
  [x[4],y[1],z[1]] #20
]

cellsStruct = [
  [1,2,12,11],
  [2,3,13,12],
  [3,4,14,13],
  [4,5,15,14],
  [5,6,16,15],
  [6,7,17,16],
  [7,8,18,17],
  [8,9,19,18],
  [9,10,20,19],
  [10,1,11,20]
 
]

cellsStructBorder = [
  [1,2],
  [2,3],
  [3,4],
  [4,5],
  [5,6],
  [6,7],
  [7,8],
  [8,9],
  [9,10],
  [10,1]
]

""" Creation of the cells with the coordinates of the polygon """
roof = MKPOL([vertsStruct,[1]])
roof = (OFFSET([par, par, par])(SKEL_2(roof)))


VIEW(roof)