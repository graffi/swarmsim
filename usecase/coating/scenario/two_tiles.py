import copy
from lib.swarm_sim_header import *


def scenario(sim, agent_count):
    if agent_count == -1:
        agent_count = 30
    sim.add_item((0, 0))
    sim.add_item((5, 0))
    generating_random_spraded_agents(sim, agent_count)