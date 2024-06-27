# amulet-plugins
Collection of custom plugins built for https://www.amuletmc.com/


## Plugins:

### castle_generator.py
Generate a simple castle in the selection, including walls and towers.

Options:
* Flatten - Replace pre-existing blocks with air
* Towers - Add towers to the castle corners
* Tower Size - The size of the towers
* Wall Width - The size of the walls
* Dimples - Vary the castle parapet each block.
* Fix Dimples - Force the castle to have "perfect" dimples (**Warning: this will ignore your selection box**)

### perlin_noise.py
Generate perlin noise over the selection.

Options:
* Flatten - Replace pre-existing blocks with air
* Frequency - Increase resolution / noise detail
* Random Seed - Set the seed used for generation (use -1 for a random value.)

### mountain_v1.py
Generate mountains using Perlin noise, runs multiple layers of noise and then merge together.

> [!NOTE]
> This code is very CPU intensive

Options:
* Flatten - Replace pre-existing blocks with air
* Merge edges - Reduce effect towards the edges of the selection
* Random Seed - Set the seed used for generation (use -1 for a random value.)
