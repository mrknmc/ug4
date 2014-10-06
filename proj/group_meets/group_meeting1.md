% Storm on multicore
% Mark Nemec
% October 8, 2014

### What is Storm?

 * Distributed computation framework
 * Realtime data processing
 * Defined in terms of a topology using spouts and bolts
 * Programming language agnostic

![](topology.png)

---

### Example Topology

> Spout -> Bolt 1 -> Bolt 2

 * A spout generates random sentences
 * First bolt splits the sentence into words
 * Second bolt counts the word occurences

![](tuple_tree.png)

---

### What is my project about?

> Borrowing ideas from Storm and applying them in the context of multicore CPUs.

 * Perform parallel computation on a single multi-core server
 * Complete control over computation, no need to rent clusters in a data centre
 * Remove overhead from nodes communicating across a cluster

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
