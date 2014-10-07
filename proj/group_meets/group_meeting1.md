% Storm on multicore
% Mark Nemec
% October 8, 2014

### What is Storm?

 * Real-time distributed computation framework
 * Defined in terms of a topology using spouts and bolts
 * Programming language agnostic
 * Fault-tolerant

![](topology.png)

<div class="notes">

 * Storm is a real-time distributed computation network.
 * Computation is defined in terms of a topology which consists of spouts which represent data streams and bolts which can perform map and reduce operations on these streams.
 * Storm is programming language agnostic due to Apache Thrift, which means you can define spouts and bolts in any language supported by Thrift.
 * Storm is fault-tolerant. When a work dies, it restarts it. When a node dies it starts the workers on a different node.

</div>

---

### Example Topology

> Spout -> Bolt 1 -> Bolt 2

 * Spout generates random sentences.
 * First bolt splits the sentence into words.
 * Second bolt counts the word occurrences.

![](tuple_tree.png)

<div class="notes">

 * Here is an simple example topology where we have a spout generating random sentences.
 * Next we have a bolt which splits the sentence into words and emits those.
 * Lastly we have a spout which counts the occurrences of words.
 * There is a daemon called acker which informs the master node when a tuple has been fully processed or if it failed to get processed.

</div>

---

### What is my project about?

> Borrowing ideas from Storm and applying them in the context of multi-core CPUs.

 * Perform parallel computation on a single multi-core server.
 * Complete control over computation, no need to rent clusters in a data centre.
 * Remove overhead from nodes communicating across a cluster.
 * Could be used as a running task within a Storm cluster.

<div class="notes">

 * The aim of my project is to be able to perform similar computations on a single server with a multi-core CPU. Storm already has a local mode but it's not optimized for single server - it is useful for development and testing but otherwise it is a mere cluster simulator.
 * It allows you to have complete control over your computation without having to own a data centre.
 * 

</div>

---

### My plan

 * Change as little code as possible
 * Find functionality that needs to be stripped.
 * 

---

### Timeline

 1. ~~Learn how to use Storm~~
 2. Trim down the code base
 3. 

---

# Thank you for attention.

 * 
