import numpy as np

class ArrayHelper:
    def __init__(self, depth, width, height = 1):
        self.height = height
        self.arr = np.zeros((depth, width))
    
    def mergeArray(self, array2):
        if self.arr.shape == array2.shape:
            self.arr = np.add(self.arr, array2)
        else:
            # UGH 
            self.arr = np.add(self.arr, np.rot90(array2, 1))

    def normalised(self):
        return self.arr * (1.0/self.arr.max())
