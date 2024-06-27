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

class ArrayHelper:
    def __init__(self, width, depth, height):
        self.height = height
        self.arr = np.zeros((width, depth))
    
    def mergeArray(self, array2):
        if self.arr.shape == array2.shape:
            self.arr = np.add(self.arr, array2)
        else:
            # UGH 
            self.arr = np.add(self.arr, np.rot90(array2, 1))

    def normalised(self):
        return self.arr * (1.0/self.arr.max())


def main(world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict):

    myamulet = AmuletWrapper(world, dimension, selection, options)

    myarray = ArrayHelper(myamulet.width, myamulet.depth, myamulet.height)
    #print(myarray.arr)

    seed = options['Random Seed']
    if options['Random Seed'] == -1:
        seed = int(random.random() * 10 ** 9) # seed has to be less than (2 ** 32 - 1)

    # Add ground height
    if options['Merge with ground']:
        myarray.mergeArray(myamulet.height_map())

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
    for iter in range(1, round((myamulet.width + myamulet.height) / 32) + 1):
        print("Foo"+str(frequency)+str(iter))
        addNoise(myarray, frequency ** iter)


    # todo:
    # * Pass arr through filter multiplying only tiles near the center.

    #print("building...")
    #print(myarray.normalised())
    myamulet.build(np.multiply(myarray.normalised(), myamulet.height))

    print("Complete!")

def options():
    return AmuletWrapper.options() | {
        "Merge with ground": ["bool", False], # This effects how "smooth" the results are
        "Random Seed": ["int", -1] # -1 for a random
    }


export = {
    "name": "Alpha Mountain v1",
    "operation": main,
    "options": options()
}
