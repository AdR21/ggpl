#workshop_03

"""Creazione di una scala, composta da una pedana, un muro portante e un pavimento"""

from pyplasm import *

wall=0.5 #spessore del muro di sostegno
floor=0.25 #pavimento sottostante la scala
landing=1.0 #pedana antistante la scala
height=3.0 #altezza del muro
length=6.0 #lunghezza della scalinata (profondita' del muro)
steps=10.0 #numero di gradini
sx= 1.5 #larghezza gradino (parametro formale X)
sy=length/steps #lunghezza gradino (parametro formale Y)
dz=height/steps #altezza gradino (parametro formale Z)

"""inizializzazione struttura vuota in cui verra' costruita la scala"""
elem=CUBOID([0,0,0])
struct=STRUCT([elem])

"""
createStaircase: funzione che ricorsivamente costruisce un gradino alla volta
Se si arriva a una profondita' compresa tra i 2/5 e i 4/5 della profondita' totale, si costruisce un pianerottolo lungo 3 volte un gradino normale
nella costruzione del muro di sostegno.
Della pedana sottostante si tiene conto della lunghezza dei gradini, della loro altezza e della lunghezza del pianerottolo
"""
def createStaircase(x,y,z,tempWidth,tempHeight,tempStruct):
	if(2.0*length/5.0<tempWidth<4.0*length/5.0):
		step=COLOR(WHITE)(CUBOID([x, y*3, z]))
		traslation=STRUCT([T([1,2,3])([wall/3,tempWidth,tempHeight]),step])
		tempWidth=tempWidth + y*3.0
		tempHeight=tempHeight + z	
	else:
		step=COLOR(WHITE)(CUBOID([x, y, z]))
		traslation=STRUCT([T([1,2,3])([wall/3,tempWidth,tempHeight]),step])
		tempWidth=tempWidth + y
		tempHeight=tempHeight + z
	stair=STRUCT([traslation,tempStruct])
	if tempWidth < length+y:
		createStaircase(x, y, z, tempWidth, tempHeight, stair)
	else:
		w=COLOR(BROWN)(CUBOID([wall,length+landing+y*2,height+floor]))
		f=COLOR(BROWN)(CUBOID([sx+wall/2,length+landing+y*2,floor]))
		stair=STRUCT([T([2,3])([landing,floor]),stair])		
		finalStaircase=STRUCT([w,f,stair])

		VIEW(finalStaircase)

"""
ggpl_staircase_with_central_landing: funzione che prende in input i 3 parametri formali relativi alle 3 dimensioni
"""
def ggpl_staircase_with_central_landing(x1,y1,z1):
	createStaircase(x1,y1,z1,0,0,struct)

ggpl_staircase_with_central_landing(sx,sy,dz)