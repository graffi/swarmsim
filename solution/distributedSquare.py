NE = 0
E = 1
SE = 2
SW = 3
W = 4
NW = 5


direction = [NE, E, SE, SW, W, NW]

def solution(sim):
    print("Runde", sim.get_actual_round())
    if sim.get_actual_round() == 1:
        init_particles(sim.get_particle_list())
        leader_election(sim.get_particle_list())

    if sim.get_actual_round() % 2 == 1:
        update_leaders(sim.get_particle_list())
        calc_movement(sim.get_particle_list())
    else:
        get_first_particle_to_move(sim.get_particle_list())


# elects leader with the highest id
def leader_election(particleList):
    for particle in particleList:
        send_max_id_to_all_nbs(particle)
    for particle in particleList:
        if particle.number == particle.read_memory_with("MaxID"):
            particle.write_memory_with("Leader", "True")
            particle.set_color(4)

# sends max id to all nbs and recursivley the nbs send it to their nbs
def send_max_id_to_all_nbs(particle):
    nbs = particle.scan_for_particle_within(hop=1)
    for neigh in nbs:
        if neigh.read_memory_with("MaxID") < particle.read_memory_with("MaxID"):
            particle.write_to_with(neigh, "MaxID", particle.read_memory_with("MaxID"))
            send_max_id_to_all_nbs(neigh)

# initialize the memory of the particles
def init_particles(particleList):
    for particle in particleList:
        particle.write_memory_with("MaxID", particle.number)
        particle.write_memory_with("Leader", "False")
        particle.write_memory_with("AnnounceNext", None)
        particle.write_memory_with("Mark", "False")
        particle.write_memory_with("Order", None)
        particle.write_memory_with("Direction", None)

def calc_movement(particleList):
    for particle in particleList:
        if particle.read_memory_with("Leader") == "True":
            i = 0
            while i < 6:
                nb = particle.get_particle_in(i)
                next_nb = particle.get_particle_in((i + 1) % 6)
                if nb != None and next_nb == None and nb.read_memory_with("Leader") == "False":
                    dir = (i + 2) % 6
                    return dictate(nb, dir)
                i = i + 1

#####################################################################################

def update_leaders(particleList):
    allLeadersRdy(particleList)
    newLeaders(particleList)
    for particle in particleList:
        refresh_mem(particle)


def newLeaders(particleList):
    for particle in particleList:
        if particle.read_memory_with("Leader") == "False" and particle.read_memory_with("Mark") == "True":
            particle.write_memory_with("Leader", "True")
            particle.set_color(4)

def allLeadersRdy(particleList):
    for particle in particleList:
        if particle.read_memory_with("Leader") == "True" and particle.read_memory_with("AnnounceNext") == None:
            w = particle.get_particle_in(W)
            sw = particle.get_particle_in(SW)
            se = particle.get_particle_in(SE)
            if sw != None and se != None and w != None:
                particle.write_memory_with("AnnounceNext", "True")
                markNextLeaders(particle)
            else:
                spreadNoNextLeaders(particle)

def markNextLeaders(particle):
    e = particle.get_particle_in(E)
    sw = particle.get_particle_in(SW)
    se = particle.get_particle_in(SE)
    if e.read_memory_with("Leader") == "False":
        e.write_memory_with("Mark", "True")
    if sw.read_memory_with("Leader") == "False":
        sw.write_memory_with("Mark", "True")
    if se.read_memory_with("Leader") == "False":
        se.write_memory_with("Mark", "True")

def demarkNextLeaders(particle):
    e = particle.get_particle_in(E)
    sw = particle.get_particle_in(SW)
    se = particle.get_particle_in(SE)
    if e != None:
        if e.read_memory_with("Leader") == "False":
            e.write_memory_with("Mark", "False")
    if sw != None:
        if sw.read_memory_with("Leader") == "False":
            sw.write_memory_with("Mark", "False")
    if se != None:
        if se.read_memory_with("Leader") == "False":
            se.write_memory_with("Mark", "False")

def spreadNoNextLeaders(particle):
    particle.write_memory_with("AnnounceNext", "False")
    particle.write_memory_with("Mark", "True")
    demarkNextLeaders(particle)
    nbs = particle.scan_for_particle_within(1)
    for nb in nbs:
        if nb.read_memory_with("Leader") == "True" and nb.read_memory_with("Mark") == "False":
            spreadNoNextLeaders(nb)

#####################################################################################

# leader tells non leader neighbour to move in a circle till every spot is filled
def dictate(particle, dir):
    particle.write_memory_with("Direction", dir)
    particle.write_memory_with("Mark", "True")
    particle.write_memory_with("Order", 1)
    particle.set_color(3)

    indepth_replacement(particle)

def indepth_replacement(particle):
    particle.set_color(3)
    nbs = particle.scan_for_particle_within(1)
    for nb in nbs:
        if nb.read_memory_with("Leader") == "False" and nb.read_memory_with("Mark") == "False":
            orderNr = particle.read_memory_with("Order")
            orderNr = orderNr + 1

            dir = calc_dir(particle, nb)

            nb.write_memory_with("Mark", "True")
            nb.write_memory_with("Order", orderNr)
            nb.write_memory_with("Direction", dir)

            return indepth_replacement(nb)

def calc_dir(p1, p2):
    i = 0
    while i < 6:
        tmp = p2.get_particle_in(i)
        if tmp == p1:
            return i
        i = i + 1

def get_first_particle_to_move(particleList):
    particleToMove = None

    for particle in particleList:
        if particle.read_memory_with("Order") == 1:
            particleToMove = particle
            break

    if particleToMove != None:
        move_in_right_order(particleToMove, 1)

def move_in_right_order(particle, orderNr):
    if particle.read_memory_with("Order") != orderNr:
        return

    nbs = particle.scan_for_particle_within(1)

    nextParticle = None
    if nbs != None:
        for nb in nbs:
            if nb.read_memory_with("Order") == (orderNr+1):
                nextParticle = nb
                break

    dir = particle.read_memory_with("Direction")
    particle.move_to(dir)
    particle.set_color(1)
    refresh_mem(particle)

    if nextParticle != None:
        move_in_right_order(nextParticle, (orderNr+1))

def refresh_mem(particle):
    particle.write_memory_with("Mark", "False")
    particle.write_memory_with("Order", None)
    particle.write_memory_with("Direction", None)
    particle.write_memory_with("AnnounceNext", None)
