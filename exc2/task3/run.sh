#!/bin/sh

hadoop jar /opt/hadoop/hadoop-0.20.2/contrib/streaming/hadoop-0.20.2-streaming.jar -input /user/s1250553/ex2/task1/small -output /user/s1140740/task_1.out -mapper mapper.py -file "`dirname $0`/mapper.py" -reducer reducer.py -file "`dirname $0`/reducer.py" -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner -jobconf map.output.key.field.separator=, -jobconf num.key.fields.for.partition=1
