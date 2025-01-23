import math
import random
import colorsys

def solution(world):
    global minAgentHeight, maxAgentHeight, maxDistance
    minAgentHeight = 0
    maxAgentHeight = 0
    maxDistance = 0
    stopiftowerbuilt = False
    visualizeEachMove = True
    debugon = False

    global agents_and_distances, alpha, beta, nextdirection, paramStartFromTowerHeight, agentCount
    global dirE, dirW, dirNE, dirSE, dirSW, dirNW, dirStand, dirNotSetYet

    global iteminE, iteminW, iteminNE, iteminNW, iteminSE, iteminSW
    global agentinE, agentinW, agentinNE, agentinNW, agentinSE, agentinSW
    global freeW, freeE, freeNE, freeNW, freeSE, freeSW
    global color1, color2, color3, color4

    paramStartFromTowerHeight = 0.4
    alpha = 0.3
    beta = 0.6

    color1 = (0.0, 0.2, 0.2, 1.0)
    color2 = (0.0, 0.6, 0.0, 1.0)
    color3 = (0.8, 0.8, 0.0, 1.0)
    color4 = (0.9, 0.4, 0.4, 1.0)

    dirNE = (0.5, 1, 0)
    dirNW = (-0.5, 1, 0)
    dirSE = (0.5, -1, 0)
    dirSW = (-0.5, -1, 0)
    dirW = (-1, 0, 0)
    dirE = (1, 0, 0)
    dirStand = (0, 0, 0)
    dirNotSetYet = (0, 0, 1)



    if world.get_actual_round() % 1 == 0:

        # Step 1: - Calculate for each agent: the distance of that agent to an item.

        # - Label Location of each item as distance = 0
        # - Label location of each Neighbor Position of Item as Distance = 1

        agents_and_distances = calculateDistances(world)
        maxDistance = 0


        for agent in agents_and_distances:
            if (agents_and_distances[agent] > maxDistance):
                maxDistance = agents_and_distances[agent]
        # print("MaxDist = ", maxDistance)


        if debugon == True:
            for agent, distance in agents_and_distances.items():
                print("Round:", world.get_actual_round(), " Agent:", agent, "Distance:", distance, " MaxDist = ", maxDistance, " Ratio = ", distance/maxDistance)
            # Iterate over each agent: If there is an item in the neighborhood, set the distance of the agent to 1.


        # From here we focus on the movement of each agent
        for agent in world.get_agent_list():
            # calculate for this specific agent it ratio = own-distance / max-distance

            if not visualizeEachMove or world.get_actual_round() % world.get_amount_of_agents() == agent.number - 1:
                print("XXXXXXX", world.get_actual_round(), " Agent No.", agent.number, "  Coordinates", agent.coordinates, " Height", agent.coordinates[1], "  Number of Agents", world.get_amount_of_agents())

                print(world.get_actual_round(), " Agent No.", agent.number, "  Coordinates", agent.coordinates, " Height", agent.coordinates[1], "  Number of Agents", world.get_amount_of_agents())
                checkSurrounding(agent)
                agentCount = len(world.get_agent_list())

                if maxDistance == 0 or agent not in agents_and_distances:
                    agent.set_color(color1)



                    agent.write_memory_with("status", "towerbuild")
                    agent.write_memory_with("owndistance", 1)


                    # mydistance = age
                    # agent.read_memory_with("owndistance")





                    
                    walkRegular(agent)
                else:
                    myRatio = agents_and_distances[agent] / maxDistance
                    set_rainbow_color(agent, agents_and_distances[agent], maxDistance)

                    if maxDistance < paramStartFromTowerHeight * agentCount:
                        # agent.set_color(color1)
                        walkDirected(agent)
                    elif myRatio < alpha :
                        # agent.set_color(color2)
                        walkRegular(agent)
                    elif myRatio >= alpha and myRatio < beta :
                        # agent.set_color(color3)
                        walkHorizontal(agent)
                    elif myRatio >= beta :
                        # agent.set_color(color4)
                        walkBridgeend(agent)
                        # test

            # For next step: define the goal of the simulation, e.g. to build a tower of n agents and then terminate the simulation



            if agent.coordinates[1] > maxAgentHeight:
                maxAgentHeight = agent.coordinates[1]
            if agent.coordinates[1] < minAgentHeight:
                minAgentHeight = agent.coordinates[1]

            towerheight = maxAgentHeight - minAgentHeight + 1
            if debugon:
                print("Round: ", world.get_actual_round(), "MaxHeight: ", maxAgentHeight, "Minheight: ", minAgentHeight,
                  "Towerheight: ", towerheight, "  Agent No.", agent.number, "  Coordinates", agent.coordinates,
                  " Height", agent.coordinates[1], "  Number of Agents", world.get_amount_of_agents())

            TowerHasBeenBuilt = (towerheight == world.get_amount_of_agents())
            if TowerHasBeenBuilt and stopiftowerbuilt:
                world.set_successful_end()




