# Architecture of Storm

## Clojure

### backtype.storm.command

Contains commands to send to Nimbus. For example `activate`, `deactivate`, `killTopology` etc.

### backtype.storm.daemon

#### acker

This is a daemon that tracks whether a tuple can be ack-ed. It checks the tuple's dependency acyclic graph (DAG) and when it sees that it is complete, it notifies the spout that had produced the tuple that the tuple was processed.

Apparently contains some crazy algorithm that tracks the tuples. See more here [https://storm.incubator.apache.org/documentation/Guaranteeing-message-processing.html](https://storm.incubator.apache.org/documentation/Guaranteeing-message-processing.html).

Has a `RotatingMap` which contains a bucket of Java `HashMap`s. All is explained in the link above.

`acker` is just a bolt defined with `mk-acker-bolt`.

#### builtin-metrics

Metrics data structures and facade methods used throughout the project.

#### common

Common functions used throughout the project.

#### drpc

Contains code for Distributed Remote Procedure Call (DRPC).

See more here [https://storm.incubator.apache.org/documentation/Distributed-RPC.html](https://storm.incubator.apache.org/documentation/Distributed-RPC.html).

#### executor

An executor is a single thread of execution, potentially executing multiple tasks belonging to the same component (`Bolt` or `Spout`). Executor is directly tied to this component, only executing tasks belonging to the component.

#### logviewer

Access logfiles of specific workers.

#### nimbus

Contains code for the master node, Nimbus.

#### task

A task is a "unit of data processing", i.e. where the actual code is executed. It is directly tied to an executor and it is an "execution unit of a component". There can be more tasks within one executor but the default is to have 1:1.

#### worker

A worker is an abstraction around a JVM. For one topology there are multiple workers spread across the cluster. One machine will have multiple workers running on it (potentially belonging to different clusters).

### backtype.storm.messaging

#### loader

Contains the definition of a receiving thread which is a thread listening on the worker port. It puts incoming messages on an incoming queue.

See more [http://www.michael-noll.com/blog/2013/06/21/understanding-storm-internal-message-buffers/](http://www.michael-noll.com/blog/2013/06/21/understanding-storm-internal-message-buffers/).

#### local

TODO

### backtype.storm.metric

#### testing

TODO

### backtype.storm.scheduler

There be dragons here.

#### DefaultScheduler

TODO

#### EvenScheduler

TODO

#### IsolationScheduler

TODO

### backtype.storm.ui

#### core

TODO

#### helpers

TODO

### backtype.storm

#### bootstrap

Bootstrapping the imports of many components into a macro.

#### clojure

Clojure DSL for implementing bolts and spouts.

#### cluster

Functionality related to the state of the cluster. ZooKeeper passing around stuff from master to nodes.

#### config

Configuration of the topology etc.

#### disruptor

Wrappers around LMAX Disruptor (queueing system).

#### event

TODO

#### LocalCluster

Cluster when ran locally (development mode).

#### LocalDRPC

DRPC when ran locally (development mode).

#### log

Logging facilities.

#### process_simulator

Simulates a process (for testing purposes).

#### stats

Statistical methods.

#### testing

Pretty self-explanatory.

#### testing4j

Pretty self-explanatory.

#### thrift

TODO

#### timer

Very similar to `java.util.Timer`, except it integrates with Storm's time simulation capabilities.

#### tuple

Contains one function that produces a list hashCode.

#### util

Utilities used all over the place.

#### zookeeper

Zookeeper wrapper.

## Dev

Contains storm implementations which can be used to write Spouts and Bolts in other languages.

## JVM

### backtype.storm.clojure

Contains wrapper around Clojure DSL Bolt and Spout definitions.

### backtype.storm.coordination

TODO

### backtype.storm.daemon

Contains the Shutdownable interface.

### backtype.storm.drpc

DRPC stuff.

### backtype.storm.grouping

Contains CustomStreamGrouping interface.

### backtype.storm.hooks

Hooks that can do things when certain events happen.

### backtype.storm.messaging

TODO.

### backtype.storm.metric

More metrics.

### backtype.storm.multilang

Stuff used when defining bolts and spouts in other languages than Java.

### backtype.storm.nimbus

Validation of topologies.

### backtype.storm.planner

Not used anywhere?

### backtype.storm.scheduler

TODO

### backtype.storm.security

Security stuff.

### backtype.storm.serialization

Serializers/Deserializers.

### backtype.storm.spout

Spout interfaces.

### backtype.storm.state

Not supported yet?

### backtype.storm.task

Mainly bolt interfaces.

### backtype.storm.testing

Testing.

### backtype.storm.topology

Base classes for components and TopologyBuilder.

### backtype.storm.transactional

TODO

### backtype.storm.tuple

Basic unit of emitable data.

### backtype.storm.ui

One exception is here.

### backtype.storm.utils

Utilities. So many of them.

### backtype.storm

#### Config

Configuration constants.

#### ConfigValidation

Configuration validation.

#### Constants

String constants.

#### StormSubmitter

Used to submit a topology to a cluster.

## Multilang

Contains storm implementations which can be used to write Spouts and Bolts in other languages.

## Py

Generated by thrift.

## UI

Storm web UI.
