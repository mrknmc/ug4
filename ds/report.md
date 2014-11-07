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
