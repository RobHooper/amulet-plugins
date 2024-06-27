import numpy as np

try:
    from lib.arrayhelper import ArrayHelper
except ModuleNotFoundError:
    # When ran directly :/
    from arrayhelper import ArrayHelper

def generate_gradients(grid_size):
    angles = np.random.rand(grid_size, grid_size) * 2 * np.pi
    gradients = np.dstack((np.cos(angles), np.sin(angles)))

    return gradients

def dot_grid_gradient(ix, iy, x, y, gradients):
    dx, dy = x - ix, y - iy
    gradient = gradients[iy % gradients.shape[0], ix % gradients.shape[1]]
    return dx * gradient[0] + dy * gradient[1]

def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def lerp(a, b, t):
    return a + t * (b - a)

def perlin_noise(x, y, gradients):
    ix, iy = int(x), int(y)
    sx, sy = fade(x - ix), fade(y - iy)

    n0 = dot_grid_gradient(ix, iy, x, y, gradients)
    n1 = dot_grid_gradient(ix + 1, iy, x, y, gradients)
    ix0 = lerp(n0, n1, sx)

    n0 = dot_grid_gradient(ix, iy + 1, x, y, gradients)
    n1 = dot_grid_gradient(ix + 1, iy + 1, x, y, gradients)
    ix1 = lerp(n0, n1, sx)

    return lerp(ix0, ix1, sy)

def generate_perlin_noise(width, depth, height, grid_size, seed = 10):
    """
    width = size of array
    depth = size of array
    height = value multiplier
    grid_size // frequency = the resolution of gradients within array
    """
    np.random.seed(seed)

    gradients = generate_gradients(grid_size)
    noise = np.zeros((depth, width))
    
    for i in range(depth):
        for j in range(width):
            x = j / (width / (grid_size - 1))
            y = i / (depth / (grid_size - 1))
            noise[i, j] = perlin_noise(x, y, gradients) * height
    
    return noise

def center_grid(depth, width):
    """
    Returns a grid of values increasing towards the center

    FIXME:  This is not as good as it can be.. a 3 by 3 grid for instance foobar's it
            I would like to round up when we half the array then drop a row to fit.
    """
    #print(f"Asked for: {(depth, width)}")
          
    myarray = ArrayHelper(depth = int(depth /2), width = int(width /2))

    for row in range(myarray.arr.shape[0]):
        myarray.arr[row] += row
    for col in range(myarray.arr.shape[1]):
        myarray.arr[:,col] += col 
    
    myarray.arr = np.concatenate((myarray.arr, np.flip(myarray.arr, 1)), 1)
    myarray.arr = np.concatenate((myarray.arr, np.flip(myarray.arr)))

    myarray.arr = myarray.normalised()

    myarray.arr = np.pad(
        myarray.arr, 
        [(0, depth - myarray.arr.shape[0]), (0, width - myarray.arr.shape[1])], 
        mode='constant', 
        constant_values=0.1
    )
    #print(myarray.arr.shape)

    return myarray.arr

def main():
    #arr = generate_perlin_noise(6,10,1,4).clip(min=0)
    #print(arr)
    #arr = np.add(arr, generate_perlin_noise(6,10,1,4))
    #print(np.round(arr.clip(min=0), decimals = 6))
    #print(arr)
    #arr = np.add(arr, generate_perlin_noise(6,10,1,2))
    #arr *= (1.0/arr.max())
    # arr = center_grid(5,5)
    arr = center_grid(7,5)
    print(np.round(arr, decimals=6))

    print("complete")

if __name__ == "__main__":
    main()