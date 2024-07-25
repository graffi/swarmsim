import random

dirNE = (0.5, 1, 0)
dirNW = (-0.5, 1, 0)
dirSE = (0.5, -1, 0)
dirSW = (-0.5, -1, 0)
dirW = (-1, 0, 0)
dirE = (1, 0, 0)
dirStand = (0, 0, 0)
dirNotSetYet = (0,0,1)

directions = [dirNE,dirE,dirSE,dirSW,dirW,dirNW]

color_default = (0.7, 0.2, 0.2, 1.0)

color_fixed = (0.5, 0.0, 0.5, 1.0)

color_signal_1 = (0.5, 0.5, 0.0, 1.0)

color_signal_neg_1 = (0.7, 0.0, 0.0, 1.0)

color_on_top = (0.0, 0.5, 0.5, 1.0)


falling = 999



def solution(world):
    minAgentHeight = 0
    maxAgentHeight = 0

    if world.get_actual_round() % 1 == 0:
        # if world.get_actual_round() == 1:
        #     HashMap<int,String> walkDirectionList = new HashMap<String,String>();

        for agent in world.get_agent_list():

            # print(world.get_actual_round(), " Agent No.", agent.number, "  Coordinates", agent.coordinates, " Height", agent.coordinates[1], "  Number of Agents", world.get_amount_of_agents())

            # KG: Correct: set minAgentHeight and maxAgentHeight to height of agent [1]

            if agent.coordinates[1] > maxAgentHeight:
                maxAgentHeight = agent.coordinates[1]
            if agent.coordinates[1] < minAgentHeight:
                minAgentHeight = agent.coordinates[1]

            # Check whether in the direction of SE, SW are agents or items
            # These directions are all relative to the current agent: First value is X coordinate (left right), second is the Y coordinate (up down), the third coordinate is for 3D coordinate systems but not used in 2D-Hex-Grid

            iteminE = agent.item_in(dirE)
            iteminW = agent.item_in(dirW)
            iteminSE = agent.item_in(dirSE)
            iteminSW = agent.item_in(dirSW)
            iteminNE = agent.item_in(dirNE)
            iteminNW = agent.item_in(dirNW)

            agentinE = agent.agent_in(dirE)
            agentinW = agent.agent_in(dirW)
            agentinSE = agent.agent_in(dirSE)
            agentinSW = agent.agent_in(dirSW)
            agentinNE = agent.agent_in(dirNE)
            agentinNW = agent.agent_in(dirNW)

            freeW = not agent.agent_in(dirW) and not agent.item_in(dirW)
            freeE = not agent.agent_in(dirE) and not agent.item_in(dirE)
            freeNW = not agent.agent_in(dirNW) and not agent.item_in(dirNW)
            freeNE = not agent.agent_in(dirNE) and not agent.item_in(dirNE)
            freeSW = not agent.agent_in(dirSW) and not agent.item_in(dirSW)
            freeSE = not agent.agent_in(dirSE) and not agent.item_in(dirSE)


            nextdirection = dirNotSetYet # characterizes an invalid state, will be changed later

            if not hasattr(agent, 'planned_direction'):
                agent.planned_direction = random.choice([dirW, dirE])  # East or West
                print("Agent", agent.get_id(), "planned direction:", agent.planned_direction)
            planned_direction = agent.planned_direction
            agent.write_memory_with("planned_direction", planned_direction)

            if not hasattr(agent, 'weight'):
                agent.weight = 0
            agent.weight = find_weight(agent)


            agent.ground = find_ground(agent)
            #agent.csv_agent_writer.write_agent(steps=agent.ground)
            agent.write_memory_with("ground", agent.ground)

            fixed_diagonal(agent)

            if agent.ground >= falling:
                if agent.timer >= 60:
                    agent.fixed = False
                    agent.timer = 0
                agent.timer += 1
            else:
                agent.timer = 0

            if agent.fixed:
                nextdirection = directed_tentacle(agent)

            agent.write_memory_with("timer", agent.timer)
            agent.write_memory_with("state", agent.state)
            agent.write_memory_with("fixed", agent.fixed)
            agent.write_memory_with("signal", agent.signal)

            agent.set_color(color_default)

            if agent.fixed:
                agent.set_color(color_fixed)
            if agent.signal == 1:
                agent.set_color(color_signal_1)
            if agent.signal == -1:
                agent.set_color(color_signal_neg_1)
            if is_on_top(agent):
                agent.set_color(color_on_top)

            if not agent.fixed:

                # try:
                #     print("Agent No " + agent.number + "   dirWalkPlan is set to " + str(dirWalkPlan[agent.number]))
                # except:
                #     dirWalkPlan[agent.number] = random.choice((dirW, dirE))

                # CASE Begin: FALLING Start  - freeSW and freeSE -   Check whether Agent needs to fall
                if freeSW and freeSE:
                    yposition = agent.coordinates[1]

                    # We know already that this agent must fall, it will be in a zig (SE) - zag (SW) pattern, depending on the height (y - coordinate)
                    if (yposition % 2) == 0:
                        nextdirection = dirSW
                    else:
                        nextdirection = dirSE
                # CASE End: FALLING End  - freeSW and freeSE -   Check whether Agent needs to fall


                # CASE Begin: Agent is alone on the floor - Walk Left - Right -  iteminSE and iteminSW  - and nothing is above it
                    # Walk to left of right if possible, otherwise stand
                if not agentinW and not agentinE:


                    if nextdirection == dirNotSetYet and iteminSE and iteminSW:
                        # Move left or right
                        # randdirection = dirE

                        randdirection = planned_direction # dirWalkPlan
                        nextdirection = dirStand

                        if randdirection == dirW and freeW and not agentinNE:
                            nextdirection = randdirection
                        if randdirection == dirW and not freeW and agentinNE:
                            agent.planned_direction = dirE
                            randdirection = dirE
                            nextdirection = randdirection
                        if randdirection == dirE and freeE and not agentinNW:
                            nextdirection = randdirection
                        if randdirection == dirE and not freeE and agentinNW:
                            agent.planned_direction = dirW
                            randdirection = dirW
                            nextdirection = randdirection


                    if nextdirection == dirNotSetYet and agentinSE and iteminSW and not agentinNW:

                        # Move left or right
                        randdirection = planned_direction
                        nextdirection = dirStand
                        if randdirection == dirE and freeE:
                            nextdirection = randdirection


                    if nextdirection == dirNotSetYet and agentinSW and iteminSE and not agentinNE:
                        # Move left or right

                        randdirection = planned_direction
                        nextdirection = dirStand
                        if randdirection == dirW and freeW:
                            nextdirection = randdirection

                    if nextdirection == dirNotSetYet and freeSE and iteminSW and not agentinNE and freeW:
                        # Move left
                        dirWalkPlan = dirW
                        nextdirection = dirW
                        agent.planned_direction = dirW
                        # nextdirection = dirStand


                    if nextdirection == dirNotSetYet and freeSW and iteminSE and not agentinNW and freeE:
                        # Move left
                        nextdirection = dirE
                        dirWalkPlan = dirE
                        agent.planned_direction = dirE
                    # CASE End: Agent is on the floor - Walk Left -Right - iteminSE and iteminSW  - and nothing is above it

                if agent.planned_direction == dirW and agent.agent_in(dirW) and agent.get_agent_in(dirW).fixed:
                    nextdirection = dirE

                elif agent.planned_direction == dirE and agent.agent_in(dirE) and agent.get_agent_in(dirE).fixed:
                    nextdirection = dirW

                # CASE Begin: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NE, walk E
                if nextdirection == dirNotSetYet and agentinSW and agentinSE and freeE and agentinNE and not agentinNW and not agent.get_agent_in(dirSE).fixed:
                    nextdirection = dirE    # freeE is True
                    agent.planned_direction = dirE
                # CASE End: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NE, walk E
                # Why not also case for W?
                if nextdirection == dirNotSetYet and agentinSW and agentinSE and freeW and agentinNW and not agentinNE and not agent.get_agent_in(dirSW).fixed:
                    nextdirection = dirW
                    agent.planned_direction = dirW
                # CASE End: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NE, walk E


                if nextdirection == dirNotSetYet and freeNE and freeE and agentinSE and not agentinNW :
                    nextdirection = dirE
                    agent.planned_direction = dirE # freeE is True

                # CASE Begin: CLIMBING - Try climb NW, then try climb NE. Must be free, and carrying nothing
                        # climb on agent in W if possible AND no other agent is on top of you
                if nextdirection == dirNotSetYet and (agentinW and freeNW and not agent.get_agent_in(dirW).fixed) and ((not agentinNE) or (agentinNE and agentinE and not agent.get_agent_in(dirNE).fixed and not agent.get_agent_in(dirE).fixed)):
                    nextdirection = dirNW

                        # climb on agent in E if possible AND no other agent is on top of you
                if nextdirection == dirNotSetYet and (agentinE and freeNE and not agent.get_agent_in(dirE).fixed) and ((not agentinNW) or (agentinNW and agentinW and not agent.get_agent_in(dirNW).fixed and not agent.get_agent_in(dirW).fixed)):
                    nextdirection = dirNE
                # CASE Begin: CLIMBING - Try climb NW, then try climb NE. Must be free, and


                # CASE Begin: TOWER SHIFT LEFT AND RIGHT
                # if standing only on agent in SE, check whether we need to move to E
                if (nextdirection == dirNotSetYet or nextdirection == dirStand) and agentinSE and not agentinSW and freeE and not agentinNW and (True or not agent.get_agent_in(dirSE).fixed):
                    nextdirection = dirE
                    agent.planned_direction = dirE
                    dirWalkPlan = dirE

                if (nextdirection == dirNotSetYet or nextdirection == dirStand) and agentinSW and not agentinSE and freeW and not agentinNE and (True or not agent.get_agent_in(dirSW).fixed):
                    yposition = agent.coordinates[1]
                    nextdirection = dirW
                    agent.planned_direction = dirW
                    dirWalkPlan = dirW

                # CASE END: TOWER SHIFT LEFT AND RIGHT

                # CASE DEFAULT: If no direction selected, do not move
                if nextdirection == dirNotSetYet:
                    nextdirection = dirStand

            #if agent.lock >= 1:
                #agent.set_color((0.0, 0.0, 0.0, 1.0))


                # FINAL MOVE: if the agent is not falling currently, walk in the selected direction
            if nextdirection != dirNotSetYet:
                agent.move_to(nextdirection)



        # For next step: define the goal of the simulation, e.g. to build a tower of 6 agents and then terminate the simulation

        towerheight = maxAgentHeight - minAgentHeight + 1
        print("Round: ",world.get_actual_round(), "MaxHeight: ", maxAgentHeight , "Minheight: ", minAgentHeight , "Towerheight: ", towerheight ,"  Agent No.", agent.number, "  Coordinates", agent.coordinates, " Height", agent.coordinates[1],  "  Number of Agents", world.get_amount_of_agents())

        #global towerisbuild

        TowerOfAgentsHasBeenBuilt  = (towerheight == world.get_amount_of_agents())
        #if TowerOfAgentsHasBeenBuilt and stopiftowerbuilt:

