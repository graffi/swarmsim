import random


idle = False

assamble = False

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
            dirNE = (0.5,   1, 0)
            dirNW = (-0.5, 1, 0)
            dirSE = (0.5,  -1, 0)
            dirSW = (-0.5, -1, 0)
            dirW = (-1, 0, 0)
            dirE = (1, 0, 0)
            dirStand = (0,0,0)

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

            dirNotSetYet = (0,0,1)
            nextdirection = dirNotSetYet # characterizes an invalid state, will be changed later

            if not hasattr(agent, 'weight'):
                agent.weight = 0

            agent.weight = find_weight(agent)
            if False:
                if agent.weight == 1:
                    agent.set_color((0.5, 0.0, 0.0, 1.0))
                elif agent.weight == 2:
                    agent.set_color((0.0, 0.0, 0.5, 1.0))
                elif agent.weight == 3:
                    agent.set_color((0.0, 0.5, 0.0, 1.0))
                elif agent.weight == 4:
                    agent.set_color((0.5, 0.0, 0.5, 1.0))
                elif agent.weight == 5:
                    agent.set_color((0.5, 0.5, 0.0, 1.0))
                elif agent.weight == 6:
                    agent.set_color((0.5, 0.5, 0.5, 1.0))

            if not hasattr(agent, 'diagonal'):
                agent.diagonal = 0
            agent.diagonal = find_diagonal(agent)

            if not hasattr(agent, 'has_line'):
                agent.has_line = False
            if not agent.has_line:
                if agent.diagonal == 1:
                    agent.set_color((0.5, 0.0, 0.0, 1.0))
                elif agent.diagonal == -1:
                    agent.set_color((0.0, 0.0, 0.5, 1.0))
                elif agent.diagonal == 0:
                    agent.set_color((0.0, 0.5, 0.0, 1.0))
            else:
                agent.has_line = False

            if get_idle():

                if get_assamble():
                    if agent.weight == 1:
                        if hasattr(agent, 'first'):
                            if agent.agent_in(dirW):
                                nextdirection = dirNW
                            elif agent.agent_in(dirE):
                                nextdirection = dirNE
                    elif agent.weight == 2:
                        if agent.agent_in(dirW) and agent.agent_in(dirNE):
                            nextdirection = dirNW
                        elif agent.agent_in(dirE) and agent.agent_in(dirNW):
                            nextdirection = dirNE
                    if checklinedirection(world):
                        set_idle(False)
                        #set_assamble(False)


                    #elif not hasattr(agent, 'first'):
                        #if agent.item_in(dirSW) and agent.agent_in(dirE):
                            #nextdirection = dirNE
                        #elif agent.item_in(dirSE) and agent.agent_in(dirW):
                           #nextdirection = dirNW

                    #if hasattr(agent, 'first'):
                        #agent.first = False

                else:
                #try_bridge(world)
                    bridge_build(world)
                    if agent.weight == 1:
                        if agent.agent_in(dirSW):
                            nextdirection = dirSE
                        elif agent.agent_in(dirSE):
                            nextdirection = dirSW


                    if agent.weight == 2:
                        if agent.agent_in(dirE) and agent.agent_in(dirSW):
                            nextdirection = dirSE
                        elif agent.agent_in(dirW) and agent.agent_in(dirSE):
                            nextdirection = dirSW

            else:

                if not hasattr(agent, 'planned_direction'):
                    agent.planned_direction = random.choice([(1, 0, 0), (-1, 0, 0)])  # East or West
                    print("Agent", agent.get_id(), "planned direction:", agent.planned_direction)
                planned_direction = agent.planned_direction
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


                    agent.csv_agent_writer.write_agent(memory_read=1)

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


                # CASE Begin: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NE, walk E
                if nextdirection == dirNotSetYet and agentinSW and agentinSE and freeE and agentinNE and not agentinNW :
                    nextdirection = dirE    # freeE is True
                    agent.planned_direction = dirE
                # CASE End: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NE, walk E
                # Why not also case for W?
                if nextdirection == dirNotSetYet and agentinSW and agentinSE and freeW and agentinNW and not agentinNE:
                    nextdirection = dirW
                    agent.planned_direction = dirW
                # CASE End: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NE, walk E


                if nextdirection == dirNotSetYet and freeNE and freeE and agentinSE and not agentinNW :
                    nextdirection = dirE
                    agent.planned_direction = dirE# freeE is True



                # CASE Begin: CLIMBING - Try climb NW, then try climb NE. Must be free, and carrying nothing
                        # climb on agent in W if possible AND no other agent is on top of you
                if nextdirection == dirNotSetYet and (agentinW and freeNW) and ((not agentinNE) or (agentinNE and agentinE)):
                    nextdirection = dirNW

                        # climb on agent in E if possible AND no other agent is on top of you
                if nextdirection == dirNotSetYet  and  (agentinE and freeNE) and ((not agentinNW) or (agentinNW and agentinW)):
                    nextdirection = dirNE
                # CASE Begin: CLIMBING - Try climb NW, then try climb NE. Must be free, and


                # CASE Begin: TOWER SHIFT LEFT AND RIGHT
                # if standing only on agent in SE, check whether we need to move to E
                if (nextdirection == dirNotSetYet or nextdirection == dirStand) and agentinSE and not agentinSW and freeE and not agentinNW :
                    nextdirection = dirE
                    agent.planned_direction = dirE
                    dirWalkPlan = dirE

                if (nextdirection == dirNotSetYet or nextdirection == dirStand) and agentinSW and not agentinSE and freeW and not agentinNE:
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

        checklinedirection(world)



        # For next step: define the goal of the simulation, e.g. to build a tower of 6 agents and then terminate the simulation

        towerheight = maxAgentHeight - minAgentHeight + 1
        print("Round: ",world.get_actual_round(), "MaxHeight: ", maxAgentHeight , "Minheight: ", minAgentHeight , "Towerheight: ", towerheight ,"  Agent No.", agent.number, "  Coordinates", agent.coordinates, " Height", agent.coordinates[1],  "  Number of Agents", world.get_amount_of_agents())

        #global towerisbuild

        TowerOfAgentsHasBeenBuilt  = (towerheight == world.get_amount_of_agents())
        #if TowerOfAgentsHasBeenBuilt and stopiftowerbuilt:







