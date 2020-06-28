def scenario(world):

    # Ants
    part_num = 0
    while part_num <= 30:
        ant = world.add_particle(0, 0)
        setattr(ant, "way_home_list", [])
        part_num += 1

    # Food
    world.add_tile(-5.0, 10.0)
    world.add_tile(5.0, 10.0)
    world.add_tile(10.0, -0.0)
    world.add_tile(5.0, -10.0)
    world.add_tile(-5.0, -10.0)
    world.add_tile(-10.0, 0.0)

    # Base
    world.add_marker(0, 0, 1)