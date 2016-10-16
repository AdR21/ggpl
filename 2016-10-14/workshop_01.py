# workshop_01
from larlib import *


beams_weight = [3.0, 6.0, 4.0, 3.0]
pilars_height = [5.0, 4.0, 3.0]
pilar_space_tot=0

p0 = CUBOID([0,0,0])
arc_all = STRUCT([p0])
pilar_height_tot=0

for y,p in enumerate(pilars_height):
	p1 = CUBOID([1,1,p])
	beam_weight_tot=0
	if y!=0:
			p1_t = STRUCT([T(3)(pilar_height_tot+1), p1])
			arc_all = STRUCT([arc_all,p1_t])
	else:
			arc_all = STRUCT([arc_all,p1])
	
	pilar_height_tot= pilar_height_tot + p

	for i,b in enumerate(beams_weight):
		t1_next = CUBOID([1,b,1])
		if i==0:
			if(y==0):
				t1_next_t = STRUCT([T(2)(0.5),T(3)(pilar_height_tot), t1_next])
			else:
				t1_next_t = STRUCT([T(2)(0.5),T(3)(pilar_height_tot+1), t1_next])
		else:
			if(y==0):
				t1_next_t = STRUCT([T(2)(beam_weight_tot+0.5),T(3)(pilar_height_tot), t1_next])
			else:
				t1_next_t = STRUCT([T(2)(beam_weight_tot+0.5),T(3)(pilar_height_tot+1), t1_next])
		beam_weight_tot = beam_weight_tot + b
		p1_next = CUBOID([1,1,p])
		if(y==0):
			p1_next_t = STRUCT([T(2)(beam_weight_tot), p1_next])
		else:
			p1_next_t = STRUCT([T(2)(beam_weight_tot),T(3)(pilar_height_tot-p+1), p1_next])
		arc = STRUCT([p1_next_t,t1_next_t])
		arc_all = STRUCT([arc_all,arc])


VIEW(arc_all)