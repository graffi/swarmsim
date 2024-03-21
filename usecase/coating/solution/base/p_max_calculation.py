from lib.swarm_sim_header import *
from lib import agent as agent_class
from solution import solution_header


def find_p_max(agent: agent_class) -> None:
    """
    calculates the p_max for a agent based on all information this agent has
    @param agent: the agent for which the p_max should be calculated
    """
    if debug and debug_p_max_calculation:
        print("\n After P", agent.number, "own distance", agent.own_dist)
        print("Direction | Distance")
        for direction in direction_list:
            print(direction_number_to_string(direction), "|", agent.nh_list[direction])
        print("Before P MAX:")
        print("id | dist | direction")
        print(agent.p_max)

    own_p_max(agent.own_dist, agent.p_max, agent.number, agent.nh_list)
    global_p_max(agent)

    if debug and debug_p_max_calculation:
        print("P MAX:")
        print("id | dist | direction")
        print(agent.p_max)

    if debug and debug_p_max_calculation:
        print("P_Max Table \n ID | Distance")
        print(agent.p_max_table)


def own_p_max(own_distance: float, p_max: solution_header.PMaxInfo, agent_number: int,
              nh_list: solution_header.NH_LIST_TYPE) -> bool:
    """
    Checks if this agent or any of its neighbors has maximum distance and sets the values of the p_max object
    @return: True if this agent is at maximum distance, False otherwise
    @param own_distance: the distance of this agent
    @param p_max: the current p_max of this agent. Will be changed if this agent is at maximum distance
    @param agent_number: the agents id
    @param nh_list: the agents neighborhood
    """
    if own_distance is not math.inf:
        p_max.dist = own_distance
        p_max.ids = {agent_number}
        for direction in direction_list:
            neighbor = nh_list[direction]
            if neighbor.type == "p" and p_max.dist < neighbor.dist:
                p_max.dist = neighbor.dist
    return False


def global_p_max(agent: agent_class) -> None:
    """
    Finds the greatest p_max in all messages received
    @param agent: the agent for which the p_max should be calculated
    """
    for rcv_direction in agent.rcv_buf:
        if isinstance(agent.rcv_buf[rcv_direction], solution_header.PMax):
            if agent.rcv_buf[rcv_direction].p_max_dist > agent.p_max.dist:
                agent.p_max.dist = agent.rcv_buf[rcv_direction].p_max_dist
                agent.p_max.ids = {agent.number}