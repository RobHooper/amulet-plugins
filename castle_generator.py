## Bob Hooper, 2024 - https://robhooper.net
## Authors note:
##      Sorry for the state of this code! This was a learning project and may be cleaned up later.

from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

from amulet.api.block import Block  # For working with Blocks
from amulet.api.block_entity import BlockEntity
from amulet_nbt import *  # For working with block properties

import math
import random
import json

import numpy as np


def myFunction(world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict):
    block_platform = "bedrock"  # the platform the blocks below are defined in
    block_version = (1, 17, 0)  # the version the blocks below are defined in
    block_entity = None
    block = Block("minecraft", "stone", {})

    # Init useful vars
    box = selection[0]

    minx = box.min_x
    miny = box.min_y
    minz = box.min_z
    maxx = box.max_x
    maxy = box.max_y
    maxz = box.max_z

    width = maxx - minx
    depth = maxz - minz
    height = maxy - miny

    # We can ensure a clean wall by overwriting the user selection
    if options['Fix Dimples'] == True:
        if width % 2 == 0:
            maxx += 1
            width +=1
        if depth % 2 == 0:
            maxz += 1
            depth +=1

    wallheight = height - 2
    
    if options["Towers"] == True:
        walloffset = int(options["Tower Size"] / 3)
    else:
        walloffset = 0

    ## Init Matrix
    # Mainly using Matrix to practice and learn!
    # Using np because it has better performance and it is what people use (apparently!)
    arrshape = (width, depth)
    arr = np.zeros(arrshape, dtype=int)

    ## Draw what I want.

    # Create walls
    for wallsize in range(options["Wall Width"]):
        arr[wallsize + walloffset] = [wallheight]
        arr[:,wallsize + walloffset] = [wallheight]
        arr[-wallsize -1 - walloffset] = [wallheight]
        arr[:,-wallsize -1 - walloffset] = [wallheight]

    # Towers
    if options["Towers"] == True:
        for towersizex in range(options["Tower Size"]):
            for towersizez in range(options["Tower Size"]):
                arr[towersizex][towersizez] = height
                arr[towersizex, -towersizez -1] = height
                arr[-towersizex -1, towersizez] = height
                arr[-towersizex -1, -towersizez -1] = height

    # Dimple

    if options['Dimples'] == True:
        ## Solution 1, Doubles up on block removal:
        #for row in range(1, width, 2):
        #    arr[row] -= 1
        #
        #for row in range(1, depth, 2):
        #    arr[:,row] -= 1

        ## Solution 2, only works on specific size castles:
        dimples = np.array([0,1])
        dimples = np.resize(dimples, arrshape)

        ## Solution 3:
        #dimples = np.zeros(arrshape, dtype=int)
        #for row in range(1, width, 2):
        #    dimples[row] = 1
        #
        #for row in range(1, depth, 2):
        #    dimples[:,row] = 1

        # print(dimples) # Debug
        arr = np.subtract(arr, dimples)

    ## Actually place blocks
    for x in range(width):
        blx = x + minx
        for z in range(depth):
            blz = z + minz
            for y in range(height):
                bly = y + miny
                #print(f"debug: {x}, {y}, {z}")

                if arr[x][z] >= 1:
                    block = Block("minecraft", "stone", {})
                    arr[x][z] -= 1
                else:
                    # Skip if options.flatten is True
                    if options['Flatten'] == True:
                        block = Block("minecraft", "air", {})
                    else:
                        continue

                world.set_version_block(
                        blx,
                        bly,
                        blz,
                        dimension,
                        (block_platform, block_version),
                        block,
                        block_entity
                )

    #print("Complete!")


## https://github.com/Amulet-Team/Amulet-Map-Editor/blob/master/amulet_map_editor/programs/edit/plugins/operations/examples/3_fixed_function_pipeline.py
operation_options = {  # options is a dictionary where the key is the description shown to the user and the value describes how to build the UI
    "Flatten": ["bool" , True],  # Delete blocks in selected area
    "Towers": ["bool" , True], # Generate towers
    "Tower Size": [
        "int",
        3,
    ],
    "Wall Width": [
        "int",
        1,
    ],
    "Dimples": ["bool", True],
    "Fix Dimples": ["bool", False], # Overwrite user selection to ensure clean towers
}

export = {
    "name": "Castle Builder",
    "operation": myFunction,
    "options": operation_options    
}
