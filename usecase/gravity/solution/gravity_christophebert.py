import random

dirNE = (0.5, 1, 0)
dirNW = (-0.5, 1, 0)
dirSE = (0.5, -1, 0)
dirSW = (-0.5, -1, 0)
dirW = (-1, 0, 0)
dirE = (1, 0, 0)
dirStand = (0, 0, 0)
dirNotSetYet = (0, 0, 1)

directions = [dirNE, dirE, dirSE, dirSW, dirW, dirNW]

color_default = (0.7, 0.2, 0.2, 1.0)
color_fixed = (0.5, 0.0, 0.5, 1.0)
color_signal_1 = (0.5, 0.5, 0.0, 1.0)
color_signal_neg_1 = (0.7, 0.0, 0.0, 1.0)
color_on_top = (0.0, 0.5, 0.5, 1.0)

falling = 999


def solution(world):

    if world.get_actual_round() % 1 == 0:
        for agent in world.get_agent_list():

            freeW = not agent.agent_in(dirW) and not agent.item_in(dirW)
            freeE = not agent.agent_in(dirE) and not agent.item_in(dirE)
            freeNW = not agent.agent_in(dirNW) and not agent.item_in(dirNW)
            freeNE = not agent.agent_in(dirNE) and not agent.item_in(dirNE)
            freeSW = not agent.agent_in(dirSW) and not agent.item_in(dirSW)
            freeSE = not agent.agent_in(dirSE) and not agent.item_in(dirSE)
            nextdirection = dirNotSetYet

            if not hasattr(agent, 'planned_direction'):
                agent.planned_direction = random.choice([dirW, dirE])

            # initializing agent memory to prevent exceptions from checking none existent values
            if world.get_actual_round() == 1:
                agent.write_memory_with("agent_number", agent.number)
                agent.write_memory_with("adjust", 0)
                agent.write_memory_with("foot", -1)
                agent.write_memory_with("ready", False)
                agent.write_memory_with("timer", 0)
                agent.write_memory_with("ground", 999)
                agent.write_memory_with("fixed", False)
                agent.write_memory_with("signal", 0)
                agent.write_memory_with("state", 0)

            planned_direction = agent.planned_direction
            agent.weight = find_weight(agent)
            agent.write_memory_with("planned_direction", planned_direction)
            agent.write_memory_with("weight", agent.weight)

            if world.get_actual_round() > 1:
                agent.write_memory_with("ground", find_ground(agent))

            # writing and passing
            if (freeSE and agent.item_in(dirSW)) or agent.agent_in(dirSE) and agent.get_agent_in(dirSE).read_memory_with("east_edge") or agent.agent_in(dirSW) and agent.get_agent_in(dirSW).read_memory_with("east_edge"):
                # agent has reached East Edge
                agent.write_memory_with("east_edge", True)
            if (freeSW and agent.item_in(dirSE)) or agent.agent_in(dirSE) and agent.get_agent_in(dirSE).read_memory_with("west_edge") or agent.agent_in(dirSW) and agent.get_agent_in(dirSW).read_memory_with("west_edge"):
                # agent has reached West Edge
                agent.write_memory_with("west_edge", True)

            if agent.read_memory_with("ground") >= falling:
                if agent.read_memory_with("timer") >= 60:
                    agent.write_memory_with("fixed", False)
                    agent.write_memory_with("timer", 0)
                agent.write_memory_with("timer", agent.read_memory_with("timer") + 1)
            else:
                agent.write_memory_with("timer", 0)

            fixed_diagonal(agent)
            if agent.read_memory_with("fixed"):
                if agent.read_memory_with("adjust") != 0:
                    nextdirection = alignment(agent)
                else:
                    nextdirection = directed_tentacle(agent)

            # change color based on current phase/state
            agent.set_color(color_default)
            if agent.read_memory_with("fixed"):
                agent.set_color(color_fixed)
            if agent.read_memory_with("signal") == 1:
                agent.set_color(color_signal_1)
            if agent.read_memory_with("signal") == -1:
                agent.set_color(color_signal_neg_1)
            if is_on_top(agent):
                agent.set_color(color_on_top)

            if not agent.read_memory_with("fixed"):
                # CASE Begin: FALLING Start  - freeSW and freeSE -   Check whether Agent needs to fall
                if freeSW and freeSE:
                    yposition = agent.coordinates[1]

                    # We know already that this agent must fall, it will be in a zig (SE) - zag (SW) pattern, depending on the height (y - coordinate)
                    if (yposition % 2) == 0:
                        nextdirection = dirSW
                    else:
                        nextdirection = dirSE
                # CASE End: FALLING End  - freeSW and freeSE -   Check whether Agent needs to fall

                # CASE Begin: Agent is alone on the floor - Walk Left - Right -  agent.item_in(dirSE) and agent.item_in(dirSW)  - and nothing is above it
                # Walk to left of right if possible, otherwise stand
                if not agent.agent_in(dirW) and not agent.agent_in(dirE):

                    if nextdirection == dirNotSetYet and agent.item_in(dirSE) and agent.item_in(dirSW):
                        # Move left or right
                        randdirection = planned_direction
                        nextdirection = dirStand

                        if randdirection == dirW and freeW and not agent.agent_in(dirNE):
                            nextdirection = planned_direction
                        if randdirection == dirE and freeE and not agent.agent_in(dirNW):
                            nextdirection = planned_direction

                    if nextdirection == dirNotSetYet and freeSE and agent.item_in(dirSW) and not agent.agent_in(dirNE) and freeW:
                        nextdirection = dirW
                        agent.planned_direction = dirW

                    if nextdirection == dirNotSetYet and freeSW and agent.item_in(dirSE) and not agent.agent_in(dirNW) and freeE:
                        nextdirection = dirE
                        agent.planned_direction = dirE
                # CASE End: Agent is on the floor - Walk Left -Right - agent.item_in(dirSE) and agent.item_in(dirSW)  - and nothing is above it

                if agent.planned_direction == dirW and agent.agent_in(dirW) and agent.get_agent_in(dirW).read_memory_with("fixed"):
                    nextdirection = dirE

                elif agent.planned_direction == dirE and agent.agent_in(dirE) and agent.get_agent_in(dirE).read_memory_with("fixed"):
                    nextdirection = dirW

                # CASE Begin: Agent is on 2 agents - agent.agent_in(dirSW) and agent.agent_in(dirSE) - and carries an agent in NE, walk E
                if nextdirection == dirNotSetYet and agent.agent_in(dirSW) and agent.agent_in(dirSE) and freeE and agent.agent_in(dirNE) and not agent.agent_in(dirNW):
                    nextdirection = dirE
                    agent.planned_direction = dirE
                # CASE End: Agent is on 2 agents - agent.agent_in(dirSW) and agent.agent_in(dirSE) - and carries an agent in NE, walk E

                # CASE Begin: Agent is on 2 agents - agent.agent_in(dirSW) and agent.agent_in(dirSE) - and carries an agent in NW, walk W
                if nextdirection == dirNotSetYet and agent.agent_in(dirSW) and agent.agent_in(dirSE) and freeW and agent.agent_in(dirNW) and not agent.agent_in(dirNE):
                    nextdirection = dirW
                    agent.planned_direction = dirW
                # CASE End: Agent is on 2 agents - agent.agent_in(dirSW) and agent.agent_in(dirSE) - and carries an agent in NW, walk W

                if nextdirection == dirNotSetYet and freeNE and freeNW and freeE and agent.agent_in(dirSE):
                    nextdirection = dirE
                    agent.planned_direction = dirE

                # CASE Begin: CLIMBING - Try climb NW, then try climb NE. Must be free, and carrying nothing
                # climb on agent in W if possible AND no other agent is on top of you
                if nextdirection == dirNotSetYet and agent.agent_in(dirW) and freeNW and freeNE:
                    nextdirection = dirNW
                # climb on agent in E if possible AND no other agent is on top of you
                if nextdirection == dirNotSetYet and agent.agent_in(dirE) and freeNE and freeNW:
                    nextdirection = dirNE
                # CASE End: CLIMBING - Try climb NW, then try climb NE. Must be free, and carrying nothing

                # CASE Begin: TOWER SHIFT LEFT AND RIGHT
                # if standing only on agent in SE, check whether we need to move to E
                if (nextdirection == dirNotSetYet or nextdirection == dirStand) and agent.agent_in(dirSE) and not agent.agent_in(dirSW) and freeE and not agent.agent_in(dirNW):
                    nextdirection = dirE
                    agent.planned_direction = dirE
                    dirWalkPlan = dirE

                if (nextdirection == dirNotSetYet or nextdirection == dirStand) and agent.agent_in(dirSW) and not agent.agent_in(dirSE) and freeW and not agent.agent_in(dirNE):
                    yposition = agent.coordinates[1]
                    nextdirection = dirW
                    agent.planned_direction = dirW
                    dirWalkPlan = dirW
                # CASE END: TOWER SHIFT LEFT AND RIGHT

                # CASE DEFAULT: If no direction selected, do not move
                if nextdirection == dirNotSetYet:
                    nextdirection = dirStand

            # FINAL MOVE: if the agent is not falling currently, walk in the selected direction
            if nextdirection != dirNotSetYet:
                agent.move_to(nextdirection)

