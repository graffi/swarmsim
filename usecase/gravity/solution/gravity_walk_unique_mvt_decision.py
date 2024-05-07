# OBJECTIVES
'''
1.	To build the tower (Gravity random walk – code)
2.	To re-define the movements of the agents using the distance for each individual agent.

To achieve this:

            The agents to calculate  its own distance, in the ratio form with the formula:
                ratio = distance / maximum distance

Where:
            The distance is the distance for individual agent and the maximum distance is the maximum height of the tower
            To implement the logic such that the agents  movement here is such that all agents will decide to move ( for example it can climb up by  25%, and then swing horizontally (50%) east or west and fall 25%.

ROADMAP TO ACHIEVE THIS OBJECTIVES:

Step 1: Building the tower. Normal Gravity walker random tower.
        ##The normal regular logic for this.

Step 2: Agents to climb (as defined in the Logic, the agents with ratio <25% )
        ##This is okay, as we are implementing the regular gravity logic of upward/ climbing movement. Just fine -tuning the ratio definition movement for all agents with ratio of <25%.

Step 3: Agents to swing
        ##The objective here is to make agents move horizontally swinging EAST or WEST
        ##To achieve this, we first get the location of the first swinging agent based on the ration definition
        ## After getting the first swinging agent, we inject a scan_neighborhood function to scan any neighbouring agents.
        ##Here we implement some conditions to make the top most climbing agent to fall- as other climbing agents follow, and stop at the same horizontal line as the first swinging agents. Hence having a structure like this;

 Step 4: Falling of agents
        #Here, we focus on the falling of agents. Meaning we scan the neighbourhood, and if there’s no any other available agent or obstacle, the agent is instructed to move downwards by (-1 N. E) under the influence of gravity, and the other agents to follow, hence forming a structure as shown below.
'''

import math
import random