def checkSurrounding(agent):
    global iteminE, iteminW, iteminNE, iteminNW, iteminSE, iteminSW
    global agentinE, agentinW, agentinNE, agentinNW, agentinSE, agentinSW
    global freeW, freeE, freeNE, freeNW, freeSE, freeSW
    global agents_and_distances, alpha, beta
    global dirE, dirW, dirNE, dirSE, dirSW, dirNW, dirStand, dirNotSetYet

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


def walkRegular(agent):
    global iteminE, iteminW, iteminNE, iteminNW, iteminSE, iteminSW
    global agentinE, agentinW, agentinNE, agentinNW, agentinSE, agentinSW
    global freeW, freeE, freeNE, freeNW, freeSE, freeSW
    checkSurrounding(agent)

    myDistanceplusone = 1
    myRatioplusone = 0
    try:
        myDistanceplusone = agents_and_distances[agent]
        myDistanceplusone = myDistanceplusone + 2
        myRatioplusone = myDistanceplusone / maxDistance
    except:
        print("Agent ", agent, " has no distance")

    nextdirection = dirNotSetYet  # characterizes an invalid state, will be changed later

    # CASE Begin: FALLING Start  - freeSW and freeSE -   Check whether Agent needs to fall
    # Should only apply if the tower building is active OR this is not the last green, which just turned yellow)
    if freeSW and freeSE and (maxDistance < paramStartFromTowerHeight * agentCount or myRatioplusone < alpha):
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
            randdirection = random.choice((dirW, dirE))
            nextdirection = dirStand

            if randdirection == dirW and freeW and not agentinNE:
                nextdirection = randdirection
            if randdirection == dirE and freeE and not agentinNW:
                nextdirection = randdirection

        if nextdirection == dirNotSetYet and agentinSE and iteminSW and not agentinNW:
            # Move left or right
            randdirection = random.choice((dirStand, dirE))
            nextdirection = dirStand
            if randdirection == dirE and freeE:
                nextdirection = randdirection

        if nextdirection == dirNotSetYet and agentinSW and iteminSE and not agentinNE:
            # Move left or right
            randdirection = random.choice((dirStand, dirW))
            nextdirection = dirStand
            if randdirection == dirW and freeW:
                nextdirection = randdirection

        if nextdirection == dirNotSetYet and freeSE and iteminSW and not agentinNE and freeW:
            # Move left
            nextdirection = dirW

        if nextdirection == dirNotSetYet and freeSW and iteminSE and not agentinNW and freeE:
            # Move left
            nextdirection = dirE
    # CASE End: Agent is on the floor - Walk Left -Right - iteminSE and iteminSW  - and nothing is above it

    # CASE Begin: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NE, walk E
    if nextdirection == dirNotSetYet and agentinSW and agentinSE and freeE and agentinNE and not agentinNW:
        nextdirection = dirE  # freeE is True
    # CASE End: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NE, walk E
    # Why not also case for W?
    if nextdirection == dirNotSetYet and agentinSW and agentinSE and freeW and agentinNW and not agentinNE and not agentinE:
        nextdirection = dirW
    # CASE End: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NE, walk E

    if nextdirection == dirNotSetYet and freeNE and freeE and agentinSE and not agentinNW:
        nextdirection = dirE  # freeE is True

    # myDistanceplusone = agents_and_distances[agent]
    # myDistanceplusone = myDistanceplusone + 2
    # myRatioplusone = myDistanceplusone / maxDistance

    #Climb only if not last in category
    # if myDistanceplusone < alpha:
    if True:
        # CASE Begin: CLIMBING - Try climb NW, then try climb NE. Must be free, and carrying nothing
        # climb on agent in W if possible AND no other agent is on top of you
        if nextdirection == dirNotSetYet and (agentinW and freeNW) and ((not agentinNE) or (agentinNE and agentinE)) and (maxDistance < paramStartFromTowerHeight * agentCount or myRatioplusone < alpha):
            nextdirection = dirNW

        # climb on agent in E if possible AND no other agent is on top of you
        # LAST Green should not climb on Yellow (Except there are sufficient green around)
        if nextdirection == dirNotSetYet and (agentinE and freeNE) and ((not agentinNW) or (agentinNW and agentinW)) and (agentinSE or (maxDistance < paramStartFromTowerHeight * agentCount or myRatioplusone < alpha)):
            nextdirection = dirNE
        # CASE Begin: CLIMBING - Try climb NW, then try climb NE. Must be free, and

    # CASE Begin: TOWER SHIFT LEFT AND RIGHT
    # if standing only on agent in SE, check whether we need to move to E
    # We must forbid that the LAST green agents slides to the east (or west), as the yellow nodes are not stable! Hm, only to apply once the special rules apply.
    if nextdirection == dirNotSetYet and agentinSE and not agentinSW and freeE and not agentinNW and (maxDistance < paramStartFromTowerHeight * agentCount or myRatioplusone < alpha):
        nextdirection = dirE

    if nextdirection == dirNotSetYet and agentinSW and not agentinSE and freeW and not agentinNE and not agentinE:
        yposition = agent.coordinates[1]
        nextdirection = dirW
    # CASE END: TOWER SHIFT LEFT AND RIGHT

    # CASE DEFAULT: If no direction selected, do not move
    if nextdirection == dirNotSetYet:
        nextdirection = dirStand

    # FINAL MOVE: if the agent is not falling currently, walk in the selected direction
    if nextdirection != dirNotSetYet:
        agent.move_to(nextdirection)