def find_weight(agent):
    dirNE = (0.5, 1, 0)
    dirNW = (-0.5, 1, 0)
    dirSE = (0.5, -1, 0)
    dirSW = (-0.5, -1, 0)
    dirW = (-1, 0, 0)
    dirE = (1, 0, 0)

    weight = 0
    if agent.agent_in(dirW):
        weight+=1
    if agent.agent_in(dirNW):
        weight+=1
    if agent.agent_in(dirNE):
        weight+=1
    if agent.agent_in(dirE):
        weight+=1
    if agent.agent_in(dirSE):
        weight+=1
    if agent.agent_in(dirSW):
        weight+=1
    return weight


def find_diagonal(agent):
    if agent.weight == 1 or agent.weight == 2:

        dirNE = (0.5, 1, 0)
        dirNW = (-0.5, 1, 0)
        dirSE = (0.5, -1, 0)
        dirSW = (-0.5, -1, 0)
        dirW = (-1, 0, 0)
        dirE = (1, 0, 0)

        diagonal = 0
        if agent.agent_in(dirSW) and agent.agent_in(dirNE):
            diagonal=1
        if agent.agent_in(dirSE) and agent.agent_in(dirNW):
            diagonal=-1
        return diagonal
    return 0

def checklinedirection(world):
    dirNE = (0.5, 1, 0)
    dirNW = (-0.5, 1, 0)
    dirSE = (0.5, -1, 0)
    dirSW = (-0.5, -1, 0)

    for agent in world.get_agent_list():
        if agent.weight == 1:
            if agent.agent_in(dirSW) and agent.get_agent_in(dirSW).diagonal == 1:
                selected_agent = agent.get_agent_in(dirSW)
                while selected_agent.agent_in(dirSW):
                    selected_agent = selected_agent.get_agent_in(dirSW)
                if selected_agent.weight == 1 and selected_agent.agent_in(dirNE):
                    selected_agent.first = True
                    selected_agent.set_color((0.7, 0.0, 0.7, 1.0))
                    set_idle(True)
                    return True
            elif agent.agent_in(dirSE) and agent.get_agent_in(dirSE).diagonal == -1:
                selected_agent = agent.get_agent_in(dirSE)
                while selected_agent.agent_in(dirSE):
                    selected_agent = selected_agent.get_agent_in(dirSE)
                if selected_agent.weight == 1 and selected_agent.agent_in(dirNW):
                    selected_agent.first = True
                    selected_agent.set_color((0.7, 0.0, 0.7, 1.0))
                    set_idle(True)
                    return True
    return False


def set_idle(val):
    global idle
    idle = val

def get_idle():
    global idle
    return idle



def bridge_build(world):
    dirNE = (0.5, 1, 0)
    dirNW = (-0.5, 1, 0)
    dirSE = (0.5, -1, 0)
    dirSW = (-0.5, -1, 0)
    dirW = (-1, 0, 0)
    dirE = (1, 0, 0)


    for agent in world.get_agent_list():
        if agent.weight == 1:
            if agent.agent_in(dirE):
                selected_agent = agent.get_agent_in(dirE)
                while selected_agent.agent_in(dirE):
                    selected_agent = selected_agent.get_agent_in(dirE)
                if selected_agent.weight == 1:
                    #selected_agent.first = True
                    #selected_agent.set_color((0.7, 0.0, 0.7, 1.0))
                    set_assamble(True)
                    print("BREAK")
                    break



def set_assamble(val):
    global assamble
    assamble = val

def get_assamble():
    global assamble
    return assamble