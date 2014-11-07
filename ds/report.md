---
title: 'Distributed Systems Assignment'
author: 's1140740'
---

# 2.1

> **Proof**: If V is a vector clock, prove that $a \rightarrow b \iff V(a) \leq V(b)$.

## $a \rightarrow b \implies V(a) \leq V(b)$

There are three possibilities:

 1. Event b was a local event of a process i, by definition $V(b)[i] += V(b)[i] + 1$

 2. Event b was a send message event of a process i.
 3. Event b was a receive message event of a process i.

## $V(a) \leq V(b) \implies a \rightarrow b$

# 2.2

Liveness means that every request for critical section (CS) is eventually granted.

When a process i wants to request access to CS, it will send a REQUEST message with their id and current timestamp to all processes and add the message to its own queue. Assuming all channels are FIFO and there are no failures in channels all processes will send a timestamped REPLY message and add the message received into its own queue.

---

Process `i` decides to use the resource, it sends a `REQUEST` message, puts its own request into its queue and gets a `REPLY` message from every other process (no channel failures assumption). Now let's assume that process `i`'s request never gets satisfied. This means that its request never reaches the top of its queue (if it did, the request would get satisfied as per the algorithm). This is clearly impossible under the assumption that all accesses are _not indefinite_. This is because every time a process finishes accessing the resource it sends a `RELEASE` message to all other processes at which point those processes pop that process's request from their queue. This is guaranteed to happen due to the no process and channel failures assumption.

---

Induction on the position of the request in the queue.

Base case:

Request is at the top of the queue => it gets satisfied.

Induction hypothesis: If our request eventually gets satisfied at position $k$, it also gets satisfied if we are at position $k + 1$.

Our request is at position $k + 1$. Let the request at first position belong to process $i$ and let us call the request $R_i$. Since $R_i$ is at the first position in the queue, all the previous processes accessing the resource are finished with it, otherwise we would have their requests in our queue before $R_i$ (we can only remove a request once we receive a `RELEASE` message for it). There are three options:

 1. Process $i$ is currently accessing the resource. Since we assume processes do not fail, this means that when it is done it will send us a `RELEASE` message and we will remove $R_i$ from our queue and our request will be in position $k$.
 2. Process `i` has finished accessing the resource but we have not yet received the `RELEASE` message. Channels do not fail so we will eventually receive the message and remove $R_i$ from our queue and our request will be in position $k$.
 3. Process `i` has not started accessing the resource. This implies that $R_i$ is not at the top of the queue of process $i$. However, since we have shown that no other process can be accessing the resource at this time

# 2.3

The weighted diameter of this graph is 7. The path realising this diameter is $A \rightarrow C \rightarrow E \rightarrow G \rightarrow H$.

If the graph was unweighted, the diameter would be 4 and the corresponding path would be $A \rightarrow C \rightarrow F \rightarrow G \rightarrow I$.

# 2.4

\begin{figure}
\begin{subfigure}[b]{0.3\textwidth}
\includegraphics[width=\textwidth]{prims/1.png}
\caption{Step 1}
\end{subfigure}
\begin{subfigure}[b]{0.3\textwidth}
\includegraphics[width=\textwidth]{prims/2.png}
\caption{Step 2}
\end{subfigure}
\begin{subfigure}[b]{0.3\textwidth}
\includegraphics[width=\textwidth]{prims/3.png}
\caption{Step 3}
\end{subfigure}
\begin{subfigure}[b]{0.3\textwidth}
\includegraphics[width=\textwidth]{prims/4.png}
\caption{Step 4}
\end{subfigure}
\begin{subfigure}[b]{0.3\textwidth}
\includegraphics[width=\textwidth]{prims/5.png}
\caption{Step 5}
\end{subfigure}
\begin{subfigure}[b]{0.3\textwidth}
\includegraphics[width=\textwidth]{prims/6.png}
\caption{Step 6}
\end{subfigure}
\begin{subfigure}[b]{0.3\textwidth}
\includegraphics[width=\textwidth]{prims/7.png}
\caption{Step 7}
\end{subfigure}
\begin{subfigure}[b]{0.3\textwidth}
\includegraphics[width=\textwidth]{prims/8.png}
\caption{Step 8}
\end{subfigure}
\begin{subfigure}[b]{0.3\textwidth}
\includegraphics[width=\textwidth]{prims/9.png}
\caption{Step 9}
\end{subfigure}
\caption{Prim's algorithm}
\end{figure}