def walkHorizontal(agent):
    global iteminE, iteminW, iteminNE, iteminNW, iteminSE, iteminSW
    global agentinE, agentinW, agentinNE, agentinNW, agentinSE, agentinSW
    global freeW, freeE, freeNE, freeNW, freeSE, freeSW
    checkSurrounding(agent)
    myDistanceplusone = agents_and_distances[agent]
    myDistanceplusone = myDistanceplusone + 1
    myRatioplusone = myDistanceplusone / maxDistance

    myDistanceminusone = agents_and_distances[agent]
    myDistanceminusone = myDistanceminusone - 1
    myRatiominusone = myDistanceminusone / maxDistance

    nextdirection = dirNotSetYet  # characterizes an invalid state, will be changed later

    # CASE Begin: Agent is alone on the floor - Walk Left - Right -  iteminSE and iteminSW  - and nothing is above it
    # Walk to left of right if possible, otherwise stand
    if True:
        # not agentinW and not agentinE:

        if nextdirection == dirNotSetYet and iteminSE and iteminSW:
            # Move left or right
            randdirection = random.choice((dirW, dirE))
            nextdirection = dirStand

            if randdirection == dirW and freeW and not agentinNE:
                nextdirection = randdirection
            if randdirection == dirE and freeE and not agentinNW:
                nextdirection = randdirection

        if nextdirection == dirNotSetYet and agentinSE and iteminSW and not agentinNW:
            # Move left or right
            randdirection = random.choice((dirStand, dirE))
            nextdirection = dirStand
            if randdirection == dirE and freeE:
                nextdirection = randdirection

        if nextdirection == dirNotSetYet and agentinSW and iteminSE and not agentinNE:
            # Move left or right
            randdirection = random.choice((dirStand, dirW))
            nextdirection = dirStand
            if randdirection == dirW and freeW:
                nextdirection = randdirection

        if nextdirection == dirNotSetYet and freeSE and iteminSW and not agentinNE and freeW:
            # Move left
            nextdirection = dirW

        if nextdirection == dirNotSetYet and freeSW and iteminSE and not agentinNW and freeE:
            # Move left
            nextdirection = dirE

    # CASE End: Agent is on the floor - Walk Left -Right - iteminSE and iteminSW  - and nothing is above it

    # CASE Begin: CLIMBING - Try climb NW, then try climb NE. Must be free, and carrying nothing
    # climb on agent in W if possible AND no other agent is on top of you
    # if nextdirection == dirNotSetYet and (agentinW and freeNW) and agentinSW  and not agentinE and ((not agentinNE) or (agentinNE and agentinE)):
    #     nextdirection = dirNW
    #
    # climb on agent in E if possible AND no other agent is on top of you
    if nextdirection == dirNotSetYet and (agentinE and freeNE)  and not agentinW and ((not agentinNW) or (agentinNW and agentinW)) and agentinSE and myRatioplusone < beta:
        nextdirection = dirNE
    if nextdirection == dirNotSetYet and (agentinE and freeNE)  and not agentinW and ((not agentinNW) or (agentinNW and agentinW)) and myRatiominusone > alpha:
        nextdirection = dirNE
    # CASE Begin: CLIMBING - Try climb NW, then try climb NE. Must be free, and


    if nextdirection == dirNotSetYet and freeNE and freeE and agentinSE and agentinSW and not agentinNW:
        nextdirection = dirE  # freeE is True, THIS EAST


    # CASE Begin: TOWER SHIFT LEFT AND RIGHT
    # if standing only on agent in SE, check whether we need to move to E
    # and not agentinSW  - > check if needed
    if nextdirection == dirNotSetYet and agentinSE and freeE and not agentinNW and myRatioplusone < beta:

        nextdirection = dirStand

        # print("Walk Horizontal: This Going East 1:", agent, agents_and_distances[agent], maxDistance, agents_and_distances[agent]/ maxDistance, myRatioplusone, beta)

    # CASE Begin: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NE, walk E
    if nextdirection == dirNotSetYet and agentinSW and agentinSE and freeE and agentinNE and not agentinNW:
        nextdirection = dirE  # freeE is True
    # CASE End: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NW, walk W
    # Why not also case for W?
    if nextdirection == dirNotSetYet and agentinSW and agentinSE and freeW and agentinNW and not agentinNE and not agentinE:
        nextdirection = dirW
    # CASE End: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NE, walk E

    #
    # if nextdirection == dirNotSetYet and agentinSW and not agentinSE and freeW and not agentinNE:
    #     yposition = agent.coordinates[1]
    #     nextdirection = dirW
    # CASE END: TOWER SHIFT LEFT AND RIGHT

    # This will move all to the EAST

    # if agents_and_distances[agent] == maxDistance and agentinSE and freeE and myRatioplusone < beta:
    if agentinSE and freeE and freeW and freeSW and freeNW and freeNE:
        nextdirection = dirE
        print("Walk Horizontal: This Going East 2:", agent, agents_and_distances[agent], maxDistance, myRatioplusone,
              beta)

        # print("Walk Horizontal: Going East:", agent, agents_and_distances[agent], maxDistance, myRatiominusone, alpha)
    if agentinW and freeSW and freeSE:
        nextdirection = dirStand
    elif agentinSW and freeSE and freeNW and freeNE and myRatiominusone > alpha: #and agents_and_distances[agent] == maxDistance
        nextdirection = dirSE
    # elif agentinSW and agentinE and freeSE and freeNW and freeNE:  # and agents_and_distances[agent] == maxDistance
    #     nextdirection = dirSE

    # if agentinSW and agentinE and freeW and freeNW and freeNE and freeSE and myRatiominusone >= alpha:
    #     nextdirection = dirSE
        # print("Walk Horizontal: Going down: ", agent, agents_and_distances[agent], maxDistance, myRatiominusone, alpha)
    if agentinSW and agentinSE and freeE and not agentinNW:
        nextdirection = dirE
        print("Walk Horizontal: This Going East 3:", agent, agents_and_distances[agent], maxDistance, myRatioplusone,
              beta)
        print("Break Point" )



    # CASE Begin: FALLING Start  - freeSW and freeSE -   Check whether Agent needs to fall
    if freeSW and freeSE and not agentinE and not agentinW:
        yposition = agent.coordinates[1]
        # print("Walk Horizontal: This agent ", agent, " is at X ", agent.coordinates[0], ", Y ", agent.coordinates[1], " : should fall")

        # We know already that this agent must fall, it will be in a zig (SE) - zag (SW) pattern, depending on the height (y - coordinate)
        if (yposition % 2) == 0:
            nextdirection = dirSW
        else:
            nextdirection = dirSE
    # CASE End: FALLING End  - freeSW and freeSE -   Check whether Agent needs to fall

    # CASE DEFAULT: If no direction selected, do not move
    if nextdirection == dirNotSetYet:
        nextdirection = dirStand

    # FINAL MOVE: if the agent is not falling currently, walk in the selected direction
    if nextdirection != dirNotSetYet:
        agent.move_to(nextdirection)


