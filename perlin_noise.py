## Bob Hooper, 2024 - https://robhooper.net

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
import random

from lib.myamulet import AmuletWrapper
from lib.noise import generate_perlin_noise

def main(world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict):

    myamulet = AmuletWrapper(world, dimension, selection, options)

    ## Init Matrix
    arrshape = (myamulet.width, myamulet.depth)
    arr = np.zeros(arrshape, dtype=int)

    #def generate_perlin_noise(width, depth, height, grid_size = 10, seed = 10):

    seed = options['Random Seed']
    if options['Random Seed'] == -1:
        seed = int(random.random() * 10 ** 9) # seed has to be less than (2 ** 32 - 1)

    arr = np.add(
                arr,
                # Sorry!
                np.rot90(generate_perlin_noise(
                     width = myamulet.width, 
                     depth = myamulet.depth, 
                     height = myamulet.height, 
                     grid_size = options['Frequency'], 
                     seed = seed
                     ), 1)
            )

    #print(arr)

    myamulet.build(arr)

    print("Complete!")

def options():
    return AmuletWrapper.options() | {
        "Frequency": ["int", 5], # This effects how "smooth" the results are
        "Random Seed": ["int", -1] # -1 for a random
    }


export = {
    "name": "Perlin Noise",
    "operation": main,
    "options": options()
}
