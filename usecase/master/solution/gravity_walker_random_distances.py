import math
import random

def solution(world):
    minAgentHeight = 0
    maxAgentHeight = 0
    stopiftowerbuilt = False

    if world.get_actual_round() % 1 == 0:


        # Step 1: - Calculate for each agent: the distance of that agent to an item.
        #         -
        dirNE = (0.5, 1, 0)
        dirNW = (-0.5, 1, 0)
        dirSE = (0.5, -1, 0)
        dirSW = (-0.5, -1, 0)
        dirW = (-1, 0, 0)
        dirE = (1, 0, 0)
        dirStand = (0, 0, 0)

        # - Label Location of each item as distance = 0
        # - Label location of each Neighbor Position of Item as Distance = 1

        agents_and_distances = {}

        # Iterate over each agent: If there is an item in the neighborhood, set the distance of the agent to 1.
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
                #print("Agent ", agent, " has an item in the near: E", iteminE, ", W", iteminW, ", SE", iteminSE, ", SW",
                   #   iteminSW, ", NE", iteminNE, ", NW", iteminNW)

                agents_and_distances[agent] = 1

        # Now iterate as long as agents_and_distances is increasing, i.e. new agents are added:
        # The flag to repeat is set once a new agent has been added to the list.
        flagrepeatloop = True
        while flagrepeatloop:
            flagrepeatloop = False

            # Iterate over each agent, check whether it has a neighbor that is not yet in the list
            # if yes: add agent to list with distance: Neighboring node + 1

            for agent in world.get_agent_list():
                if agent in agents_and_distances:
                    currentAgentDist = agents_and_distances[agent]

                    allDirections = [dirE, dirW, dirSE, dirSW, dirNE, dirNW]

                    for selectedDirection in allDirections:
                        if agent.agent_in(selectedDirection):
                            nbrAgentInDir = agent.get_agent_in(selectedDirection)

                            # Check whether neighboring Agent is already in list with distances
                            if nbrAgentInDir in agents_and_distances:
                                # If Nbr is in the list: Check if distance over currentNode is smaller
                                if currentAgentDist + 1 < agents_and_distances[nbrAgentInDir]:
                                    agents_and_distances[nbrAgentInDir] = currentAgentDist + 1
                                    flagrepeatloop = True
                            else:
                                # If Nbr is not in the list: add to list with distance + 1
                                agents_and_distances[nbrAgentInDir] = currentAgentDist + 1
                                flagrepeatloop = True

        # Now you have a dictionary agents_and_distances where keys are agents and values are distances.
        for agent, distance in agents_and_distances.items():
            print("Round:", world.get_actual_round(), " Agent:", agent, "Distance:", distance)
            # Move the agent according to the calculated distance
           # agent.move_to(dirE)  # Example: Move all agents to the east



        # Agents have computed their distances, info in: agents_and_distances
        # Calculate max distance (maxdist)
        # Compute for each agent its ratio = own-distance / max distance
        # Plan movement of agents based on ratio to allow for swinging tentacles





        # From here we focus on the movement of each agent
        for agent in world.get_agent_list():
            # calculate for this specific agent it ratio = own-distance / max-distance
            # print(world.get_actual_round(), " Agent No.", agent.number, "  Coordinates", agent.coordinates, " Height", agent.coordinates[1], "  Number of Agents", world.get_amount_of_agents())

            if agent.coordinates[1] > maxAgentHeight:
                maxAgentHeight = agent.coordinates[1]
            if agent.coordinates[1] < minAgentHeight:
                minAgentHeight = agent.coordinates[1]

            dirNE = (0.5, 1, 0)
            dirNW = (-0.5, 1, 0)
            dirSE = (0.5, -1, 0)
            dirSW = (-0.5, -1, 0)
            dirW = (-1, 0, 0)
            dirE = (1, 0, 0)
            dirStand = (0, 0, 0)

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

            dirNotSetYet = (0, 0, 1)
            nextdirection = dirNotSetYet  # characterizes an invalid state, will be changed later

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
            if nextdirection == dirNotSetYet and agentinSW and agentinSE and freeW and agentinNW and not agentinNE:
                nextdirection = dirW
            # CASE End: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NE, walk E

            if nextdirection == dirNotSetYet and freeNE and freeE and agentinSE and not agentinNW:
                nextdirection = dirE  # freeE is True

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
            if nextdirection == dirNotSetYet and agentinSE and not agentinSW and freeE and not agentinNW:
                nextdirection = dirE

            if nextdirection == dirNotSetYet and agentinSW and not agentinSE and freeW and not agentinNE:
                yposition = agent.coordinates[1]
                nextdirection = dirW
            # CASE END: TOWER SHIFT LEFT AND RIGHT

            # CASE DEFAULT: If no direction selected, do not move
            if nextdirection == dirNotSetYet:
                nextdirection = dirStand

            # FINAL MOVE: if the agent is not falling currently, walk in the selected direction
            if nextdirection != dirNotSetYet:
                agent.move_to(nextdirection)

        # For next step: define the goal of the simulation, e.g. to build a tower of 6 agents and then terminate the simulation

        towerheight = maxAgentHeight - minAgentHeight + 1
        print("Round: ", world.get_actual_round(), "MaxHeight: ", maxAgentHeight, "Minheight: ", minAgentHeight,
              "Towerheight: ", towerheight, "  Agent No.", agent.number, "  Coordinates", agent.coordinates,
              " Height", agent.coordinates[1], "  Number of Agents", world.get_amount_of_agents())

        TowerHasBeenBuilt = (towerheight == world.get_amount_of_agents())
        if TowerHasBeenBuilt and stopiftowerbuilt:
            world.set_successful_end()
