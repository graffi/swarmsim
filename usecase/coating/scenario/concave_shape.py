from lib.swarm_sim_header import *


def scenario(sim, agent_count):
    if agent_count == -1:
        agent_count = 42
    sim.add_item((0, 0))
    sim.add_item((-1.0, 0.0))
    sim.add_item((-1.5, -1.0))
    sim.add_item((0.5, -1.0))
    sim.add_item((1.5, 1.0))
    sim.add_item((0.5, 1.0))
    sim.add_item((-1.0, 2.0))
    sim.add_item((-0.5, 1.0))
    sim.add_item((-1.5, 1.0))
    sim.add_item((0.5, 1.0))
    sim.add_item((0.5, 3.0))
    sim.add_item((-0.0, 2.0))
    sim.add_item((1.0, 4.0))
    sim.add_item((1.5, 5.0))
    sim.add_item((-0.5, 3.0))
    sim.add_item((-2.0, 4.0))
    sim.add_item((-1.5, 3.0))
    sim.add_item((-4.0, 4.0))
    sim.add_item((-3.0, 4.0))
    sim.add_item((-2.0, 6.0))
    sim.add_item((-1.5, 5.0))
    sim.add_item((-2.5, 1.0))
    sim.add_item((-3.5, 1.0))
    sim.add_item((-4.5, 1.0))
    #sim.add_location((0.0, 0.0))
    generating_random_spraded_agents(sim, agent_count)