def find_weight(agent):

    weight = 0
    for direction in directions:
        if agent.agent_in(direction):
            weight+=1
    return weight


def find_ground(agent):

    if (agent.item_in(dirSW) or agent.item_in(dirSE)):
        return 1

    ground = agent.ground
    chain = False

    for direction in directions:
        if agent.agent_in(direction) and agent.get_agent_in(direction).ground < ground:
            ground = agent.get_agent_in(direction).ground + 1
            chain = True
    if not chain:
        ground = falling
    return ground


def fixed_diagonal(agent):

    freeW = not agent.agent_in(dirW) and not agent.item_in(dirW)
    freeE = not agent.agent_in(dirE) and not agent.item_in(dirE)
    freeNW = not agent.agent_in(dirNW) and not agent.item_in(dirNW)
    freeNE = not agent.agent_in(dirNE) and not agent.item_in(dirNE)
    freeSW = not agent.agent_in(dirSW) and not agent.item_in(dirSW)
    freeSE = not agent.agent_in(dirSE) and not agent.item_in(dirSE)

    right = dirE
    left = dirW
    rightUp = dirNE
    leftDown = dirSW
    rightDown = dirSE

    freeRight = freeE
    freeLeft = freeW
    freeRightDown = freeSE
    freeRightUp = freeNE
    freeLeftDown = freeSW

    if agent.planned_direction == dirE:

        right = dirW
        left = dirE
        rightUp = dirNW
        leftDown = dirSE
        rightDown = dirSW

        freeRight = freeW
        freeLeft = freeE
        freeRightDown = freeSW
        freeRightUp = freeNW
        freeLeftDown = freeSE

    if agent.weight >= 1 and agent.weight <= 2:
        if agent.fixed:
            if ((freeLeft or agent.agent_in(left) and agent.get_agent_in(left).fixed) and (abs(agent.state) >= 11 or (abs(agent.state) >= 10 and freeRightDown and freeRight)) and
                    (((agent.agent_in(leftDown) and agent.get_agent_in(leftDown).fixed and agent.get_agent_in(leftDown).ground < agent.ground) or agent.item_in(leftDown)) and
                    ((agent.agent_in(rightUp) and not agent.get_agent_in(rightUp).fixed) or (agent.agent_in(right) and not agent.get_agent_in(right).fixed) or freeRightUp))):
                agent.fixed = False
                agent.state = 0
                agent.signal = 0

                log_agent_read(agent)
                log_memory_write(agent)
        else:
            if freeLeftDown and (agent.item_in(rightDown) or (agent.agent_in(rightDown) and agent.get_agent_in(rightDown).fixed)):
                agent.fixed = True

                log_memory_write(agent)

