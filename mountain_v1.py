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

from lib.myamulet import AmuletWrapper


def main(world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict):

    foo = AmuletWrapper(world, dimension, selection, options)

    ## Init Matrix
    arrshape = (foo.width, foo.depth)
    arr = np.zeros(arrshape, dtype=int)

    #arr[0] = 1
    arr[6] = 1

    print(arr)

    foo.build(arr)

    print("Complete!")

def options():
    return AmuletWrapper.options() | {
        "Foobar": ["bool", True]
    }


export = {
    "name": "Mountain Generator v1",
    "operation": main,
    "options": options()
}
