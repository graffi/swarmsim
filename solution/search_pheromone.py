import random
import matplotlib.pylab as plt

"""
particle color = mode
black   (1) = search-mode
green   (4) = track-follow-mode
violet (7) = home-mode

marker color = status
black (1) = base
green (4) = track
"""

NE = 0
E = 1
SE = 2
SW = 3
W = 4
NW = 5
DIRECTIONS = [NE, E, SE, SW, W, NW]

search_mode_color = 1
track_follow_mode_color = 4
home_mode_color = 7
search_track_color = 8
base_color = 1
track_color = 4
multi_layer_track_color = 9

global home
home = (0.0, 0.0)

# Particle respawn
def respawn(world):
    ant_number = 40
    while len(world.get_particle_list()) <= ant_number:
        ant = world.add_particle(0, 0)
        setattr(ant, "way_home_list", [])


# Decrease lifespan of a track
def evaporate(marker):
    normal_track_decrease_rate = 0.04
    multi_layer_track_decrease_rate = 0.04
    search_track_decrease_rate = 0.04
    if (marker.get_color() == track_color):
        marker.set_alpha(marker.get_alpha() - normal_track_decrease_rate)
    elif (marker.get_color() == multi_layer_track_color):
        marker.set_alpha(marker.get_alpha() - multi_layer_track_decrease_rate)
    elif (marker.get_color() == search_track_color):
        marker.set_alpha(marker.get_alpha() - search_track_decrease_rate)


# Decrease ant lifespan
def decrease_life_span(particle):
    ant_lifespan_decrease_rate = 0.01
    particle.set_alpha(particle.get_alpha() - ant_lifespan_decrease_rate)


# Decrease stack of food
def decrease_food_stack(food, particle):
    food_stack_decrease_rate = 0.1
    if (particle.coords == food.coords):
        food.set_alpha(food.get_alpha() - food_stack_decrease_rate)


# def start_dead_count(world):
#     global dead_count
#     if (world.get_actual_round() == 1):
#         dead_count = 0


def delete_track(marker, world):
    if (marker.get_alpha() == 0):
        world.remove_marker(marker.get_id())


# Kill ant, when no life span
def kill_ant(particle, world):
    if (particle.get_alpha() == 0):
        world.remove_particle(particle.get_id())
#        dead_count += 1


# When in search mode, search rendom
def search_food_mode(particle):
    if (particle.get_color() == search_mode_color):
        next_step = random.choice(filter_search_track(particle))
        particle.move_to(next_step)
        # Save way home
        particle.way_home_list.append(invert_dir(next_step))
        # Create search track
        particle.create_marker(search_track_color)


# If found food, go in home-mode
def home_mode(particle, world):
    if (particle.check_on_tile() == True):
        particle.set_color(home_mode_color)
        # Reduce food stack, when take food
        for food in world.get_tiles_list():
            decrease_food_stack(food, particle)
            delete_food(food, world)
        # Restore life span
        particle.set_alpha(1)

# Delete food when gone
def delete_food(food, world):
    if (food.get_alpha() == 0):
        world.remove_tile_on(food.coords)


def delete_search_track(particle, world):
    if (particle.check_on_marker() == True and particle.get_marker().get_color() == search_track_color):
        world.remove_marker(particle.get_marker().get_id())


# Lay new track or reinsorce old track
def lay_track(particle):
    if (particle.check_on_marker() == False):
        track = particle.create_marker(track_color)
        # If creating a new track, set attribute
        if (track != False):
            setattr(track, 'layer', 0)
    else:
        current_marker = particle.get_marker()
        current_marker.set_color(multi_layer_track_color)
        current_marker.layer += 1


# Go home the way you came
def go_home(particle):
    if (particle.way_home_list != []):
        particle.move_to(particle.way_home_list[-1])
        del (particle.way_home_list[-1])


# If found track, follow
def follow_mode(particle):
    if (particle.coords != home and particle.check_on_marker() == True and particle.get_color() != home_mode_color):
        particle.set_color(track_follow_mode_color)
        pheromone_to_follow = compare_pheromones(get_track(particle))
        particle.move_to(pheromone_to_follow)
        came_from = invert_dir(pheromone_to_follow)
        particle.way_home_list.append(came_from)


# If home, go back in search-mode
def reset_if_home(particle):
    if (particle.coords == home):
        particle.set_color(search_mode_color)
        # Reset way home list
        particle.way_home_list = []
        # Restore life span
        particle.set_alpha(1)


# If track die, go back in search-mode
def track_dies(particle):
    if (particle.get_color() == track_follow_mode_color and particle.check_on_marker() == False):
        particle.set_color(search_mode_color)


# Get all surrounding pheromones and make a dictionary
def get_track(particle):
    pheromone_dict = {}
    for dir in DIRECTIONS:
        if (particle.marker_in(dir) == True and particle.get_marker_in(dir).get_color() != base_color and particle.get_marker_in(dir).get_color() != search_track_color):
            pheromone_dict.update(
                {dir: [particle.get_marker_in(dir).layer]})
        if (particle.way_home_list != None):
            pheromone_dict.pop(particle.way_home_list[-1], None)
    return pheromone_dict


def compare_pheromones(pheromones_dict):
    # If the dictionary is empty go in a random direction
    if (len(pheromones_dict) == 0):
        return random.choice(DIRECTIONS)
    else:
        # Filter all entries which have max layer
        max_layer = max([value[0] for direction, value in pheromones_dict.items()])
        # Filter all directions which have max layer
        resulting_directions  = [direction for direction, value in pheromones_dict.items() if value[0] == max_layer]
        return random.choice(resulting_directions)


# Invert dir
def invert_dir(dir):
    if dir >= 3:
        return dir - 3
    else:
        return dir + 3


# Making a plot
def plot(rounds, deads):
    plt.plot(rounds, deads)
    plt.xlabel("rounds")
    plt.ylabel("dead ants")
    # plt.title("Rounds: ", str(rounds[-1]), "Deads:", str(deads[-1]))
    plt.show()

def filter_search_track (particle):
    selected_directions = []
    for dir in selected_directions:
        if (particle.get_marker_in(dir).get_color() != search_track_color):
            selected_directions.append(dir)
    if (len(selected_directions)==0):
        selected_directions = DIRECTIONS
    return selected_directions

# Start
###########################################################################################################################################################################

rounds = []
deads = []


def solution(world):
    global dead_count

#    start_dead_count(world)
    respawn(world)
    rounds.append(world.get_actual_round())
#    deads.append(dead_count)

    for marker in world.get_marker_list():
        evaporate(marker)
        delete_track(marker, world)

    for particle in world.get_particle_list():
        decrease_life_span(particle)
        kill_ant(particle, world)
        search_food_mode(particle)
        home_mode(particle, world)

        # If in home-mode, go home and lay track
        if (particle.get_color() == home_mode_color):
            delete_search_track(particle, world)
            lay_track(particle)
            go_home(particle)

        follow_mode(particle)
        reset_if_home(particle)
        track_dies(particle)

    # If all food is collected, success
    if (len(world.get_tiles_list()) == 0):
        world.success_termination()
        print("Rounds:", rounds[-1])
#        print("Deads:", deads[-1])
#        plot(rounds, deads)



