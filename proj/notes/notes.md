# Turning Thrift Objects into normal classes

In original Storm, Bolt/Spout have ComponentCommon and ComponentObject. ComponentCommon can just be mapped. ComponentObject, however, needs to be turned into a class as there is no union (how it's represented in Thrift) in Java. In Thrift, ComponentObject can be either a binary array, ShellComponent or a JavaObject.

 - ShellSpout and ShellBolt have ShellComponent
 - ShellSpout and ShellBolt implement ISpout and IBolt
 - IRichSpout and IRichBolt extend ISpout, IBolt and IComponent
 - IBasicSpout and IBasicBolt extend IComponent
 - BaseRichSpout and BaseRichBolt extend BaseComponent and implement IRichSpout and IRichBolt
 - BaseBasicSpout and BaseBasicBolt extend BaseComponent and implement IBasicSpout and IBasicBolt
 
# Cluster state

Cluster state is created for every daemon. The state is then read at any of them for "snapshots". For example, Nimbus sets an assignmnet using the state and the `set-assignment!` zookeeper api and this is automatically available for the supervisor daemon and the `assignments` function call.

# Supervisor tasks

 - heartbeat to the cluster state
 - downloads the code
 - kill all workers that are not getting assignments anymore
 - reads an assignment and launches workers

# Worker tasks

 - heartbeat as well
 - make executors
 - launch a receive thread
 - transfer handler (to transfer data out) and its own thread
 - local transfer function (transfers from receive thread/queue to local executors)
 - transfer function (transfers from executors forwarded to either local or remote executors)
 - establishes connections with remote workers through mq-context

# Executor tasks

 - groups tuples onto tasks they should be sent to
 - have a handler for worker-transfer-fn to consume the batch-transfer-queue
 - publish on batch-transfer-queue which is consumed by thing above

# Task

 - tasks execute within one thread of an executor, sequentially
 - there is not much need for them

# What does executor need from the Worker

## Original Storm

 - worker-context
     + system-topology
     + component->sorted-tasks
     + component->stream->fields
     + port
     + task-ids
     + default-shared-resources
     + user-shared-resources
 - conf
 - storm-conf
 - executor-receive-queue-map
 - storm-id
 - storm-active-atom
 - suicide-fn
 - storm-cluster-state
 - task->component

## My Storm

 - worker-context
     + X system-topology
     + X component->sorted-tasks
     + X component->stream->fields
     + X uuid (maybe)
     + X task-ids
 - X conf
 - X storm-conf
 - X executor-receive-queue-map
 - X storm-id
 - storm-active-atom (maybe not)
 - X suicide-fn
 - X storm-cluster-state
 - X task->component