##################################################

def fixed_diagonal(agent):
    freeSW = not agent.agent_in(dirSW) and not agent.item_in(dirSW)
    freeSE = not agent.agent_in(dirSE) and not agent.item_in(dirSE)

    rightUp = dirNE
    leftDown = dirSW
    rightDown = dirSE
    freeLeftDown = freeSW

    if agent.planned_direction == dirE:
        rightUp = dirNW
        leftDown = dirSE
        rightDown = dirSW
        freeLeftDown = freeSE

##################################################

    if agent.read_memory_with("fixed"):
        if abs(agent.read_memory_with("state")) >= 9 and ((agent.agent_in(leftDown) and agent.get_agent_in(leftDown).read_memory_with("fixed")) or (agent.item_in(leftDown) and (agent.agent_in(rightUp) and not agent.get_agent_in(rightUp).read_memory_with("fixed")))) and ((agent.weight == 1 and abs(agent.read_memory_with("state") + agent.read_memory_with("adjust")) >= 11) or (agent.agent_in(rightUp) and not agent.get_agent_in(rightUp).read_memory_with("fixed"))):
            agent.write_memory_with("fixed", False)
            agent.write_memory_with("ready", False)
            agent.write_memory_with("state", 0)
            agent.write_memory_with("signal", 0)
            agent.write_memory_with("adjust", 0)
            log_agent_read(agent)
            log_memory_write(agent)
    elif agent.read_memory_with("east_edge") and agent.read_memory_with("west_edge") and freeLeftDown and (agent.item_in(rightDown)
         or (agent.agent_in(rightDown) and agent.get_agent_in(rightDown).read_memory_with("fixed")) and agent.get_agent_in(rightDown).read_memory_with("state") == 0):
        agent.write_memory_with("fixed", True)
        log_memory_write(agent)