def solution(world):
    min_agent_height = float('inf')
    max_agent_height = 0
    stop_if_tower_built = False
    tower_has_been_built = False

    # Build the tower
    for agent in world.get_agent_list():
        if agent.coordinates[1] > max_agent_height:
            max_agent_height = agent.coordinates[1]
        if agent.coordinates[1] < min_agent_height:
            min_agent_height = agent.coordinates[1]

    # Tower height calculation
    tower_height = max_agent_height - min_agent_height + 1

    # Check if the tower has been built
    if tower_height == len(world.get_agent_list()):
        tower_has_been_built = True

    # If tower has not been built yet, continue building
    if not tower_has_been_built:
        for agent in world.get_agent_list():
            if agent.coordinates[1] > max_agent_height:
                max_agent_height = agent.coordinates[1]
            if agent.coordinates[1] < min_agent_height:
                min_agent_height = agent.coordinates[1]

            dir_NE = (0.5, 1, 0)
            dir_NW = (-0.5, 1, 0)
            dir_SE = (0.5, -1, 0)
            dir_SW = (-0.5, -1, 0)
            dir_W = (-1, 0, 0)
            dir_E = (1, 0, 0)
            dir_stand = (0, 0, 0)

            item_in_E = agent.item_in(dir_E)
            item_in_W = agent.item_in(dir_W)
            item_in_SE = agent.item_in(dir_SE)
            item_in_SW = agent.item_in(dir_SW)
            item_in_NE = agent.item_in(dir_NE)
            item_in_NW = agent.item_in(dir_NW)

            agent_in_E = agent.agent_in(dir_E)
            agent_in_W = agent.agent_in(dir_W)
            agent_in_SE = agent.agent_in(dir_SE)
            agent_in_SW = agent.agent_in(dir_SW)
            agent_in_NE = agent.agent_in(dir_NE)
            agent_in_NW = agent.agent_in(dir_NW)

            free_W = not agent_in_W and not item_in_W
            free_E = not agent_in_E and not item_in_E
            free_NW = not agent_in_NW and not item_in_NW
            free_NE = not agent_in_NE and not item_in_NE
            free_SW = not agent_in_SW and not item_in_SW
            free_SE = not agent_in_SE and not item_in_SE

            dir_not_set_yet = (0, 0, 1)
            next_direction = dir_not_set_yet  # characterizes an invalid state, will be changed later

            # CASE Begin: FALLING Start  - free_SW and free_SE -   Check whether Agent needs to fall
            if free_SW and free_SE:
                y_position = agent.coordinates[1]

                # We know already that this agent must fall, it will be in a zig (SE) - zag (SW) pattern, depending on the height (y - coordinate)
                if (y_position % 2) == 0:
                    next_direction = dir_SW
                else:
                    next_direction = dir_SE
            # CASE End: FALLING End  - free_SW and free_SE -   Check whether Agent needs to fall

            # CASE Begin: Agent is alone on the floor - Walk Left - Right -  itemin_SE and itemin_SW  - and nothing is above it
            # Walk to left of right if possible, otherwise stand
            if not agent_in_W and not agent_in_E:

                if next_direction == dir_not_set_yet and item_in_SE and item_in_SW:
                    # Move left or right
                    rand_direction = random.choice((dir_W, dir_E))
                    next_direction = dir_stand

                    if rand_direction == dir_W and free_W and not agent_in_NE:
                        next_direction = rand_direction
                    if rand_direction == dir_E and free_E and not agent_in_NW:
                        next_direction = rand_direction

                if next_direction == dir_not_set_yet and agent_in_SE and item_in_SW and not agent_in_NW:
                    # Move left or right
                    rand_direction = random.choice((dir_stand, dir_E))
                    next_direction = dir_stand
                    if rand_direction == dir_E and free_E:
                        next_direction = rand_direction

                if next_direction == dir_not_set_yet and agent_in_SW and item_in_SE and not agent_in_NE:
                    # Move left or right
                    rand_direction = random.choice((dir_stand, dir_W))
                    next_direction = dir_stand
                    if rand_direction == dir_W and free_W:
                        next_direction = rand_direction

                if next_direction == dir_not_set_yet and free_SE and item_in_SW and not agent_in_NE and free_W:
                    # Move left
                    next_direction = dir_W

                if next_direction == dir_not_set_yet and free_SW and item_in_SE and not agent_in_NW and free_E:
                    # Move left
                    next_direction = dir_E
            # CASE End: Agent is on the floor - Walk Left -Right - itemin_SE and itemin_SW  - and nothing is above it

            # CASE Begin: Agent is on 2 agents - agentin_SW and agentin_SE - and carries an agent in NE, walk E
            if next_direction == dir_not_set_yet and agent_in_SW and agent_in_SE and free_E and agent_in_NE and not agent_in_NW:
                next_direction = dir_E  # free_E is True
            # CASE End: Agent is on 2 agents - agentin_SW and agentin_SE - and carries an agent in NE, walk E
            # Why not also case for W?
            if next_direction == dir_not_set_yet and agent_in_SW and agent_in_SE and free_W and agent_in_NW and not agent_in_NE:
                next_direction = dir_W
            # CASE End: Agent is on 2 agents - agentin_SW and agentin_SE - and carries an agent in NE, walk E

            if next_direction == dir_not_set_yet and free_NE and free_E and agent_in_SE and not agent_in_NW:
                next_direction = dir_E  # free_E is True

            # CASE Begin: CLIMBING - Try climb NW, then try climb NE. Must be free, and carrying nothing
            # climb on agent in W if possible AND no other agent is on top of you
            if next_direction == dir_not_set_yet and (agent_in_W and free_NW) and (
                    (not agent_in_NE) or (agent_in_NE and agent_in_E)):
                next_direction = dir_NW

            # climb on agent in E if possible AND no other agent is on top of you
            if next_direction == dir_not_set_yet and (agent_in_E and free_NE) and (
                    (not agent_in_NW) or (agent_in_NW and agent_in_W)):
                next_direction = dir_NE
            # CASE Begin: CLIMBING - Try climb NW, then try climb NE. Must be free, and

            # CASE Begin: TOWER SHIFT LEFT AND RIGHT
            # if standing only on agent in SE, check whether we need to move to E
            if next_direction == dir_not_set_yet and agent_in_SE and not agent_in_SW and free_E and not agent_in_NW:
                next_direction = dir_E

            if next_direction == dir_not_set_yet and agent_in_SW and not agent_in_SE and free_W and not agent_in_NE:
                y_position = agent.coordinates[1]
                next_direction = dir_W
            # CASE END: TOWER SHIFT LEFT AND RIGHT

            # CASE DEFAULT: If no direction selected, do not move
            if next_direction == dir_not_set_yet:
                next_direction = dir_stand

            # FINAL MOVE: if the agent is not falling currently, walk in the selected direction
            if next_direction != dir_not_set_yet:
                agent.move_to(next_direction)

        # Update tower height after building
        tower_height = max_agent_height - min_agent_height + 1

    # If tower is built, apply custom agent behaviors
    else:
        distance_ratios = {}
        max_distance = max_agent_height

        # Step 2: Calculate Distance Ratio for each agent
        for agent in world.get_agent_list():
            distance = agent.coordinates[1]
            distance_ratio = calculate_distance_ratio(distance, max_distance)
            distance_ratios[agent] = distance_ratio

        # Step 2: Determine Movement Decisions
        movement_decisions = {}

        for agent, distance_ratio in distance_ratios.items():
            # Determining the movement decisions based on distance ratio
            if distance_ratio <= 0.25:
                decision = "climb"
                # color 1, Dark color
                agent.set_color((0.0, 0.2, 0.2, 1.0))

            elif 0.25 < distance_ratio <= 0.75:
                decision = "swing"
                # color 2, greenish color
                agent.set_color((0.0, 0.6, 0.0, 1.0))

            else:
                decision = "fall"
                # color 3, the shinny yellow color
                agent.set_color((0.8, 0.8, 0.0, 1.0))

            movement_decisions[agent] = decision

        # Step 3: Implement Movement Functions
        # Step 3: Implement Movement Functions
        for agent, decision in movement_decisions.items():
            # Movement based on decision
            if decision == "climb":
                climb(agent)
            elif decision == "swing":
                swing(agent, distance_ratios)  # Pass the  parameter here
            elif decision == "fall":
                fall(agent, distance_ratios)
        # Debugging
        print("Individual Distance of Agents:")
        for agent, distance_ratio in distance_ratios.items():
            print(f"Agent {agent.number}: Distance Ratio = {distance_ratio}")

        print("\nDecisions of Individual Agents:")
        for agent, decision in movement_decisions.items():
            print(f"Agent {agent.number}: Decision = {decision}")

    # For next step: define the goal of the simulation, e.g. to build a tower of 6 agents and then terminate the simulation
    print("\nRound: ", world.get_actual_round(), "MaxHeight: ", max_agent_height, "Minheight: ", min_agent_height,
          "Towerheight: ", tower_height, "  Number of Agents", world.get_amount_of_agents())

    if tower_has_been_built and stop_if_tower_built:
        world.set_successful_end()


