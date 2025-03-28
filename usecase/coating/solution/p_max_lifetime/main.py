#from lib import world, agent as agent_class
import copy
from core import world, agent as agent_class
import random
# from usecase.coating.solution.p_max_lifetime.swarm_sim_header import *
from core.swarm_sim_header import *
# import solution.p_max_lifetime.distance_calculation as distance_calc_mod
import usecase.coating.solution.p_max_lifetime.distance_calculation as distance_calc_mod
# import solution.p_max_lifetime.read_write as read_write_mod
import usecase.coating.solution.p_max_lifetime.read_write as read_write_mod
# import solution.p_max_lifetime.p_max_calculation as p_max_calc_mod
import usecase.coating.solution.p_max_lifetime.p_max_calculation as p_max_calc_mod
#  import solution.p_max_lifetime.coating_alg as coating_alg
import usecase.coating.solution.p_max_lifetime.coating_alg as coating_mod
# import solution.goal_test as goal_test
import usecase.coating.solution.p_max_lifetime.coating_alg as coating_alg
import usecase.coating.solution.goal_test as goal_test
import colorsys

cycle_no = 3


# def solution(sim: world) -> None:
def solution(world):
    """
    Main solution function that is called each round
    @param sim: the current world state
    """
    # code for deleting agents to test robustness
    if world.config_data.agent_fail_quote > 0 and world.get_actual_round() == 300:
        for to_delete in list(filter(lambda x: x.willfail, world.agents)):
            to_delete.delete_agent()


## KG: Currently stuck here
    if world.get_actual_round() == 1:
        # coating_mod.initialize_agents(world)
        print("My list of ", len(world.agents)," agents: ", world.agents)

        coating_mod.initialize_agents(world)


    for agent in world.agents:
        currentColor = agent.get_color()
        set_rainbow_color(agent)
        # resets all agents last movement direction every 10 cycles
        print("Agent Nr ", str(agent.number), " Color: ", agent.get_color())
        if world.get_actual_round() % (cycle_no * 10) == 1:
            if len(agent.prev_direction) > 0:
                agent.prev_direction.pop(0)

        if world.get_actual_round() % cycle_no == 1:
            if agent.wait:
                agent.wait = False
            else:
                move_cycle(agent)

        elif world.get_actual_round() % cycle_no == 2:
            read_cycle(agent)

        elif world.get_actual_round() % cycle_no == 0:
            write_cycle(agent)

    goal_test.end_sim(world)


# def initialize_agents(sim: world) -> None:
def initialize_agents(world):
    """
    handles initialization for all agents in round 1
    @param world: the current world state
    """
    for agent in world.agents:
        # coating_alg.initialize_agent(agent)
        if color is None:
            color = self.config_data.agent_color
        else:
            color = agent.set_rainbow_color()
        initialize_agent(agent)
        # agent.set_color(currcol)

        if random.random() < world.config_data.agent_fail_quote:
            agent.willfail = True
        agent.dest_t = random.choice(world.get_items_list()).coordinates
        print("dfsdfjhakjahskf")


# def write_cycle(agent: agent_class) -> None:
def write_cycle(agent):
    """
    lets the current agent send messages to its neighbors
    @param agent: the agent whose turn it is
    """
    agent.next_direction = coating_alg.coating_alg(agent)
    if agent.own_dist != math.inf:




        if len(agent.p_max.ids) > 0 and agent.p_max.dist > 0:
            set_rainbow_color(agent)



        if len(agent.p_max.ids) > 0 and agent.p_max.dist > 0 and agent.next_direction is False:
            # agent.p_max_table.update({agent.p_max.id: agent.p_max.dist})
            read_write_mod.send_p_max_to_neighbors(agent)
        else:
            read_write_mod.send_own_dist_to_neighbors(agent)
    else:
        next_dir = get_next_direction_to(agent.coordinates[0], agent.coordinates[1],
                                         agent.dest_t[0], agent.dest_t[1])
        if agent.agent_in(next_dir):
            read_write_mod.send_target_item(agent, next_dir)


