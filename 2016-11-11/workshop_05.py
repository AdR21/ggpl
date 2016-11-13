#workshop_05

"""Reproduction of a school forniture """

from pyplasm import *

"""Function to create colors from RGB"""
def intRGBColor(values):
    return Color4f([values[0]/255.0,values[1]/255.0,values[2]/255.0,1.0])

"""Function to create a chair"""
def ggpl_chair(dx, dy, dz):
    depthLeg = 0.05 * dx
    distanceLeg = 0.03 * dx
    depthChair = 0.01 * dz
    heightLeg = 0.45 * dz

    def makeLeg(dx, dy, dz):
        def baseChair(dx, dy, dz):
            first = PROD([PROD([QUOTE([-distanceLeg, dx - distanceLeg * 2]),QUOTE([-distanceLeg, dy - distanceLeg * 2])]),QUOTE([- dz + depthLeg, depthLeg])])
            second = PROD([PROD([QUOTE([-distanceLeg - depthLeg, dx - distanceLeg * 2 - depthLeg * 2]),QUOTE([-distanceLeg - depthLeg, dy - distanceLeg * 2 - depthLeg * 2])]),QUOTE([- dz + depthLeg, depthLeg])])

            return DIFF([first, second])

        x = QUOTE([-distanceLeg, depthLeg, - (dx - distanceLeg * 2 - depthLeg * 2), depthLeg])
        y = QUOTE([-distanceLeg, depthLeg, - (dy - distanceLeg * 2 - depthLeg * 2), depthLeg])
        z = QUOTE([dz - depthLeg])

        return STRUCT([PROD([PROD([x, y]),z]),baseChair(dx, dy, dz)])

    return STRUCT([
        COLOR(BLACK)(makeLeg(dx, dy, heightLeg)),T(3)(heightLeg),
        COLOR(intRGBColor([139,232,184]))(CUBOID([dx, dy, depthChair])),T(2)(dy - depthChair),
        COLOR(intRGBColor([139,232,184]))(CUBOID([dx, depthChair, dz - depthChair - heightLeg]))
    ])

VIEW(ggpl_chair(0.40,0.40,0.80))

"""Function to create a school desk"""
def ggpl_schoolDesk(dx, dy, dz):
    depthLeg = 0.05 * dx
    distanceLeg = 0.03 * dx
    depthTable = 0.05 * dz

    def makeLeg(dx, dy, dz):
        def baseTable(dx, dy, dz):
            first = PROD([PROD([QUOTE([-distanceLeg, dx - distanceLeg * 2]),QUOTE([-distanceLeg, dy - distanceLeg * 2])]),QUOTE([- dz + depthLeg, depthLeg])])
            second = PROD([PROD([QUOTE([-distanceLeg - depthLeg, dx - distanceLeg * 2 - depthLeg * 2]),QUOTE([-distanceLeg - depthLeg, dy - distanceLeg * 2 - depthLeg * 2])]),QUOTE([- dz + depthLeg, depthLeg])])

            return DIFF([first, second])

        x = QUOTE([-distanceLeg, depthLeg, - (dx - distanceLeg * 2 - depthLeg * 2), depthLeg])
        y = QUOTE([-distanceLeg, depthLeg, - (dy - distanceLeg * 2 - depthLeg * 2), depthLeg])
        z = QUOTE([dz - depthLeg])

        return STRUCT([PROD([PROD([x, y]),z]),baseTable(dx, dy, dz)])

    return (STRUCT([
    	COLOR(BLACK)(makeLeg(dx, dy, dz - depthTable)),T(3)(dz - depthTable),
    	COLOR(intRGBColor([139,232,184]))(CUBOID([dx, dy, depthTable]))
    ]))

VIEW(ggpl_schoolDesk(0.60,1,0.80))

"""Function to create a blackboard"""
def ggpl_blackboard(dx,dy,dz):
    edge = 0.07
    panel = COLOR(BLACK)(CUBOID([dx-(2*edge),dy,dz-(2*edge)]))
    panel = STRUCT([T([1,3])([edge,edge]),panel])

    edgeHPC = CUBOID([dx,dy,dz])
    edgeHPC = COLOR(intRGBColor([192,192,192]))(DIFF([edgeHPC, panel]))
    
    blackboard = STRUCT([T(1)(dx),R([1,2])(PI),panel,edgeHPC,T([1,3])([(5*edge),(5*edge)]),S([1,3])])
    
    return STRUCT([blackboard])

VIEW(ggpl_blackboard(3.50,0.03,1.50))


