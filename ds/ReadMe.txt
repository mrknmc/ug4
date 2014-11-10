# Simulator Design
All the code that executes base station's commands such as starting discovery is in the file `base_station.py`. The high level code for the algorithm is in the `main` function on `sim.py`. This file also contains function `parse_file` which parses the file. File `models.py` contains models of components used in the simulation. `Coords` represents location of a node. `Event` represents an event that should be logged. `Message` represents a type of message being sent. `Edge` represents an undirected edge in the graph and `Network` is an abstraction of the wireless network that allows access to nodes by id or coordinates. File `util.py` contains utility functions such as computing the Euclidean distance, reversing an Edge or computing the energy cost. An object representing a node in the network and all its methods such as receiving a message and finding the minimum weight outgoing edge (MWOE) are in the file `node.py`.

# MST Algorithm
I assumed that message sending in the network is synchronous. That is when a message is sent, a response is returned right away (in reality it would be after a certain delay). Furthermore, rather than implementing a global clock, nodes send and receive message as they come along. This means that reimplementing this algorithm with asynchronous messaging would be simple. In general, the synchronicity of the algorithm is kept in place and everything within a connected component happens in correct order.

Firstly, my algorithm starts with the base station telling all nodes to find their neighbours. I assume that the only thing nodes know about their neighbours are their coordinates.

Secondly, the base station informs the leaders to start the MST construction. Each leader then forwards a message to find the MWOE to its children and finds its own MWOE. A node finds its MWOE by sending a message through all the outgoing edges to neighbours that are not children of the node and have not been rejected yet. Neighbours respond to this message with their leader's id and they are either rejected if it is the same (they had to be added to the same component by some other node) or they are considered otherwise. Recursion is used to simulate a convergecast and the minimum weight edge is chosen out of all possible MWOEs by the leader.

Thirdly, the leader uses a broadcast to inform the node that has the chosen MWOE that it should add the edge when merging occurs. The node informs the node on the other side of the edge so it can add the edge in the merging stage as well.

Finally, the base station informs the leaders to start the merging phase. In this phase, the leaders start a broadcast with their id and the leader with the highest id in the component is selected as a new leader of the connected component. Furthermore, any outstanding edges chosen in the previous phase to be added to the component are added. When this phase is over for all leaders, the base station checks who the leaders in the next level are going to be (subset of previous leaders) and starts the next round of the algorithm. The algorithm is over when the leaders do not change.

# Broadcast strategy
My strategy for keeping nodes alive is to reconstruct the MST after every broadcast. Thus if a certain node dies its edges will be replaced by edges through some other nodes.

Nodes forward the messages and when they die they inform nodes they have an edge to. These nodes remove their edge to the dead node and then the node is removed from the network. Next time MST is constructed the node will thus not be connectible.
