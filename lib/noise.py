import numpy as np

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


def main():
    arr = generate_perlin_noise(6,10,1,2).clip(min=0)
    #print(arr)
    #arr = np.add(arr, generate_perlin_noise(6,10,1,4))
    #print(np.round(arr.clip(min=0), decimals = 6))
    #print(arr)
    #arr = np.add(arr, generate_perlin_noise(6,10,1,2))
    arr *= (1.0/arr.max())
    print(arr)

    print("complete")

if __name__ == "__main__":
    main()