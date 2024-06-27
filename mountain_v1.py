## Bob Hooper, 2024 - https://robhooper.net

from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

from amulet.api.block import Block  # For working with Blocks
from amulet.api.block_entity import BlockEntity
from amulet_nbt import *  # For working with block properties

import random

import numpy as np
import random

from lib.myamulet import AmuletWrapper
from lib.noise import generate_perlin_noise, center_grid
from lib.arrayhelper import ArrayHelper

def main(world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict):

    myamulet = AmuletWrapper(world, dimension, selection, options)

    myarray = ArrayHelper(depth = myamulet.depth, width = myamulet.width, height = myamulet.height)
    #print(myarray.arr)

    seed = options['Random Seed']
    if options['Random Seed'] == -1:
        ## UGH, Amulet limits int values to 30000000
        seed = int(random.random() * 10 ** 9) # seed has to be less than (2 ** 32 - 1)
        print(f"Seed: {seed}")

    def addNoise(arr, freq, amp = 1):
        arr.mergeArray( generate_perlin_noise(
            width = myamulet.width, 
            depth = myamulet.depth, 
            height = amp, 
            grid_size = freq, 
            seed = seed)
        )

    frequency = 2    

    # Attempt at a dynamic frequency range:
    #for iter in range(1, round((myamulet.width + myamulet.height) / 32) + 1):
    #    #print("Foo"+str(frequency)+str(iter))
    #    addNoise(myarray, frequency ** iter)

    addNoise(myarray, 2)
    addNoise(myarray, 4, 0.5)
    addNoise(myarray, 9, 0.3)
    addNoise(myarray, 18, 0.1)

    #print(myarray.arr)
    #print(center_grid(width = myamulet.width, depth = myamulet.depth))

    # Add ground height
    if options['Merge edges']:
        # Reduces the effect near edges (Needs work..)
        myarray.arr = np.multiply(myarray.arr, center_grid(depth = myamulet.depth, width = myamulet.width))

    # Normalise and fit selection height
    myarray.arr = np.multiply(myarray.normalised(), myamulet.height)

    # Add ground height
    if options['Flatten'] != True:
        myarray.arr = np.maximum(myarray.arr, myamulet.height_map())

    # Build
    myamulet.build(myarray.arr)

    print("Complete!")

def options():
    return AmuletWrapper.options() | {
        "Merge edges": ["bool", True], # This effects how "smooth" the results are
        "Random Seed": ["int", -1] # -1 for a random
    }


export = {
    "name": "Alpha Mountain v1",
    "operation": main,
    "options": options()
}
