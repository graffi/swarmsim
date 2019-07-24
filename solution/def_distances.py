from solution.std_lib import *
import math

class Neighbors:
    def __init__(self, type, dist):
        self.type = type
        self.dist = dist

    def __str__(self):
        return " " + str(self.type)  + " " + str(self.dist)


debug = 1


def def_distances(particle):
    if debug:
        print("\n***************************************************************")
        print(" Before P", particle.number, "own distance", particle.own_dist, "coords", particle.coords)

    particle.nh_dict = scan_nh(particle)

    for dir in particle.nh_dict:
        particle.nh_dict[dir].dist = get_nh_dist(particle, dir)
    if debug :
        print("Direction | Type | Distance")
        for dir in particle.nh_dict:
            print(dir_to_str(dir), "|", particle.nh_dict[dir].type, "|", particle.nh_dict[dir].dist)
    particle.own_dist = calc_own_dist(particle)

    if particle.own_dist is not math.inf:
        for dir in particle.nh_dict:
            particle.nh_dict[dir].dist = calc_nh_dist(dir, particle)
            #if particle is beside a tile then this tile is the new target
            if particle.nh_dict[dir].type == "t":
                particle.dest_t == particle.get_tile_in(dir)

        for dir in particle.nh_dict:
            particle.fl_min = set_min_fl(particle)
        #def_min_dist_fl(particle)
        #def_max_dist_p(particle)
    if debug:
        print("\n After P", particle.number, "own distance", particle.own_dist)
        print("Direction | Type | Distance")
        for dir in particle.nh_dict:
            print(dir_to_str(dir),"|",particle.nh_dict[dir].type, "|", particle.nh_dict[dir].dist )



def scan_nh(particle):
    nh_dict = dict()
    for dir in direction:
        if particle.particle_in(dir):
            nh_dict[dir] = Neighbors("p", math.inf)
        elif particle.tile_in(dir):
            nh_dict[dir] = Neighbors("t", 0)
        else:
            nh_dict[dir] = Neighbors("fl", math.inf)
    return nh_dict


def get_nh_dist(particle, dir):
    if particle.nh_dict[dir].type == "t":
        return 0
    elif particle.nh_dict[dir].type == "p":
        if dir in particle.rcv_buf:
            return particle.rcv_buf[dir].own_dist
    return math.inf


def calc_own_dist(particle):
    min_key = min(particle.nh_dict.keys(), key=(lambda k: particle.nh_dict[k].dist))
    return particle.nh_dict[min_key].dist + 1


def calc_nh_dist(dir, particle):
    if particle.nh_dict[dir].dist is math.inf and \
            (particle.own_dist != math.inf or \
            particle.nh_dict[dir_in_range(dir + 1)].dist != math.inf or \
            particle.nh_dict[dir_in_range(dir - 1)].dist != math.inf) :
        # """
        # if the defined direction is a FL and in SE, SW, NW, NE and the min dist is coming
        #  from one of those direction than the fl becomes the same distance
        # """
        if particle.nh_dict[dir].type == "fl" and dir in [SE, SW, NE, NW]:
            min_dir = min ([dir_in_range(dir + 1), dir_in_range(dir - 1)], key=(lambda k:  particle.nh_dict[k].dist) )
            if min_dir in [SE, SW, NE, NW]:
                return min(particle.nh_dict[min_dir].dist, particle.own_dist)
        return 1 + min(particle.own_dist,
                        particle.nh_dict[dir_in_range(dir + 1)].dist,
                        particle.nh_dict[dir_in_range(dir - 1)].dist)

    return particle.nh_dict[dir].dist

def set_min_fl(particle):
       pass

def def_min_dist_fl(particle):
    for dir in particle.fl_dir_list:
        loc_min_fl(dir, particle)
    for dir in particle.rcv_buf:
        gl_min_fl(dir, particle)


def loc_min_fl(dir, particle,):
    if particle.nh_dict[dir].dist == particle.loc_fl_min_dist and len(particle.loc_fl_min_dir) > 0:
        particle.loc_fl_min_dir.append(dir)

    elif particle.nh_dict[dir].dist <= particle.own_dist:
        particle.loc_fl_min_dist= particle.gl_fl_min_dist = particle.nh_dict[dir].dist
        particle.loc_fl_min_dir.clear()
        particle.loc_fl_min_dir.append(dir)
        particle.gl_fl_min_dir = dir
        particle.gl_fl_min_hop = 1


def gl_min_fl(dir, particle):
    if particle.rcv_buf[dir].fl_min_dist < particle.gl_fl_min_dist:
        particle.gl_fl_min_dist = particle.rcv_buf[dir].fl_min_dist
        particle.gl_fl_min_dir = dir
        particle.gl_fl_min_hop = particle.rcv_buf[dir].fl_min_hop + 1
    elif particle.rcv_buf[dir].fl_min_dist == particle.gl_fl_min_dist \
            and particle.rcv_buf[dir].fl_min_hop + 1 < particle.gl_fl_min_hop:
        particle.gl_fl_min_dir = dir
        particle.gl_fl_min_hop = particle.rcv_buf[dir].fl_min_hop + 1


def def_max_dist_p(particle):
    for dir in particle.p_dir_list:
        loc_max_p(dir, particle)
    for dir in particle.rcv_buf:
        gl_p_max(dir, particle)

def loc_max_p(dir, particle):
    if particle.nh_dict[dir].dist > particle.gl_p_max_dist:
        particle.loc_p_max_dist = particle.gl_p_max_dist = particle.nh_dict[dir].dist
        particle.loc_p_max_dir = particle.gl_p_max_dir = dir
        particle.gl_p_max_hop = 1
        particle.gl_p_max_id = particle.get_particle_in(dir).number

def gl_p_max(dir, particle):
    if particle.rcv_buf[dir].p_max_dist != math.inf and particle.gl_p_max_dist != math.inf:
        if particle.rcv_buf[dir].p_max_dist > particle.gl_p_max_dist:
            particle.gl_p_max_dist = particle.rcv_buf[dir].p_max_dist
            particle.gl_p_max_dir = dir
            particle.gl_p_max_hop = particle.rcv_buf[dir].p_max_hop + 1
            particle.gl_p_max_id = particle.rcv_buf[dir].p_max_id
        elif particle.rcv_buf[dir].p_max_dist == particle.gl_p_max_dist \
                and  particle.rcv_buf[dir].p_max_hop + 1 < particle.gl_p_max_hop :
            particle.gl_p_max_dir = dir
            particle.gl_p_max_hop = particle.rcv_buf[dir].p_max_hop + 1
            particle.gl_p_max_id = particle.rcv_buf[dir].p_max_id