# The function to calculate the distance ratio for an agent
def calculate_distance_ratio(distance, max_distance):
    if max_distance == 0:
        return 0  # to avoid division by zero
    ratio = distance / max_distance
    return max(min(ratio, 1), 0)  # To ensure that the ratio the ratio is between 0 and 1


def climb(agent):

    #Usual code for tower building
    dir_NE = (0.5, 1, 0)
    dir_NW = (-0.5, 1, 0)
    dir_SE = (0.5, -1, 0)
    dir_SW = (-0.5, -1, 0)
    dir_W = (-1, 0, 0)
    dir_E = (1, 0, 0)
    dir_stand = (0, 0, 0)

    item_in_E = agent.item_in(dir_E)
    item_in_W = agent.item_in(dir_W)
    item_in_SE = agent.item_in(dir_SE)
    item_in_SW = agent.item_in(dir_SW)
    item_in_NE = agent.item_in(dir_NE)
    item_in_NW = agent.item_in(dir_NW)

    agent_in_E = agent.agent_in(dir_E)
    agent_in_W = agent.agent_in(dir_W)
    agent_in_SE = agent.agent_in(dir_SE)
    agent_in_SW = agent.agent_in(dir_SW)
    agent_in_NE = agent.agent_in(dir_NE)
    agent_in_NW = agent.agent_in(dir_NW)

    free_W = not agent_in_W and not item_in_W
    free_E = not agent_in_E and not item_in_E
    free_NW = not agent_in_NW and not item_in_NW
    free_NE = not agent_in_NE and not item_in_NE
    free_SW = not agent_in_SW and not item_in_SW
    free_SE = not agent_in_SE and not item_in_SE

    dir_not_set_yet = (0, 0, 1)
    next_direction = dir_not_set_yet  # characterizes an invalid state, will be changed later

    # CASE Begin: FALLING Start  - free_SW and free_SE -   Check whether Agent needs to fall
    if free_SW and free_SE:
        y_position = agent.coordinates[1]

        # We know already that this agent must fall, it will be in a zig (SE) - zag (SW) pattern, depending on the height (y - coordinate)
        if (y_position % 2) == 0:
            next_direction = dir_SW
        else:
            next_direction = dir_SE
    # CASE End: FALLING End  - free_SW and free_SE -   Check whether Agent needs to fall

    # CASE Begin: Agent is alone on the floor - Walk Left - Right -  itemin_SE and itemin_SW  - and nothing is above it
    # Walk to left of right if possible, otherwise stand
    if not agent_in_W and not agent_in_E:

        if next_direction == dir_not_set_yet and item_in_SE and item_in_SW:
            # Move left or right
            rand_direction = random.choice((dir_W, dir_E))
            next_direction = dir_stand

            if rand_direction == dir_W and free_W and not agent_in_NE:
                next_direction = rand_direction
            if rand_direction == dir_E and free_E and not agent_in_NW:
                next_direction = rand_direction

        if next_direction == dir_not_set_yet and agent_in_SE and item_in_SW and not agent_in_NW:
            # Move left or right
            rand_direction = random.choice((dir_stand, dir_E))
            next_direction = dir_stand
            if rand_direction == dir_E and free_E:
                next_direction = rand_direction

        if next_direction == dir_not_set_yet and agent_in_SW and item_in_SE and not agent_in_NE:
            # Move left or right
            rand_direction = random.choice((dir_stand, dir_W))
            next_direction = dir_stand
            if rand_direction == dir_W and free_W:
                next_direction = rand_direction

        if next_direction == dir_not_set_yet and free_SE and item_in_SW and not agent_in_NE and free_W:
            # Move left
            next_direction = dir_W

        if next_direction == dir_not_set_yet and free_SW and item_in_SE and not agent_in_NW and free_E:
            # Move left
            next_direction = dir_E
    # CASE End: Agent is on the floor - Walk Left -Right - itemin_SE and itemin_SW  - and nothing is above it

    # CASE Begin: Agent is on 2 agents - agentin_SW and agentin_SE - and carries an agent in NE, walk E
    if next_direction == dir_not_set_yet and agent_in_SW and agent_in_SE and free_E and agent_in_NE and not agent_in_NW:
        next_direction = dir_E  # free_E is True
    # CASE End: Agent is on 2 agents - agentin_SW and agentin_SE - and carries an agent in NE, walk E
    # Why not also case for W?
    if next_direction == dir_not_set_yet and agent_in_SW and agent_in_SE and free_W and agent_in_NW and not agent_in_NE:
        next_direction = dir_W
    # CASE End: Agent is on 2 agents - agentin_SW and agentin_SE - and carries an agent in NE, walk E

    if next_direction == dir_not_set_yet and free_NE and free_E and agent_in_SE and not agent_in_NW:
        next_direction = dir_E  # free_E is True

    # CASE Begin: CLIMBING - Try climb NW, then try climb NE. Must be free, and carrying nothing
    # climb on agent in W if possible AND no other agent is on top of you
    if next_direction == dir_not_set_yet and (agent_in_W and free_NW) and (
            (not agent_in_NE) or (agent_in_NE and agent_in_E)):
        next_direction = dir_NW

    # climb on agent in E if possible AND no other agent is on top of you
    if next_direction == dir_not_set_yet and (agent_in_E and free_NE) and (
            (not agent_in_NW) or (agent_in_NW and agent_in_W)):
        next_direction = dir_NE
    # CASE Begin: CLIMBING - Try climb NW, then try climb NE. Must be free, and

    # CASE Begin: TOWER SHIFT LEFT AND RIGHT
    # if standing only on agent in SE, check whether we need to move to E
    if next_direction == dir_not_set_yet and agent_in_SE and not agent_in_SW and free_E and not agent_in_NW:
        next_direction = dir_E

    if next_direction == dir_not_set_yet and agent_in_SW and not agent_in_SE and free_W and not agent_in_NE:
        y_position = agent.coordinates[1]
        next_direction = dir_W
    # CASE END: TOWER SHIFT LEFT AND RIGHT

    # CASE DEFAULT: If no direction selected, do not move
    if next_direction == dir_not_set_yet:
        next_direction = dir_stand

    # FINAL MOVE: if the agent is not falling currently, walk in the selected direction
    if next_direction != dir_not_set_yet:
        agent.move_to(next_direction)

    # Update tower height after building