##################################################

def directed_tentacle(agent):
    freeW = not agent.agent_in(dirW) and not agent.item_in(dirW)
    freeE = not agent.agent_in(dirE) and not agent.item_in(dirE)
    freeNW = not agent.agent_in(dirNW) and not agent.item_in(dirNW)
    freeNE = not agent.agent_in(dirNE) and not agent.item_in(dirNE)
    freeSW = not agent.agent_in(dirSW) and not agent.item_in(dirSW)
    freeSE = not agent.agent_in(dirSE) and not agent.item_in(dirSE)
    free_directions = [freeNE, freeE, freeSE, freeSW, freeW, freeNW]

    indexRightUp = (0 + agent.read_memory_with("state")) % 6
    indexRight = (1 + agent.read_memory_with("state")) % 6
    indexRightDown = (2 + agent.read_memory_with("state")) % 6
    indexLeftDown = (3 + agent.read_memory_with("state")) % 6
    indexLeft = (4 + agent.read_memory_with("state")) % 6
    indexLeftUp = (5 + agent.read_memory_with("state")) % 6

    left = dirW
    leftUp = dirNW
    rightDown = dirSE
    leftDown = dirSW

    if agent.planned_direction == dirE:
        copy = indexRightUp
        indexRightUp = indexLeftUp
        indexLeftUp = copy

        copy = indexRight
        indexRight = indexLeft
        indexLeft = copy

        copy = indexRightDown
        indexRightDown = indexLeftDown
        indexLeftDown = copy

        left = dirE
        leftUp = dirNE
        rightDown = dirSW
        leftDown = dirSE

