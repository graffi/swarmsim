import random
#Standard Lib that has to be in each solution
from lib.std_lib import *

def solution(sim):

    if sim.get_actual_round() % 2 == 0:
        for particle in sim.get_particle_list():
            particle.move_to(random.choice(direction))