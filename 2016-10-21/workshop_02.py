# workshop_02

"""Creazione di una struttura composta da telai di pilastri e travi
"""

from larlib import *

import csv

"""pillarsLength: lunghezza pilastri 
	beamsLength: lunghezza travi 
	pillarWidth: larghezza pilastro
	beamWidth: larghezza trave
	planDist: distanza tra  piani
"""

pillarsLength = [0.5, 3.0, 3.0, 3.05]
beamsLength = [4.5, 4.5]
pillarWidth = 0.5
beamWidth  = pillarWidth/2.0
planDist = [4.5, 4.5, 4.5, 4.5]

with open('frame_data_441476./frame_data_441476.csv', 'rb') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)

"""Struttura vuota dove verra' costruito il telaio
"""

pillars = CUBOID([0,0,0])
arch = STRUCT([pillars])

"""Creazione struttura
"""

def ggpl_bone_structure(pillarsLengthAll, beamsLengthAll, planDistTot, x, z, y, archTotal):
	if  z < len(pillarsLength): 
		pillars1 = COLOR(BLUE)(CUBOID([pillarWidth,pillarWidth,pillarsLength[z]]))
		pillars1All = STRUCT([T(1)(planDistTot),T(2)(beamsLengthAll),T(3)(pillarsLengthAll), pillars1])
		beams1 = COLOR(GREEN)(CUBOID([beamWidth,beamsLength[y],beamWidth]))
		beams1All = STRUCT([T([1,2,3])([beamWidth/2.0+planDistTot, (3.0*pillarWidth/4.0)+beamsLengthAll, pillarsLengthAll+pillarsLength[z]]), beams1])
		
		if  x < len(planDist): 
			archTotal = STRUCT([archTotal,pillars1All,beams1All])
			t2 = COLOR(GREEN)(CUBOID([planDist[x],beamWidth,beamWidth]))
			t2_t = STRUCT([T([1,2,3])([beamWidth/2.0+planDistTot, (pillarWidth/4.0)+beamsLengthAll, pillarsLengthAll+pillarsLength[z]]), t2])
			beamsLengthAll=beamsLengthAll+beamsLength[y]+(pillarWidth/2.0)
			
			if y < len(beamsLength) - 1: 
				y=y+1
				archTotal = STRUCT([archTotal,t2_t])
				return ggpl_bone_structure(pillarsLengthAll, beamsLengthAll, planDistTot, x, z, y, archTotal)
			
			else:
				pillars1_next_t = STRUCT([T(1)(planDistTot),T(2)(beamsLengthAll),T(3)(pillarsLengthAll), pillars1])
				t2_next_t = STRUCT([T([1,2,3])([beamWidth/2.0+planDistTot, (pillarWidth/4.0)+beamsLengthAll,pillarsLengthAll+pillarsLength[z]]), t2])
				archTotal = STRUCT([archTotal,t2_t,pillars1_next_t,t2_next_t])
				planDistTot = planDistTot + planDist[x]
				x=x+1
				return ggpl_bone_structure(pillarsLengthAll, 0, planDistTot, x, z, 0, archTotal)
		
		else:
			pillarsLengthAll = pillarsLengthAll + pillarsLength[z] + beamWidth
			z=z+1
			return ggpl_bone_structure(pillarsLengthAll, 0, 0, 0, z, 0, archTotal)
	
	else:
		dist = 0
		for p in planDist:
			dist = dist + p
		return ggpl_bone_structure_1(dist, 0, 0, 0, 0, archTotal)

"""Telaio finale
"""

def ggpl_bone_structure_1(dist, pillarsLengthAll, beamsLengthAll, j, y, archTotal):
	pillars1 = COLOR(BLUE)(CUBOID([pillarWidth,pillarWidth,pillarsLength[y]]))
	pillars1All = STRUCT([T(1)(dist),T(2)(beamsLengthAll),T(3)(pillarsLengthAll), pillars1])
	beams1 = COLOR(GREEN)(CUBOID([beamWidth,beamsLength[j],beamWidth]))
	beams1All = STRUCT([T([1,2,3])([beamWidth/2.0+dist, (3.0*pillarWidth/4.0)+beamsLengthAll,pillarsLengthAll+pillarsLength[y]]), beams1])
	beamsLengthAll=beamsLengthAll+beamsLength[j]+(pillarWidth/2.0)
	if j == len(beamsLength) - 1:
		pillars1_next_t = STRUCT([T(1)(dist),T(2)(beamsLengthAll),T(3)(pillarsLengthAll), pillars1])
		pillarsLengthAll = pillarsLengthAll + pillarsLength[y] + beamWidth
		archTotal = STRUCT([archTotal,pillars1All,beams1All,pillars1_next_t])
		if y != len(pillarsLength) - 1:
			y=y+1
			return ggpl_bone_structure_1(dist, pillarsLengthAll, 0, 0, y, archTotal)
		else:
			VIEW(archTotal)
	else:
		j=j+1
		archTotal = STRUCT([archTotal,pillars1All,beams1All])
		return ggpl_bone_structure_1(dist, pillarsLengthAll, beamsLengthAll, j, y, archTotal)

ggpl_bone_structure(0, 0, 0, 0, 0, 0, arch)