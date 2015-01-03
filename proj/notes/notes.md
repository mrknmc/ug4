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

# Executor tasks

<!-- what are executors responsible for? -->

# Task

<!-- what are tasks responsible for? -->
