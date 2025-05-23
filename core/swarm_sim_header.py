from core.matter import MatterType

import sys
import random
import math
debug = 0
debug_write = 0
debug_read = 0
debug_p_max_calculation = 0
debug_distance_calculation = 0
debug_movement = 0
direction_list = [0, 1, 2, 3, 4, 5]
direction_to_coords = [(0.5, 1, 0),
                       (1, 0, 0),
                       (0.5, -1, 0),
                       (-0.5, -1, 0),
                       (-1, 0, 0),
                       (-0.5, 1, 0)]
simple_direction_map = {"NE": 0, "E": 1, "SE": 2, "SW": 3, "W": 4, "NW": 5}

def get_coordinates_in_direction(coordinates, direction):
    """
    Returns the coordinates data of the pointed directions

    :param coordinates: agents actual staying coordination
    :param direction: The direction. Options:  E, SE, SW, W, NW, or NE
    :return: The coordinates of the pointed directions
    """
    if hasattr(direction, "__getitem__"):
        return coordinates[0] + direction[0], coordinates[1] + direction[1], coordinates[2] + direction[2]
    else:
        return coordinates[0] + direction_to_coords[direction][0], coordinates[1] + direction_to_coords[direction][1],\
               coordinates[2] + direction_to_coords[direction][2]


def get_multiple_steps_in_direction(start, direction, steps):
    """
    returns coordinates of the point from the start variable in x steps in the given direction
    :param start: the starting point
    :param direction: the directionF
    :param steps: the amount of steps
    :return: coordinates (float, float, float)
    """
    return start[0] + (direction[0] * steps), start[1] + (direction[1] * steps), start[2] + (direction[2] * steps)


def scan_in(matter_map: dict, center, hop, grid):
    result = []
    n_sphere_border = grid.get_n_sphere_border(center, hop)
    for coords in n_sphere_border:
        if coords in matter_map:
            result.append(matter_map[coords])
    return result


def scan_within(matter_map, center, hop, grid):
    result = []
    n_sphere_border = grid.get_n_sphere(center, hop)
    for coords in n_sphere_border:
        if coords in matter_map:
            result.append(matter_map[coords])
    return result


def create_matter_in_line(world, start, direction, amount, matter_type=MatterType.AGENT):
    current_position = start
    for _ in range(amount):
        if matter_type == MatterType.AGENT:
            world.add_agent(current_position)
        elif matter_type == MatterType.ITEM:
            world.add_item(current_position)
        elif matter_type == MatterType.LOCATION:
            world.add_location(current_position)
        else:
            print("create_matter_in_line: unknown type (allowed: agent, item or location")
            return
        current_position = get_coordinates_in_direction(current_position, direction)


def generating_random_spraded_agents(world, max_size_agent):
    for _ in range(0, max_size_agent):
        x = random.randrange(-world.get_x_size(), world.get_x_size())
        y = random.randrange(-world.get_y_size(), world.get_y_size())
        if y % 2 == 1:
            x = x + 0.5
        while (x, y, 0.0) in world.item_map_coordinates or (x, y, 0.0) in world.agent_map_coordinates:
            x = random.randrange(-world.get_x_size(), world.get_x_size())
            y = random.randrange(-world.get_y_size(), world.get_y_size())
            if y % 2 == 1:
                x = x + 0.5
        world.add_agent((x, y, 0.0))


def move_to_dest_step_by_step(agent, destiny, prev_dir=None):
    """

    :param agent:
    :param destiny:
    :param prev_dir
    :return: True if movement occured, False if not movment and a Matter if the next direction point has a matter on it
    """
    if prev_dir is None:
        prev_dir = []
    # print("get_next_direction_to(agent.coordinates[0] = ",agent.coordinates[0]," agent.coordinates[1] = ", agent.coordinates[1], "destiny[0] = ", destiny[0], " destiny[1]) = ", destiny[1] )
    next_dir = get_next_direction_to(agent.coordinates[0], agent.coordinates[1], destiny[0], destiny[1])
    # print ("nextdir = ", next_dir )
    if next_dir in prev_dir:
        return None
    if agent.item_in(next_dir) or agent.agent_in(next_dir):
        agent.get_matter_in(next_dir)
        return agent.get_matter_in(next_dir)
    if len(agent.prev_direction) >= agent.max_prev_dirs:
        agent.prev_direction.pop(0)
    agent.prev_direction.append(get_the_invert(next_dir))
    agent.move_to(next_dir)
    if debug and debug_movement:
        print("\n P", agent.number, " moves to", direction_coordinates_to_string(next_dir, directions))
    return False


def direction_number_to_string(direction):
    direction_names = ["NE", "E", "SE", "SW", "W", "NW"]
    return direction_names[direction]


def direction_coordinates_to_string(direction, directions):
    return next(key for key, value in directions.items() if value == direction)


def get_next_direction_to(src_x, src_y, dest_x, dest_y):
    """
    :param src_x: x coordinate of the source
    :param src_y: y coordinate of the source
    :param dest_x: x coordinate of the destiny
    :param dest_y: y coordinate of the destiny
    :return: the next direction that brings the matter closer to the destiny
    """
    next_dir = -1
    if (src_x < dest_x or src_x == dest_x) and src_y < dest_y:
        next_dir = simple_direction_map["NE"]
    elif src_y < dest_y and src_x > dest_x:
        next_dir = simple_direction_map["NW"]
    elif src_y > dest_y and src_x < dest_x:
        next_dir = simple_direction_map["SE"]
    elif (src_x > dest_x or src_x == dest_x) and src_y > dest_y:
        next_dir = simple_direction_map["SW"]
    elif src_y == dest_y and src_x > dest_x:
        next_dir = simple_direction_map["W"]
    elif src_y == dest_y and src_x < dest_x:
        next_dir = simple_direction_map["E"]
    return next_dir


def get_the_invert(direction):
    return (direction + 3) % 6


def direction_in_range(direction):
    return direction % 6