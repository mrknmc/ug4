# Turning Thrift Objects into normal classes

In original Storm, Bolt/Spout have ComponentCommon and ComponentObject. ComponentCommon can just be mapped. ComponentObject, however, needs to be turned into a class as there is no union (how it's represented in Thrift) in Java. In Thrift, ComponentObject can be either a binary array, ShellComponent or a JavaObject.

 - ShellSpout and ShellBolt have ShellComponent
 - ShellSpout and ShellBolt implement ISpout and IBolt
 - IRichSpout and IRichBolt extend ISpout, IBolt and IComponent
 - IBasicSpout and IBasicBolt extend IComponent
 - BaseRichSpout and BaseRichBolt extend BaseComponent and implement IRichSpout and IRichBolt
 - BaseBasicSpout and BaseBasicBolt extend BaseComponent and implement IBasicSpout and IBasicBolt
 