# Move the agent diagonally towards the bridge's end
# Move the agent down (falling)
def fall(agent, distance_ratios):
    # Find the coordinates of the last swinging agent
    last_swinging_agent_coordinates = find_last_swinging_agent(distance_ratios)

    if last_swinging_agent_coordinates is None:
        print("No swinging agent found")
        return  # No swinging agent found

    # Check if the agent is not at the same horizontal line as the last swinging agent, fall towards that line
    if agent.coordinates[1] != last_swinging_agent_coordinates[1]:
        if agent.coordinates[1] > last_swinging_agent_coordinates[1]:
            print("Agent is above the horizontal line, moving South")
            # If agent is above the horizontal line, move South
            agent.move_to((agent.coordinates[0], agent.coordinates[1] - 1, agent.coordinates[2]))  # Move downwards
        else:
            print("Agent is below the horizontal line, moving North")
            # If agent is below the horizontal line, move North
            agent.move_to((agent.coordinates[0], agent.coordinates[1] + 1, agent.coordinates[2]))  # Move upwards
    else:
        # Once the agent is at the same horizontal line, do nothing
        print("Agent is at the same horizontal line as the last swinging agent")
        pass


# Find the coordinates of the last swinging agent
def find_last_swinging_agent(distance_ratios):
    last_swinging_agent_coordinates = None
    max_distance_ratio = -1
    # Iterate through the agents sorted by their distance ratios
    sorted_agents = sorted(distance_ratios.items(), key=lambda x: x[1])
    for agent, distance_ratio in sorted_agents:
        # Check if the agent is swinging
        if distance_ratio > max_distance_ratio:
            max_distance_ratio = distance_ratio
            last_swinging_agent_coordinates = agent.coordinates
            # Prints for debugging
    print("Last swinging agent coordinates:", last_swinging_agent_coordinates)
    return last_swinging_agent_coordinates


