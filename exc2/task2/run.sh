#!/bin/sh

hadoop jar /opt/hadoop/hadoop-0.20.2/contrib/streaming/hadoop-0.20.2-streaming.jar -input /user/s1250553/ex2/task1/large -output /user/s1140740/task_2.out -mapper mapper.py -file "`dirname $0`/mapper.py" -reducer reducer.py -file "`dirname $0`/reducer.py" -file "`dirname $0`/terms.txt" -jobconf mapred.reduce.tasks=1
