from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

from amulet.api.block import Block  # For working with Blocks
from amulet.api.block_entity import BlockEntity
from amulet_nbt import *  # For working with block properties

import numpy as np

class AmuletWrapper:
    def __init__(self, world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict):
        self.world = world
        self.dimension = dimension
        # self.selection = selection # Not needed yet..
        self.options = options
        self.box = selection[0]

    @property
    def width(self):
        return self.box.max_x - self.box.min_x
    
    @property
    def depth(self):
        return self.box.max_z - self.box.min_z

    @property
    def height(self):
        return self.box.max_y - self.box.min_y +1

    @staticmethod
    def options():
        """
        https://github.com/Amulet-Team/Amulet-Map-Editor/blob/master/amulet_map_editor/programs/edit/plugins/operations/examples/3_fixed_function_pipeline.py
        """
        return {
            "Flatten": ["bool", True]
        }
    
    def build(self, 
              arr: np.ndarray,
              block: Block = Block("minecraft", "stone", {}), 
              platform: str = "bedrock",
              version: tuple = (1, 17, 0),
              entity: BlockEntity = None,
              ):
        """
        Actually place the blocks.
        """
        for x in range(self.width):
            blx = x + self.box.min_x
            for z in range(self.depth):
                blz = z + self.box.min_z
                for y in range(self.height):
                    bly = y + self.box.min_y
                    # print(f"debug: {blx}, {bly}, {blz}") # Debug

                    if arr[x][z] >= 1:
                        blk = block
                        arr[x][z] -= 1
                    else:
                        # Skip if options.flatten is True
                        if self.options['Flatten'] == True:
                            blk = Block("minecraft", "air", {})
                        else:
                            continue

                    print(blk)

                    self.world.set_version_block(
                            blx,
                            bly,
                            blz,
                            self.dimension,
                            (platform, version),
                            blk,
                            entity
                    )

