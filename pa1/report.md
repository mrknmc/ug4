---
title: 'Parallel Architecture, Assignment 1'
author: 'Mark Nemec, s1140740'
abstract: 'Paper C: "Superspeculative Microarchitecture for Beyond AD 2000", M. H. Lipasti and J. P. Shen, IEEE Computer, vol. 30, no. 9, September 1997'
---

# Superspeculative Microarchitecture for Beyond AD 2000

## Description

The paper describes class of techniques termed superspeculative and provides an implementation of these techniques in a microarchitecture called Superflow. It claims that this new paradigm gets performance increases over top-of-the-line microprocessors of the time by predicting values produced by producer instructions and executing consumer instructions before the values become known. Moreover, the authors claim that they can achieve this performance improvement without sacrificing code compatibility.

The main idea of a superspeculative microarchitecture is that producer instructions generate many predictable values in real programs and one can thus speculate about values of the operands of their consumer instructions and begin their execution without results from producer instructions. 

Another reason to speculate about values of instructions is the classical dataflow limit for program performance:

 > "_Given unlimited machine resources, a program cannot execute any faster than the execution of the longest dependence chain induced by the program's true data dependences._"

This means that even with a very wide conventional superscalar the performance is limited by the serialisation of producer and consumer instructions. The only way to speed up the execution is to try to predict values before they become known. If the prediction is successful, this "breaks" the serialisation.

At the time, most machines adopted a strong-dependence model. This model specifies that instructions are possibly executed out-of-order but only if there is no dependence. What this means that dependences between instructions are never violated. However, there are cases when it may appear that there is a dependence even when there is not.The paper claims that this model is "too rigorous and unnecessarily restricts available parallelism" <!-- quote? -->.

To be able to predict operands of consumer instructions, the paper proposes a weak-dependence model. In this model the machine can temporarily violate dependences as long as it can recover from misspeculations. If a substantial number of predictions is correct, the paper claims that the machine can outperform, traditional strong-dependence machines.

## Results

The authors implemented the techniques discussed in a microarchitecture called Superflow. 

## Discussion

# A Single-Chip Multiprocessor

## Description

## Results

## Discussion
