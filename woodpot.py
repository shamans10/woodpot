#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import division
import os
import sys
import re
import math

# Assumes SolidPython is in site-packages or elsewhere in sys.path
from solid import *
from solid.utils import *

SEGMENTS = 75

def calcDimensions(radius=25, height=35, wall_thickness=7, sides=6, layers=5, roundEdges=False, leveledTop=True, overlap=1.25):
    blockLength = 2*radius*tan(math.pi/sides)
    blockWidth = wall_thickness
    blockHeight = height/layers/2
    blockAngle = 180*(sides-2)/sides

    if sides == 3: # calculate vertex to vertex distance if it's a triangle
        VertexToVertex = radius*2

    elif sides == 4: # if it's a square
        VertexToVertex = math.sqrt(radius**2 + radius**2)

    else: # if it's any other type of normal polygon
        VertexToVertex = math.sqrt(radius**2 + (blockLength/2+(blockWidth/2*overlap))**2)

    block = []
    # pot bottom
    floorThickness = wall_thickness*1.4
    planks = math.ceil(radius*2.05/floorThickness)
    for l in range(2):
        for p in range(planks):
            if (p%2 == 0):
                newSide = rotate(a=blockAngle-90+l*90)(translate([0,floorThickness*p*(1-(1/planks))-radius+floorThickness/2,l*blockHeight])(cube([radius*3+(floorThickness*overlap),floorThickness,blockHeight], center = True)))
                block = union()(block,newSide)

    #remove excess floor planks
    excess = []
    excessOuter = (cube([radius*4, VertexToVertex*4, height*2], center=True))
    for e in range(math.ceil(sides)):
        excessInner = rotate(blockAngle*e-90)(cube([radius*2+blockWidth*overlap, VertexToVertex*2, height*3], center=True))
        excess = excessOuter - excessInner
        block = block - excess
        #excess = excessInner+excess

    for l in range(layers): # Sides of the pot
        for s in range(sides): #Generate layers
            if (l == layers-1) and leveledTop == True: #if it's the top layer and leveledTop is true
                if (s%2 == 0): # if side iter is even
                    newSide = rotate(a=blockAngle*s)(translate([0,radius,blockHeight*l*2])(cube([blockLength+(blockWidth*overlap),blockWidth,blockHeight], center = True)))
                    block = union()(block,newSide)

                elif (s%2 > 0): # else side iter is odd
                    newSide = rotate(a=blockAngle*s)(translate([0,radius*-1,blockHeight*l*2])(cube([blockLength+(blockWidth*overlap),blockWidth,blockHeight], center = True)))
                    block = union()(block,newSide)

            elif (s%2 == 0): # if side iter is even
                newSide = rotate(a=blockAngle*s)(translate([0,radius,blockHeight*l*2])(cube([blockLength+(blockWidth*overlap),blockWidth,blockHeight], center = True)))
                block = union()(block,newSide)
            elif (s%2 > 0): # else side iter is odd
                newSide = rotate(a=blockAngle*s)(translate([0,radius*-1,blockHeight*l*2+blockHeight])(cube([blockLength+(blockWidth*overlap),blockWidth,blockHeight], center = True)))
                block = union()(block,newSide)

    if roundEdges == True:
        innerCyl = cylinder(r=VertexToVertex, h=height*5, center= True)
        outerCyl = cylinder(r=VertexToVertex*2, h=height*4, center= True)
        outerCyl = outerCyl - innerCyl
        block = block - outerCyl
    return block

woodpot = calcDimensions(radius=20,height=30,wall_thickness=5,sides=6,layers=5,roundEdges=True, leveledTop=False,overlap=1.0)
if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join(out_dir, 'woodpot.scad')

    print("%(__file__)s: SCAD file written to: \n%(file_out)s" % vars())

    scad_render_to_file(woodpot, file_out, file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)
