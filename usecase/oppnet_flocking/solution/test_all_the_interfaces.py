"""
This solution tests all the interfaces that are provided from swarm-world MAX Round must be at least 41
"""

import logging
import random
from lib.swarm_sim_header import get_multiple_steps_in_direction

def solution(world):
    dirs = world.grid.get_directions_list()
    center = world.grid.get_center()

    if world.get_actual_round() == 1:
        print("Scanning for locations, tiles and particles")
        logging.info("Scanning for locations, tiles and particles")
        all_matters_list = world.get_particle_map_coordinates()[center].scan_for_matters_within()
        for list in all_matters_list:
            if list.type == 'particle':
                print("particle at", list.coordinates)
            elif list.type == 'tile':
                print("tile", list.coordinates)
            elif list.type == 'location':
                print("location", list.coordinates)
        print("Testing Interface: Take Drop Tiles and Particles")
        logging.info("Testing Interface: Take Drop Tiles and Particles")

    elif world.get_actual_round() == 2:
        print("Round 2")
        world.get_particle_list()[0].take_tile_in(dirs[1])
    elif world.get_actual_round() == 3:
        print("Round 3")
        world.get_particle_list()[0].take_particle_in(dirs[1])
    elif world.get_actual_round() == 4:
        print("Round 4")
        world.get_particle_list()[0].drop_tile_in(dirs[1])
        print("Tiles coordinates ", world.get_tiles_list()[0].coordinates[0], world.get_tiles_list()[0].coordinates[1])
    elif world.get_actual_round() == 5:
        print("Tiles coordinates ", world.get_tiles_list()[0].coordinates[0], world.get_tiles_list()[0].coordinates[1])
        world.get_particle_list()[0].take_particle_in(dirs[3])
    elif world.get_actual_round() == 6:
        world.get_particle_list()[0].drop_particle_in(dirs[3])
        world.get_particle_list()[0].take_tile_in(dirs[1])
    elif world.get_actual_round() == 7:
        world.get_particle_list()[0].drop_tile()
        world.get_particle_list()[0].take_tile()
    elif world.get_actual_round() == 8:
        world.get_particle_list()[0].drop_particle_in(dirs[3])
        world.get_particle_list()[0].take_particle_in(dirs[3])
    elif world.get_actual_round() == 9:
        world.get_particle_list()[0].drop_particle()
    elif world.get_actual_round() == 10:
        if len(world.get_particle_list()) > 1:
            world.get_particle_list()[0].take_particle_with(world.get_particle_list()[1].get_id())
    elif world.get_actual_round() == 11:
        world.get_particle_list()[0].drop_particle()
        if len(world.get_tiles_list()) > 0:
            world.get_particle_list()[0].take_tile_with(world.get_tiles_list()[0].get_id())
    elif world.get_actual_round() == 12:
        world.get_particle_list()[0].drop_tile()
        world.get_particle_list()[0].take_tile_on(center)
    elif world.get_actual_round() == 13:
        world.get_particle_list()[0].drop_tile_on(get_multiple_steps_in_direction(center, dirs[1], 4))
    elif world.get_actual_round() == 14:
        world.get_particle_list()[0].take_particle()
    elif world.get_actual_round() == 15:
        world.get_particle_list()[0].drop_particle_on(get_multiple_steps_in_direction(center, dirs[3], 4))

    elif world.get_actual_round() == 16:
        logging.info("Testing Read and Write")
        print("Testing Read and Write")
        logging.info("Start Writing ")
        print("Start Writing")

        world.get_particle_list()[0].write_to_with(world.locations[0], "K1", "location Data")
        world.get_particle_list()[0].write_to_with(world.tiles[0], "K1", "Tile Data")
        world.get_particle_list()[0].write_to_with(world.get_particle_list()[1], "K1", "Particle Data")
    elif world.get_actual_round() == 17:
        logging.info("Start Reading")
        print("Start Reading")
        loc_data = world.get_particle_list()[0].read_from_with(world.locations[0], "K1")
        tile_data = world.get_particle_list()[0].read_from_with(world.tiles[0], "K1")
        part_data = world.get_particle_list()[0].read_from_with(world.get_particle_list()[1], "K1")

        if loc_data != 0:
            print(loc_data)
        if tile_data != 0:
            print(tile_data)
        if part_data != 0:
            print(part_data)

    elif world.get_actual_round() > 20:
        for particle in world.get_particle_list():
            particle.move_to(random.choice(dirs))
            if particle.coordinates in world.get_tile_map_coordinates():
                print("Found Tile")
                particle.take_tile()
                particle.carried_tile.set_color((0.5, 0.5, 0.5, 1.0))
                world.csv_round.success()
    if world.get_actual_round() == 24:
        world.get_particle_list()[1].create_tile()
        world.get_particle_list()[2].create_location()
        world.get_particle_list()[3].create_particle()

    if world.get_actual_round() == 40:
        world.get_particle_list()[4].create_tile()
        world.get_particle_list()[5].create_location()
        world.get_particle_list()[6].create_particle()
