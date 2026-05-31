# Gravity

In this use case, the swarm agents are influenced by gravity. This means that each agent, given that they are not in a fixed state, moves to the south direction of the simulation space, which simulates them falling in the direction of the gravitational pull.
As the grid of the simulated world has no direct direction to the south, the agents fall in a zigzag pattern to the
south-west or south-east.

Agents are in a fixed state either when they are connected to a platform, or when they are connected to another agent which itself is in a fixed state.

## Gravity Swarm Algorithms

The scripts present in the directory `solutions` provide algorithms that declare how each agent of a swarm behaves under the gravity use case.
These algorithms provide possible solutions to the challenge of a swarm, initially placed on a starting island, having to find and traverse to other islands located in the simulation world.

In the context of spatial environments, particularly those influenced by gravity, the design and
evaluation of such swarm algorithms pose unique challenges. Gravity
constrains agent actions and influences the stability of collective formations,
such as towers or bridges, agents are effected by gravity when crossing gaps
in between platforms, and must build supporting structures.

Each solution algorithm possesses different characteristics in terms of evaluations criterias such as 
1. Temporal Efficiency: The total number of rounds until the goal is reached is a primary
measure of performance. A lower number of rounds indicates higher efficiency.
2. Resource Utilization: How the agents utilize resources (e.g., platforms) should also be
considered. Optimal resource utilization leads to faster goal achievement.
3. Degree of Cooperation: The degree of cooperation between the agents can serve as an
indicator of performance. Higher cooperation rates could lead to faster and more stable
solutions.
4. Solution Stability: Stability means that the structure formed by the agents does not collapse
without internal or external influences.

Different solution algorithms also differ in their ability to solve simulation scenarios. Some algorithms can solve scenarios which other algorithms can not solve, and vice versa.

## Gravity Simulation Scenarios
Under the directory `scenarios`, there are scripts which generate simulations worlds in which the different algorithms can be evaluated. The scenarios range from simple and idealized for the constraints of the swarm algorithms, to more complex and challenging in order to explore the limitations of each swarm algorithm's approach.