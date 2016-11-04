""" WORKSHOP 04 """
from pyplasm import *

verts = [[7,2,0],[11,2,5],[15,2,0],[15,7,0],[21,7,0],[21,12,5],[21,17,0],[1,17,0],[1,12,5],[1,7,0],[7,7,0],[11,12,5],[21,12,0],[1,12,0],[11,12,0],[11,17,0],[11,2,0]]
cells = [[8,7,9,6],[9,10,11,12],[12,4,5,6],[12,11,1,2],[12,2,3,4],[10,8],[7,5],[14,9],[13,6],[1,3],[12,15],[12,16],[13,14],[2,17]]

pol = MKPOL([verts, cells,[1]])

struct_roof = OFFSET([0.5, 0.5, 0.5])(SKEL_1(pol))

panel_roof = COLOR(RED)(OFFSET([0.5, 0.5, 0.5])(SKEL_2(pol)))

coords = UKPOL(panel_roof)

pol2 = COLOR(RED)(MKPOL(coords))
pol2 = (SKEL_1(pol2))

roof = STRUCT([struct_roof, panel_roof])
VIEW(roof)

 