##################################################

    if agent.weight == 1 or 2:
        # normal mode to search islands
        if agent.read_memory_with("signal") == 0:

            if agent.read_memory_with("state") in [-4, 4]:
                agent.write_memory_with("signal", -1)

            # move the diagonal tower to a new direction
            elif free_directions[indexLeftDown] and is_agent_fixed(agent, indexRightDown) and (
                    is_agent_fixed(agent, indexLeft) or (free_directions[indexLeft] and agent.weight == 1)):
                log_agent_read(agent)
                return directions[indexLeftDown]

            # rotate the direction of the current agent
            elif is_agent_fixed(agent, indexRight) and (
                    (free_directions[indexLeftDown] and agent.get_agent_in(directions[indexRight]).weight == 1) or
                    abs(agent.read_memory_with("state") - agent.get_agent_in(directions[indexRight]).read_memory_with("state")) <= 2):
                log_memory_write(agent)

                if agent.planned_direction == dirW:
                    agent.write_memory_with("state", agent.read_memory_with("state") - 1)
                else:
                    agent.write_memory_with("state", agent.read_memory_with("state") + 1)

            # tentacle has found a new island
            elif -6 <= agent.read_memory_with("state") <= 6 and ((agent.item_in(leftDown) and not agent.agent_in(left)) or update_foot(agent)):
                if agent.item_in(leftDown) and not agent.agent_in(left):
                    agent.write_memory_with("foot", 1)
                log_agent_read(agent)
                log_memory_write(agent)
                agent.write_memory_with("signal", 1)
                if agent.agent_in(leftUp):
                    agent.write_memory_with("adjust", agent.get_agent_in(leftUp).read_memory_with("adjust") + 1)
                elif agent.agent_in(leftDown):
                    agent.write_memory_with("adjust", -1)
                elif agent.agent_in(left):
                    agent.write_memory_with("adjust", agent.get_agent_in(left).read_memory_with("adjust"))

            # tentacle move return to the start of old island
            elif (is_on_top(agent) and agent.item_in(directions[indexLeftDown]) and
                  not agent.item_in(leftDown) and not agent.item_in(rightDown)) or (
                    is_agent_signal(agent, indexLeft, -1) or
                    is_agent_signal(agent, indexLeftUp, -1) or
                    is_agent_signal(agent, indexLeftDown, -1)):
                log_agent_read(agent)
                log_memory_write(agent)
                agent.write_memory_with("signal", -1)

        # leave old island and stand up
        elif agent.read_memory_with("signal") == 1:
            update_foot(agent)
            if release_signal(agent):
                log_memory_write(agent)
                agent.write_memory_with("signal", 0)
                agent.write_memory_with("foot", -1)
                if agent.planned_direction == dirW:
                    agent.write_memory_with("state", agent.read_memory_with("state") - 9)
                else:
                    agent.write_memory_with("state", agent.read_memory_with("state") + 9)

        # return to old island
        elif agent.read_memory_with("signal") == -1:
            if (agent.item_in(directions[indexRightDown]) or (
                    is_agent_signal(agent, indexRight, 0) or
                    is_agent_signal(agent, indexRightUp, 0) or
                    is_agent_signal(agent, indexRightDown, 0))
            ):
                log_memory_write(agent)
                agent.write_memory_with("signal", 0)
                if agent.planned_direction == dirW:
                    agent.planned_direction = dirE
                    agent.write_memory_with("state", agent.read_memory_with("state") + 10)
                else:
                    agent.planned_direction = dirW
                    agent.write_memory_with("state", agent.read_memory_with("state") - 10)

    return dirStand

##################################################

def alignment(agent):

    free_spaces = sum([
        not agent.agent_in(dirW) and not agent.item_in(dirW),
        not agent.agent_in(dirNW) and not agent.item_in(dirNW),
        not agent.agent_in(dirSW) and not agent.item_in(dirSW),
        not agent.agent_in(dirE) and not agent.item_in(dirE),
        not agent.agent_in(dirNE) and not agent.item_in(dirNE),
        not agent.agent_in(dirSE) and not agent.item_in(dirSE)
    ])

    right = dirE
    left = dirW
    rightUp = dirNE
    leftUp = dirNW
    rightDown = dirSE
    leftDown = dirSW

    if agent.planned_direction == dirE:
        right = dirW
        left = dirE
        rightUp = dirNW
        leftUp = dirNE
        rightDown = dirSW
        leftDown = dirSE