def walkBridgeend(agent):
    global iteminE, iteminW, iteminNE, iteminNW, iteminSE, iteminSW
    global agentinE, agentinW, agentinNE, agentinNW, agentinSE, agentinSW
    global freeW, freeE, freeNE, freeNW, freeSE, freeSW
    checkSurrounding(agent)

    nextdirection = dirNotSetYet  # characterizes an invalid state, will be changed later



    # CASE Begin: Agent is alone on the floor - Walk Left - Right -  iteminSE and iteminSW  - and nothing is above it
    # Walk to left of right if possible, otherwise stand
    if True:
        # not agentinW and not agentinE:

        if nextdirection == dirNotSetYet and iteminSE and iteminSW:
            # Move left or right
            randdirection = random.choice((dirW, dirE))
            nextdirection = dirStand

            if randdirection == dirW and freeW and not agentinNE:
                nextdirection = randdirection
            if randdirection == dirE and freeE and not agentinNW:
                nextdirection = randdirection

        if nextdirection == dirNotSetYet and agentinSE and iteminSW and not agentinNW:
            # Move left or right
            randdirection = random.choice((dirStand, dirE))
            nextdirection = dirStand
            if randdirection == dirE and freeE:
                nextdirection = randdirection

        if nextdirection == dirNotSetYet and agentinSW and iteminSE and not agentinNE:
            # Move left or right
            randdirection = random.choice((dirStand, dirW))
            nextdirection = dirStand
            if randdirection == dirW and freeW:
                nextdirection = randdirection

        if nextdirection == dirNotSetYet and freeSE and iteminSW and not agentinNE and freeW:
            # Move left
            nextdirection = dirW

        if nextdirection == dirNotSetYet and freeSW and iteminSE and not agentinNW and freeE:
            # Move left
            nextdirection = dirE

    # CASE End: Agent is on the floor - Walk Left -Right - iteminSE and iteminSW  - and nothing is above it



    # CASE Begin: CLIMBING - Try climb NW, then try climb NE. Must be free, and carrying nothing
    # climb on agent in W if possible AND no other agent is on top of you
    # if nextdirection == dirNotSetYet and (agentinW and freeNW) and agentinSW  and not agentinE and ((not agentinNE) or (agentinNE and agentinE)):
    #     nextdirection = dirNW

    # climb on agent in E if possible AND no other agent is on top of you
    if nextdirection == dirNotSetYet and (agentinE and freeNE) and agentinSE and not agentinW and ((not agentinNW) or (agentinNW and agentinW)):
        nextdirection = dirNE
    # CASE Begin: CLIMBING - Try climb NW, then try climb NE. Must be free, and



    # CASE Begin: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NE, walk E
    if nextdirection == dirNotSetYet and agentinSW and agentinSE and freeE and agentinNE and not agentinNW:
        nextdirection = dirE  # freeE is True
    # CASE End: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NW, walk W
    # Why not also case for W?
    if nextdirection == dirNotSetYet and agentinSW and agentinSE and freeW and agentinNW and not agentinNE:
        nextdirection = dirStand
    # CASE End: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NE, walk E

    if nextdirection == dirNotSetYet and freeNE and freeE and agentinSE and not agentinNW:
        nextdirection = dirE  # freeE is True

    # if nextdirection == dirNotSetYet and freeNW and freeW and agentinSW and not agentinNE:
    #     nextdirection = dirW  # freeW is True




    # CASE Begin: TOWER SHIFT LEFT AND RIGHT
    # if standing only on agent in SE, check whether we need to move to E
    if nextdirection == dirNotSetYet and agentinSE and not agentinSW and freeE and not agentinNW and not agentinW:
        nextdirection = dirE
    #
    # if nextdirection == dirNotSetYet and agentinSW and not agentinSE and freeW and not agentinNE:
    #     yposition = agent.coordinates[1]
    #     nextdirection = dirW
    # CASE END: TOWER SHIFT LEFT AND RIGHT




    # This will move all to the EAST
    myDistanceplusone = agents_and_distances[agent]
    myDistanceplusone = myDistanceplusone + 2
    myRatioplusone = myDistanceplusone / maxDistance
    if agents_and_distances[agent] == maxDistance and agentinSE and freeE and myRatioplusone < beta:
        nextdirection = dirE
        # print("Walk Bridge End: Going East:", agent, agents_and_distances[agent], maxDistance, myRatiominusone, alpha)


    if agentinW and freeSW and freeSE:
        nextdirection = dirStand
    elif agentinSW and not agentinE and freeSE and freeNW and freeNE and agents_and_distances[agent] == maxDistance:
        nextdirection = dirSE
    myDistanceminusone = agents_and_distances[agent]
    myDistanceminusone = myDistanceminusone - 2
    myRatiominusone = myDistanceminusone / maxDistance
    if agentinSW and agentinE and freeNW and freeNE and freeSE and myRatiominusone >= alpha:
        nextdirection = dirSE
    if agentinSW and freeNW and freeNE and freeE and freeSE:
        nextdirection = dirSE

        # print("WalkBridgeEnd: Going SE:", agent, agents_and_distances[agent], maxDistance, myRatiominusone, alpha)

    # CASE Begin: FALLING Start  - freeSW and freeSE -   Check whether Agent needs to fall
    if freeSW and freeSE and not agentinE and not agentinW and not agentinNW and not agentinNE:
        yposition = agent.coordinates[1]
        # print("Walk bridge end: This agent ", agent, " is at X ", agent.coordinates[0], ", Y ", agent.coordinates[1]," : should fall")

        # We know already that this agent must fall, it will be in a zig (SE) - zag (SW) pattern, depending on the height (y - coordinate)
        if (yposition % 2) == 0:
            nextdirection = dirSW
        else:
            nextdirection = dirSE
    # CASE End: FALLING End  - freeSW and freeSE -   Check whether Agent needs to fall

    # if agents_and_distances[agent] == maxDistance and agentinW and freeNW and freeNE and freeE and freeSW and freeSE:
    #     nextdirection = dirSW
    # if agents_and_distances[agent] < maxDistance and agentinW and freeNW and freeNE and freeE and freeSW and agentinSE :
    #     nextdirection = dirSW

    if agentinW and freeNW and freeNE and freeE and freeSW:
        nextdirection = dirSW


    # CASE DEFAULT: If no direction selected, do not move
    if nextdirection == dirNotSetYet:
        nextdirection = dirStand

    # FINAL MOVE: if the agent is not falling currently, walk in the selected direction
    if nextdirection != dirNotSetYet:
        agent.move_to(nextdirection)