def set_rainbow_color(agent):
    agentCount = len(agent.world.agents)
    myDist = agent.own_dist
    agentMaxDist = agent.p_max.dist

    # Saturation and Value are set to 1 for full color
    saturation = 1.0
    value = 1.0

    # Normalize myDist to a value between 0 and 1
    normalized_dist = 0
    normalized_dist = myDist / agentMaxDist

    # Convert the normalized value to a hue in the HSV color space
    hue = normalized_dist
    rgba = (0.0,0.0,0.0,1.0)


    # Convert HSV to RGB
    try:
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        rgba = (rgb[0], rgb[1], rgb[2], 1.0)
        print("Success: myDist", myDist, "Max", agentMaxDist, "Hue ", hue, "Saturation", saturation, "Value", value, "RGBA", rgba)
    except:
        print("Failed: myDist", myDist, "Max", agentMaxDist, "Hue ", hue, "Saturation", saturation, "Value", value, "RGBA", rgba)
    # Convert RGB to RGBA by adding an alpha value of 1.0


    # Set the color of the agent
    agent.set_color(rgba)

# def read_cycle(agent: agent_class) -> None:
def read_cycle(agent):
    """
    Lets the current agent read messages from its neighbors and calculate distances for each neighbor location
    @param agent: the agent whose turn it is
    """
    if debug and debug_read:
        print("reading memory of agent", agent.number)
    agent.rcv_buf = read_write_mod.read_and_clear(agent.read_whole_memory())
    agent.nh_list = distance_calc_mod.calculate_distances(agent)
    p_max_calc_mod.find_p_max(agent)
    if agent.own_dist is math.inf:
        read_write_mod.check_for_new_target_item(agent)
    agent.rcv_buf_dbg = copy.deepcopy(agent.rcv_buf)
    agent.rcv_buf.clear()


# def move_cycle(agent: agent_class) -> None:
def move_cycle(agent):
    """
    Lets the current agent move
    @param agent: the agent whose turn it is
    """
    if agent.next_direction is False and agent.own_dist > 1:

        if debug and debug_movement:
            print("moving closer to target item")
        move_to_target_item(agent)
    elif agent.next_direction is not False and not agent.agent_in(agent.next_direction) \
            and not agent.item_in(agent.next_direction):
        move_to_next_dir(agent)
    coating_alg.reset_p_max(agent)


# def move_to_next_dir(agent: agent_class) -> None:
def move_to_next_dir(agent):
    """
    Moves the agent to the next direction calculated by the algorithm
    @param agent: the agent whose turn it is
    """
    if len(agent.prev_direction) >= agent.max_prev_dirs:
        agent.prev_direction.pop(0)
    agent.prev_direction.append(get_the_invert(agent.next_direction))
    agent.move_to(agent.next_direction)
    if debug:
        print("dist list before moving", [str(neighbor) for neighbor in agent.nh_list])
        print("\n P", agent.number, " coates to", direction_number_to_string(agent.next_direction))
    new_own_dist = agent.nh_list[agent.next_direction].dist
    neighbor_left = agent.nh_list[direction_in_range(agent.next_direction - 1)]
    neighbor_right = agent.nh_list[direction_in_range(agent.next_direction + 1)]
    coating_alg.reset_attributes(agent)
    coating_alg.reset_p_max(agent)
    agent.wait = True
    agent.own_dist = new_own_dist
    agent.nh_list[direction_in_range(agent.prev_direction[-1] + 1)] = neighbor_left
    agent.nh_list[direction_in_range(agent.prev_direction[-1] - 1)] = neighbor_right


# def move_to_target_item(agent: agent_class) -> None:
def move_to_target_item(agent):
    """
    Moves the agent in the global direction of it's target item
    This method uses information from the world class
    @param agent: the agent whose turn it is
    """
    hit_a_matter = move_to_dest_step_by_step(agent, agent.dest_t, agent.prev_direction)
    if hit_a_matter or hit_a_matter is None:
        # reset_attributes(agent)
        if hit_a_matter is not None:
            if agent.own_dist > distance_calc_mod.calc_own_dist_t(hit_a_matter):
                agent.own_dist = distance_calc_mod.calc_own_dist_t(hit_a_matter)
            if hit_a_matter.type == "item" and debug:
                print("got a distance from a item")
    else:
        coating_alg.reset_attributes(agent)
        coating_alg.reset_p_max(agent)
        agent.wait = True
