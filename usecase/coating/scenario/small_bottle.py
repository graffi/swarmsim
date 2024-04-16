from lib.swarm_sim_header import *


def scenario(world, agent_count):
	if agent_count == -1:
		agent_count = 42
	world.add_item((0.0, 0.0, 0.0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((-1.0, 0.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((-2.0, -0.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((-3.0, -0.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((-3.5, 1.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((-4.0, 2.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((-4.5, 3.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((-4.0, 4.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((-3.5, 5.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((-3.0, 6.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((-2.0, 6.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((-1.0, 6.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((-0.0, 6.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((0.5, 5.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((1.0, 4.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((1.5, 3.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((1.0, 2.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((1.0, -0.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((2.0, 2.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((2.0, 0.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((3.0, 2.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	world.add_item((3.0, 0.0, 0), color=(0.3, 0.3, 0.8, 1.0))
	#world.add_location((0.0, 0.0))
	generating_random_spraded_agents(world, agent_count)