def walkDirected(agent):

    global iteminE, iteminW, iteminNE, iteminNW, iteminSE, iteminSW
    global agentinE, agentinW, agentinNE, agentinNW, agentinSE, agentinSW
    global freeW, freeE, freeNE, freeNW, freeSE, freeSW
    checkSurrounding(agent)

    dirNotSetYet = (0, 0, 1)
    nextdirection = dirNotSetYet  # characterizes an invalid state, will be changed later

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

            randdirection = planned_direction  # dirWalkPlan
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

    # CASE Begin: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NE, walk E
    if nextdirection == dirNotSetYet and agentinSW and agentinSE and freeE and agentinNE and not agentinNW:
        nextdirection = dirE  # freeE is True
        agent.planned_direction = dirE
    # CASE End: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NE, walk E
    # Why not also case for W?
    if nextdirection == dirNotSetYet and agentinSW and agentinSE and freeW and agentinNW and not agentinNE:
        nextdirection = dirW
        agent.planned_direction = dirW
    # CASE End: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NE, walk E

    if nextdirection == dirNotSetYet and freeNE and freeE and agentinSE and not agentinNW:
        nextdirection = dirE
        agent.planned_direction = dirE  # freeE is True

    # CASE Begin: CLIMBING - Try climb NW, then try climb NE. Must be free, and carrying nothing
    # climb on agent in W if possible AND no other agent is on top of you
    if nextdirection == dirNotSetYet and (agentinW and freeNW) and ((not agentinNE) or (agentinNE and agentinE)):
        nextdirection = dirNW

        # climb on agent in E if possible AND no other agent is on top of you
    if nextdirection == dirNotSetYet and (agentinE and freeNE) and ((not agentinNW) or (agentinNW and agentinW)):
        nextdirection = dirNE
    # CASE Begin: CLIMBING - Try climb NW, then try climb NE. Must be free, and

    # CASE Begin: TOWER SHIFT LEFT AND RIGHT
    # if standing only on agent in SE, check whether we need to move to E
    if (
            nextdirection == dirNotSetYet or nextdirection == dirStand) and agentinSE and not agentinSW and freeE and not agentinNW:
        nextdirection = dirE
        agent.planned_direction = dirE
        dirWalkPlan = dirE

    if (
            nextdirection == dirNotSetYet or nextdirection == dirStand) and agentinSW and not agentinSE and freeW and not agentinNE:
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
def calculateDistances(world):
    mydistances = {}
    maxDistance = 0
    debugon = False
    if debugon:
        print("calculate dist world.get_agent_list() . length:", len(world.get_agent_list()))

    for agent in world.get_agent_list():

        # print("Iterating of the agents, current agent: ", agent)
        iteminE = agent.item_in(dirE)
        iteminW = agent.item_in(dirW)
        iteminSE = agent.item_in(dirSE)
        iteminSW = agent.item_in(dirSW)
        iteminNE = agent.item_in(dirNE)
        iteminNW = agent.item_in(dirNW)

        # Check if current agent has an item in the neighborhood
        if iteminE or iteminW or iteminNE or iteminSW or iteminNW or iteminSE:
            # print("Agent ", agent, " has an item in the near: E", iteminE, ", W", iteminW, ", SE", iteminSE, ", SW",
            #   iteminSW, ", NE", iteminNE, ", NW", iteminNW)
            # print("adding ", agent, " to mydistances dictionary with distance 1, current length: ", len(mydistances))
            mydistances[agent] = 1
            if (mydistances[agent] > maxDistance):
                    maxDistance = mydistances[agent]
            # print("added ", agent, " to mydistances dictionary with distance 1, current length: ", len(mydistances))

    # print("calculate distances: mydistances ", len(mydistances))

    # Now iterate as long as agents_and_distances is increasing, i.e. new agents are added:
    # The flag to repeat is set once a new agent has been added to the list.
    flagrepeatloop = True
    while flagrepeatloop:
        flagrepeatloop = False

        # Iterate over each agent, check whether it has a neighbor that is not yet in the list
        # if yes: add agent to list with distance: Neighboring node + 1

        for agent in world.get_agent_list():
            if agent in mydistances:
                currentAgentDist = mydistances[agent]

                allDirections = [dirE, dirW, dirSE, dirSW, dirNE, dirNW]

                for selectedDirection in allDirections:
                    if agent.agent_in(selectedDirection):
                        nbrAgentInDir = agent.get_agent_in(selectedDirection)
                        currentAgentDist = mydistances[agent]

                        # print("Agent ", agent, " has Nbr ", nbrAgentInDir, " which is in mydistance ", nbrAgentInDir in agents_and_distances)
                        # Check whether neighboring Agent is already in list with distances
                        if nbrAgentInDir in mydistances:
                            # If Nbr is in the list: Check if distance over currentNode is smaller
                            if currentAgentDist + 1 < mydistances[nbrAgentInDir]:
                                mydistances[nbrAgentInDir] = currentAgentDist + 1
                                flagrepeatloop = True
                                # print("improved OLD ", nbrAgentInDir, " in mydistances dictionary with distance", currentAgentDist + 1)

                        else:
                            # If Nbr is not in the list: add to list with distance + 1
                            mydistances[nbrAgentInDir] = currentAgentDist + 1
                            flagrepeatloop = True
                            # print("added NEW ", nbrAgentInDir, " to mydistances dictionary with distance", currentAgentDist + 1)


    # Now you have a dictionary agents_and_distances where keys are agents and values are distances.
    # for agent, distance in mydistances.items():
        # print("Round:", world.get_actual_round(), " Agent:", agent, "Distance:", distance)
        # Move the agent according to the calculated distance


    return mydistances


def set_rainbow_color(agent, myDist, maxDist):
    agentCount = len(agent.world.agents)
    myDist
    agentMaxDist = maxDist

    # Saturation and Value are set to 1 for full color
    saturation = 1.0
    value = 1.0

    # Normalize myDist to a value between 0 and 1
    normalized_dist = 0
    normalized_dist = myDist / agentMaxDist

    # Convert the normalized value to a hue in the HSV color space
    hue = normalized_dist
    rgba = (0.0,0.0,0.0,1.0)


    # Convert HSV to RGB
    try:
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        rgba = (rgb[0], rgb[1], rgb[2], 1.0)
        print("Success: myDist", myDist, "Max", agentMaxDist, "Hue ", hue, "Saturation", saturation, "Value", value, "RGBA", rgba)
    except:
        print("Failed: myDist", myDist, "Max", agentMaxDist, "Hue ", hue, "Saturation", saturation, "Value", value, "RGBA", rgba)
    # Convert RGB to RGBA by adding an alpha value of 1.0


    # Set the color of the agent
    agent.set_color(rgba)
