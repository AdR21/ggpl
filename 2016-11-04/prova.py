""" WORKSHOP 04 """
from pyplasm import *

verts1 = [[9,2,2],[13,2,7],[17,2,2],[17,7,2],[23,7,2],[23,12,7],[23,17,2],[3,17,2],[3,12,7],[3,7,2],[9,7,2],[13,12,7],[23,12,2],[3,12,2],[13,12,2],[13,17,2],[13,2,2]]
cells1 = [[8,7,9,6],[9,10,11,12],[12,4,5,6],[12,11,1,2],[12,2,3,4],[10,8],[7,5],[14,9],[13,6],[1,3],[12,15],[12,16],[13,14],[2,17]]

verts_panel1 = [[3,12.5,7.5],[3,17.5,2.5],[23.25,17.5,2.5],[23.25,12.5,7.5]]
cells_panel1 = [[1,2,3,4]]
verts_panel2 = [[3,5.5,2.5],[3,12.5,7.5],[3,12.5,7.5],[3,5.5,2.5]]
cells_panel2 = [[1,2,3,4]]

verts2 = verts_panel1 + verts_panel2
cells2 = cells_panel1 + cells_panel2

struct_roof = MKPOL([verts1, cells1,[1]])
panel_roof = MKPOL([verts_panel2, cells_panel2,[1]])

struct_roof = OFFSET([0.5, 0.5, 0.5])(SKEL_1(struct_roof))

panel_roof = COLOR(RED)(OFFSET([0.25, 0.25, 0.25])(SKEL_2(panel_roof)))

roof = STRUCT([struct_roof, panel_roof])

VIEW(roof)

 