def directed_tentacle(agent):

    freeW = not agent.agent_in(dirW) and not agent.item_in(dirW)
    freeE = not agent.agent_in(dirE) and not agent.item_in(dirE)
    freeNW = not agent.agent_in(dirNW) and not agent.item_in(dirNW)
    freeNE = not agent.agent_in(dirNE) and not agent.item_in(dirNE)
    freeSW = not agent.agent_in(dirSW) and not agent.item_in(dirSW)
    freeSE = not agent.agent_in(dirSE) and not agent.item_in(dirSE)

    free_directions   = [freeNE,freeE,freeSE,freeSW,freeW,freeNW]
    # free_directions = [     0,    1,     2,     3,    4,     5]

    indexRightUp = (0 + agent.state) % 6
    indexRight  = (1 + agent.state) % 6
    indexRightDown = (2 + agent.state) % 6
    indexLeftDown = (3 + agent.state) % 6
    indexLeft  = (4 + agent.state) % 6
    indexLeftUp = (5 + agent.state) % 6

    leftDown = dirSW
    rightDown = dirSE

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

        leftDown = dirSE
        rightDown = dirSW

    if agent.weight >= 1 and agent.weight <= 2:

        # normal mode to search islands
        if agent.signal == 0:
            # move the diagonal tower to a new direction
            if free_directions[indexLeftDown] and is_agent_fixed(agent,indexRightDown) and (is_agent_fixed(agent,indexLeft) or (free_directions[indexLeft] and agent.weight == 1)):
                log_agent_read(agent)
                return directions[indexLeftDown]

            # rotate the direction of the current agent
            elif is_agent_fixed(agent,indexRight) and (
                    (free_directions[indexLeftDown] and agent.get_agent_in(directions[indexRight]).weight == 1) or
                    abs(agent.state - agent.get_agent_in(directions[indexRight]).state) <= 2):
                log_memory_write(agent)

                if agent.planned_direction == dirW:
                    agent.state -= 1
                else:
                    agent.state += 1

            # tentacle has found a new island
            elif agent.state >= -6 and agent.state <= 6 and (
                    (agent.item_in(leftDown) and not agent.agent_in(rightDown)) or (
                    is_agent_signal(agent,indexLeft,1) or
                    is_agent_signal(agent,indexLeftUp,1) or
                    is_agent_signal(agent,indexLeftDown,1))
            ):
                log_agent_read(agent)
                log_memory_write(agent)
                agent.signal = 1

            # tentacle move return to the start of old island
            elif (is_on_top(agent) and agent.item_in(directions[indexLeftDown]) and not agent.item_in(leftDown)) or (
                    is_agent_signal(agent,indexLeft,-1) or
                    is_agent_signal(agent,indexLeftUp,-1) or
                    is_agent_signal(agent,indexLeftDown,-1)):
                log_agent_read(agent)
                log_memory_write(agent)
                agent.signal = -1

        # leave old island and stand up
        elif agent.signal == 1:
            if(agent.item_in(rightDown) or (
                is_agent_signal(agent,indexRight,0) or
                is_agent_signal(agent,indexRightUp,0) or
                is_agent_signal(agent,indexRightDown,0))
            ):
                log_memory_write(agent)
                agent.signal = 0
                if agent.planned_direction == dirW:
                    agent.state -= 9
                else:
                    agent.state += 9

        # return to old island
        elif agent.signal == -1:
            if (agent.item_in(directions[indexRightDown]) or (
                is_agent_signal(agent,indexRight,0) or
                is_agent_signal(agent,indexRightUp,0) or
                is_agent_signal(agent,indexRightDown,0))
            ):
                log_memory_write(agent)
                agent.signal = 0
                if agent.planned_direction == dirW:
                    agent.planned_direction = dirE
                    agent.state += 10
                else:
                    agent.planned_direction = dirW
                    agent.state -= 10

    return dirStand


def is_on_top(agent):
    log_memory_read(agent)
    if agent.ground == falling:
        return False
    for direction in directions:
        if agent.agent_in(direction) and agent.ground < agent.get_agent_in(direction).ground:
            return False
    return True

def is_agent_fixed(agent,direction):
    return agent.agent_in(directions[direction]) and log_agent_read(agent.get_agent_in(directions[direction])) and agent.get_agent_in(directions[direction]).fixed

def is_agent_signal(agent,direction,signal):
    return is_agent_fixed(agent,direction) and agent.get_agent_in(directions[direction]).signal == signal


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
