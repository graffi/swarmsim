from scenario.scenario_std_lib import *

max=20


def scenario(sim):
    sim.add_tile(0, 0)
    sim.add_tile(0.5, 1.0)
    sim.add_tile(1.0, 2.0)
    sim.add_tile(1.5, 3.0)
    sim.add_tile(2.0, 4.0)
    sim.add_tile(2.5, 5.0)
    sim.add_tile(3.0, 6.0)
    sim.add_tile(3.5, 7.0)
    sim.add_tile(4.0, 8.0)

    generating_random_spraded_particles(sim, max)