##################################################

    if agent.read_memory_with("adjust") > 0 and not (agent.agent_in(rightDown) or agent.agent_in(leftDown)):
        agent.write_memory_with("adjust", agent.read_memory_with("adjust") - 1 )
        return rightUp

    # relocate adjust value on to the agent state
    if ((agent.item_in(leftDown) and not agent.agent_in(left)) or (agent.agent_in(leftDown) and agent.get_agent_in(leftDown).read_memory_with("adjust") == 0)) and (agent.agent_in(rightUp) or free_spaces == 5):
        if agent.planned_direction == dirE:
            agent.write_memory_with("state", agent.read_memory_with("state") - agent.read_memory_with("adjust"))
        else:
            agent.write_memory_with("state", agent.read_memory_with("state") + agent.read_memory_with("adjust"))
        agent.write_memory_with("adjust", 0)

    if agent.read_memory_with("adjust") < 0 and agent.agent_in(left) and not agent.agent_in(rightDown) and not agent.agent_in(right) and (agent.agent_in(rightUp) or agent.item_in(rightDown) or free_spaces == 5):
        return leftUp

    return dirStand

##################################################

def release_signal(agent):
    rightDown = dirSE
    leftDown = dirSW
    right = dirE
    rightUp = dirNE

    if agent.planned_direction == dirE:
        rightDown = dirSW
        leftDown = dirSE
        right = dirW
        rightUp = dirNW

    # Conditions for detecting signal 1 and item presence in leftDown
    signal_1_conditions = [
        agent.agent_in(dirNW) and agent.get_agent_in(dirNW).read_memory_with("signal") == 1,
        agent.agent_in(dirW) and agent.get_agent_in(dirW).read_memory_with("signal") == 1,
        agent.agent_in(dirSW) and agent.get_agent_in(dirSW).read_memory_with("signal") == 1,
        agent.agent_in(dirE) and agent.get_agent_in(dirE).read_memory_with("signal") == 1,
        agent.agent_in(dirNE) and agent.get_agent_in(dirNE).read_memory_with("signal") == 1,
        agent.agent_in(dirSE) and agent.get_agent_in(dirSE).read_memory_with("signal") == 1,
        agent.item_in(leftDown)
    ]

    # Conditions for detecting signal 0 and item presence in rightDown
    signal_0_conditions = [
        agent.agent_in(dirNW) and agent.get_agent_in(dirNW).read_memory_with("signal") == 0,
        agent.agent_in(dirW) and agent.get_agent_in(dirW).read_memory_with("signal") == 0,
        agent.agent_in(dirSW) and agent.get_agent_in(dirSW).read_memory_with("signal") == 0,
        agent.agent_in(dirE) and agent.get_agent_in(dirE).read_memory_with("signal") == 0,
        agent.agent_in(dirNE) and agent.get_agent_in(dirNE).read_memory_with("signal") == 0,
        agent.agent_in(dirSE) and agent.get_agent_in(dirSE).read_memory_with("signal") == 0,
    ]

    # Count how many conditions are met
    count_signal_1 = sum(signal_1_conditions)
    count_signal_0 = sum(signal_0_conditions)

    # Count free spaces around the agent
    free_spaces = sum([
        not agent.agent_in(dirW) and not agent.item_in(dirW),
        not agent.agent_in(dirNW) and not agent.item_in(dirNW),
        not agent.agent_in(dirSW) and not agent.item_in(dirSW),
        not agent.agent_in(dirE) and not agent.item_in(dirE),
        not agent.agent_in(dirNE) and not agent.item_in(dirNE),
        not agent.agent_in(dirSE) and not agent.item_in(dirSE)
    ])

    if ((agent.agent_in(dirW) and agent.get_agent_in(dirW).read_memory_with("adjust") < 0) or
            (agent.agent_in(dirNW) and agent.get_agent_in(dirNW).read_memory_with("adjust") < 0) or
            (agent.agent_in(dirSW) and agent.get_agent_in(dirSW).read_memory_with("adjust") < 0) or
            (agent.agent_in(dirE) and agent.get_agent_in(dirE).read_memory_with("adjust") < 0) or
            (agent.agent_in(dirNE) and agent.get_agent_in(dirNE).read_memory_with("adjust") < 0) or
            (agent.agent_in(dirSE) and agent.get_agent_in(dirSE).read_memory_with("adjust") < 0)):
        agent.write_memory_with("adjust", -1)

    if ((count_signal_0 == 1 and agent.item_in(rightDown)) or
            (count_signal_1 == 1 and free_spaces >= 5) or
            (agent.agent_in(right) and agent.get_agent_in(right).read_memory_with("ready")) or
            (agent.agent_in(rightUp) and agent.get_agent_in(rightUp).read_memory_with("ready")) or
            (agent.agent_in(rightDown) and agent.get_agent_in(rightDown).read_memory_with("ready")) or
             free_spaces == 4 and agent.item_in(rightDown) and not agent.agent_in(right)):
        agent.write_memory_with("ready", True)

    # Return True if:
    # - Exactly one signal_1 and one signal_0, OR
    # - Exactly one signal_1 and at least 5 free spaces, AND
    # - The right-side neighbor condition is met
    if not agent.read_memory_with("ready"):
        return False

    return (((count_signal_1 == 1 and count_signal_0 == 1) or (count_signal_1 == 1 and free_spaces == 5)) or
            (agent.read_memory_with("foot") in [0, 2] and agent.agent_in(right) and agent.get_agent_in(right).read_memory_with("signal") == 0 and agent.item_in(leftDown)) or
            free_spaces == 4 and agent.item_in(rightDown) and not agent.agent_in(right))