# The agent to swing (horizontal movement)
def swing(agent, distance_ratios):
    # Define directions for swinging
    dir_NE = (0.5, 1, 0)
    dir_NW = (-0.5, 1, 0)
    dir_SE = (0.5, -1, 0)
    dir_SW = (-0.5, -1, 0)
    dir_E = (1, 0, 0)
    dir_W = (-1, 0, 0)

    # Define scan directions
    scan_dir_NE = (0, 1, 0)
    scan_dir_NW = (0, 1, 0)
    scan_dir_SE = (0, -1, 0)
    scan_dir_SW = (0, -1, 0)
    scan_dir_W = (-1, 0, 0)
    scan_dir_E = (1, 0, 0)

    # Find the coordinates of the first swinging agent
    first_swinging_agent, first_swinging_agent_coordinates = find_first_swinging_agent(distance_ratios)

    if first_swinging_agent_coordinates is None:
        print("No first swinging agent found!")
        return  # No swinging agent found

    print("First swinging agent coordinates:", first_swinging_agent_coordinates)

    # Check for obstacles in scan directions
    obstacle_NE = agent.item_in(scan_dir_NE) or agent.agent_in(scan_dir_NE)
    obstacle_NW = agent.item_in(scan_dir_NW) or agent.agent_in(scan_dir_NW)
    obstacle_SE = agent.item_in(scan_dir_SE) or agent.agent_in(scan_dir_SE)
    obstacle_SW = agent.item_in(scan_dir_SW) or agent.agent_in(scan_dir_SW)
    obstacle_W = agent.item_in(scan_dir_W) or agent.agent_in(scan_dir_W)
    obstacle_E = agent.item_in(scan_dir_E) or agent.agent_in(scan_dir_E)

    print("Obstacle NE:", obstacle_NE)
    print("Obstacle NW:", obstacle_NW)
    print("Obstacle SE:", obstacle_SE)
    print("Obstacle SW:", obstacle_SW)
    print("Obstacle W:", obstacle_W)
    print("Obstacle E:", obstacle_E)

    # Move based on obstacles
    if obstacle_NE or obstacle_NW or obstacle_SE or obstacle_SW:
        print("Obstacle detected in adjacent directions, standing still.")
        # Stand still
        agent.move_to((0, 0, 0))
    elif obstacle_W:
        print("Obstacle detected in the West direction, moving to East.")
        # Move to East
        agent.move_to(dir_E)
    elif obstacle_E:
        print("Obstacle detected in the East direction, moving to West.")
        # Move to West
        agent.move_to(dir_W)
    else:
        # Move towards the X coordinate of the first swinging agent
        if agent.coordinates[0] < first_swinging_agent_coordinates[0]:
            print("Moving towards the X coordinate of the first swinging agent (East).")
            # Move towards East
            agent.move_to(dir_E)
        elif agent.coordinates[0] > first_swinging_agent_coordinates[0]:
            print("Moving towards the X coordinate of the first swinging agent (West).")
            # Move towards West
            agent.move_to(dir_W)


# the first swinging agent based on distance ratios
def find_first_swinging_agent(distance_ratios):
    first_swinging_agent = None
    for agent, ratio in distance_ratios.items():
        # Check if the agent is not at the top and there are no agents above it
        if ratio < 1 and not agent.agent_in((0, 1, 0)):
            first_swinging_agent = agent
            # Print for debugging purposes
            print("The very immediate Swinging agent:", agent.number, "Coordinates:", agent.coordinates)
            break
    if first_swinging_agent:
        return first_swinging_agent, first_swinging_agent.coordinates
    else:
        return None, None
