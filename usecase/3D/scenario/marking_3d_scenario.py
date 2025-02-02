from core.swarm_sim_header import get_coordinates_in_direction
import random

def scenario(world):
    center = world.grid.get_center()
    dirs = world.grid.get_directions_list()

    world.add_particle(center)
    world.add_particle(get_coordinates_in_direction(center, random.choice(dirs)))

    size = 5

    ring = world.grid.get_n_sphere_border(center, size)

    for c in ring:
        world.add_tile(c, color=(0.0, 0.0, 0.0, 0.5))