##################################################

def update_foot(agent):
    # Check left-side neighbors (NW, W, SW)
    if ((agent.agent_in(dirNW) and agent.get_agent_in(dirNW).read_memory_with("foot") in [0, 1]) or
            (agent.agent_in(dirW) and agent.get_agent_in(dirW).read_memory_with("foot") in [0, 1]) or
            (agent.agent_in(dirSW) and agent.get_agent_in(dirSW).read_memory_with("foot") in [0, 1])):
        agent.write_memory_with("foot", 0)
        return True

    # Check right-side neighbors (NE, E, SE)
    if ((agent.agent_in(dirNE) and agent.get_agent_in(dirNE).read_memory_with("foot") in [1, 2]) or
          (agent.agent_in(dirE) and agent.get_agent_in(dirE).read_memory_with("foot") in [1, 2]) or
          (agent.agent_in(dirSE) and agent.get_agent_in(dirSE).read_memory_with("foot") in [1, 2])):
        agent.write_memory_with("foot", 2)
        return True
    return False

##################################################

def find_weight(agent):
    weight = 0
    for direction in directions:
        if agent.agent_in(direction):
            weight += 1
    return weight


def find_ground(agent):
    if agent.item_in(dirSW) or agent.item_in(dirSE):
        return 1

    ground = agent.read_memory_with("ground")
    chain = False

    for direction in directions:
        if agent.agent_in(direction) and agent.get_agent_in(direction).read_memory_with("ground") < ground:
            ground = agent.get_agent_in(direction).read_memory_with("ground") + 1
            chain = True
    if not chain:
        ground = falling
    return ground

def is_on_top(agent):
    log_memory_read(agent)
    if agent.read_memory_with("ground") == falling:
        return False
    for direction in directions:
        if agent.agent_in(direction) and agent.read_memory_with("ground") < agent.get_agent_in(direction).read_memory_with("ground"):
            return False
    return True

def is_agent_fixed(agent, direction):
    return agent.agent_in(directions[direction]) and log_agent_read(
        agent.get_agent_in(directions[direction])) and agent.get_agent_in(directions[direction]).read_memory_with("fixed")

def is_agent_signal(agent, direction, signal):
    return is_agent_fixed(agent, direction) and agent.get_agent_in(directions[direction]).read_memory_with("signal") == signal

def log_agent_read(agent):
    agent.world.csv_round.update_metrics(agent_read=1)
    agent.csv_agent_writer.write_agent(agent_read=1)
    return True

def log_agent_write(agent):
    agent.world.csv_round.update_metrics(agent_write=1)
    agent.csv_agent_writer.write_agent(agent_write=1)
    return True

def log_memory_read(agent):
    agent.world.csv_round.update_metrics(memory_read=1)
    agent.csv_agent_writer.write_agent(memory_read=1)
    return True

def log_memory_write(agent):
    agent.world.csv_round.update_metrics(memory_write=1)
    agent.csv_agent_writer.write_agent(memory_write=1)
    return True
