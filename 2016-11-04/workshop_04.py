#workshop_04

"""Reproduction of a roof taken like example """

from pyplasm import *

dim = 0.2

x = [1.0,7.0,11.0,15.0,21.0]
y = [2.0,7.0,12.0,17.0]
z = [0.0, 5.0]

"""Verts and Cells on the Cartesian plane"""
verts = [[x[1],y[0],z[0]],[x[2],y[0],z[1]],[x[3],y[0],z[0]],[x[3],y[1],z[0]],[x[4],y[1],z[0]],[x[4],y[2],z[1]],[x[4],y[3],z[0]],[x[0],y[3],z[0]],[x[0],y[2],z[1]],[x[0],y[1],z[0]],[x[1],y[1],z[0]],[x[2],y[2],z[1]],[x[4],y[2],z[0]],[x[0],y[2],z[0]],[x[2],y[2],z[0]],[x[2],y[3],z[0]],[x[2],y[0],z[0]]]
cells = [[8,7,9,6],[9,10,11,12],[12,4,5,6],[12,11,1,2],[12,2,3,4],[10,8],[7,5],[14,9],[13,6],[1,3],[12,15],[12,16],[13,14],[2,17]]

"""Simple structure of the roof model"""
baseRoof = MKPOL([verts, cells,[1]])

"""Roof frame'"""
roofFrame = COLOR(BLACK)(OFFSET([dim, dim, dim])(SKEL_1(baseRoof)))

"""Cells creation"""
newBaseRoof = STRUCT([T([3])([dim*2])(baseRoof)])

"""New points to adapt the coverage"""
pts = UKPOL(newBaseRoof)
newVerts = pts[0]
newCells = pts[1]

"""Coverage of the frame"""
newVerts = [[x[0],y[2],z[1]+dim*2],[x[4],y[3]+dim,z[0]+dim],[x[4],y[2],z[1]+dim*2],[x[0],y[3]+dim,z[0]+dim],[x[0],y[1]-dim,z[0]+dim],[x[2],y[2],z[1]+dim*2],[x[1]-dim,y[1]-dim,z[0]+dim],[x[0],y[2],z[1]+dim*2],[x[4],y[1]-dim,z[0]+dim],[x[2],y[2],z[1]+dim*2],[x[3]+dim,y[1]-dim,z[0]+dim],[x[4],y[2],z[1]+dim*2],[x[2],y[0],z[1]+dim*2],[x[1]-dim,y[1]-dim,z[0]+dim],[x[1]-dim,y[0],z[0]+dim],[x[2],y[2],z[1]+dim*2],[x[2],y[2],z[1]+dim*2],[x[3]+dim,y[0],z[0]+dim],[x[3]+dim,y[1]-dim,z[0]+dim],[x[2],y[0],z[1]+dim*2],[x[0],y[3]+dim,z[0]+dim],[x[0],y[1]-dim,z[0]+dim],[x[4],y[3]+dim,z[0]+dim],[x[4],y[1]-dim,z[0]+dim],[x[0],y[2],z[1]+dim*2],[x[0],y[2],z[0]+dim],[x[4],y[2],z[1]+dim*2],[x[4],y[2],z[0]+dim],[x[3]+dim,y[0],z[0]+dim],[x[1]-dim,y[0],z[0]+dim],[x[2],y[2],z[1]+dim*2],[x[2],y[2],z[0]+dim],[x[2],y[3]+dim,z[0]+dim],[x[2],y[2],z[1]+dim*2],[x[4],y[2],z[0]+dim],[x[0],y[2],z[0]+dim],[x[2],y[0],z[1]+dim*2],[x[2],y[0],z[0]+dim]]

"""Coverage adapted to the frame"""
covRoof = MKPOL([newVerts, newCells,[1]])
covRoof = COLOR(YELLOW)(OFFSET([dim, dim, dim])(SKEL_2(covRoof)))

"""Complete roof"""
finalRoof = STRUCT([roofFrame, covRoof])

VIEW(finalRoof)