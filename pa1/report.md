---
title: 'Parallel Architecture, Assignment 1'
author: 'Mark Nemec, s1140740'
abstract: 'Paper C: "Superspeculative Microarchitecture for Beyond AD 2000", M. H. Lipasti and J. P. Shen, IEEE Computer, vol. 30, no. 9, September 1997'
---

# Superspeculative Microarchitecture for Beyond AD 2000

## Description

The paper describes class of techniques termed superspeculative and provides an implementation of these techniques in a microarchitecture called Superflow. It claims that this new paradigm gets performance increases over top-of-the-line microprocessors of the time by predicting values produced by producer instructions and executing consumer instructions before the values become known.

Main reason to speculate about values of instructions is the classical dataflow limit for program performance:

 > _Given unlimited machine resources, a program cannot execute any faster than the execution of the longest dependence chain induced by the program's true data dependences._

This means that even with a very wide conventional superscalar the performance is limited by the serialisation of producer and consumer instructions. The only way to speed up the execution is to try to predict values before they become known. If the prediction is successful, this "breaks" the serialisation.

At the time, most machines adopted a strong-dependence model. This model specifies that instructions are possibly executed out-of-order but only if there is no dependence. What this means that dependences between instructions are never violated. The authors claim that this model is "too rigorous and unnecessarily restricts available parallelism".

To be able to predict operands of consumer instructions, the authors propose a weak-dependence model. In this model the machine can temporarily violate dependences and speculate about operand values as long as it can recover from misspeculations. If a substantial number of predictions is correct, the paper claims that the machine can outperform, traditional strong-dependence machines.

## Results

In Superflow, the authors implemented superspeculative techniques that improve instruction flow, register dataflow and memory dataflow. They claim that the techniques frequently more than double the performance of a conventional superscalar processor. In fact, Superflow has a potential performance of 9 instructions per cycle and simulations yielded 7.3 IPC for the SPECint95 benchmark suite. These results were possible without recompilation or changes to the ISA.

![Benchmarks \label{benchmarks}](benchmarks.png "Benchmarks")

## Discussion



# A Single-Chip Multiprocessor

## Description

## Results

## Discussion
