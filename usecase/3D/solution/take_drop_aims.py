def solution(world):
    dirs = world.grid.get_directions_list()

    if world.get_actual_round() == 1:
        world.get_particle_list()[0].take_tile_in(dirs[2])
    elif world.get_actual_round() == 2:
        world.get_particle_list()[0].drop_tile_in(dirs[0])
    elif world.get_actual_round() == 3:
        world.get_particle_list()[0].take_particle_in(dirs[0])
    elif world.get_actual_round() == 4:
        world.get_particle_list()[0].drop_particle_in(dirs[2])

    print(world.get_actual_round())