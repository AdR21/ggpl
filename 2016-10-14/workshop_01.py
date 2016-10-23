# workshop_01

"""Creazione di un telaio con pilastri e travi"""

from larlib import *

pillarsLength = [3.0, 5.0, 5.0]
beamsLength = [10.0, 5.0]
pillarWidth = 0.5
beamWidth  = pillarWidth/2.0

pillars = CUBOID([0,0,0])
arch = STRUCT([pillars])

def chassis(pillarsLengthAll, beamsLengthAll, x, k, archTotal):
	pillars1 = (CUBOID([pillarWidth,pillarWidth,pillarsLength[k]]))
	pillars1All = STRUCT([T(2)(beamsLengthAll),T(3)(pillarsLengthAll), pillars1])
	beams1 = (CUBOID([beamWidth,beamsLength[x],beamWidth]))
	beams1All = STRUCT([T([1,2,3])([beamWidth/2.0, (3.0*pillarWidth/4.0)+beamsLengthAll,pillarsLengthAll+pillarsLength[k]]), beams1])
	beamsLengthAll=beamsLengthAll+beamsLength[x]+(pillarWidth/2.0)
	
	if x == len(beamsLength) - 1:
		pillars1NextTotal = STRUCT([T(2)(beamsLengthAll),T(3)(pillarsLengthAll), pillars1])
		pillarsLengthAll = pillarsLengthAll + pillarsLength[k] + beamWidth
		archTotal = STRUCT([archTotal,pillars1All,beams1All,pillars1NextTotal])
		if k != len(pillarsLength) - 1:
			k=k+1
			return chassis(pillarsLengthAll, 0, 0, k, archTotal)
		else:
			VIEW(archTotal)
	else:
		x=x+1
		archTotal = STRUCT([archTotal,pillars1All,beams1All])
		return chassis(pillarsLengthAll, beamsLengthAll, x, k, archTotal)

chassis(0, 0, 0, 0, arch)