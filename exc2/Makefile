# Produce PDFs from all Markdown files in a directory
# Lincoln Mullen | http://lincolnmullen.com | lincoln@lincolnmullen.com

# List files to be made by finding all *.md files and appending .pdf

.PHONY: task1 task2 task3.1 task3.2 task3.3 task4.1 task4.2 task4.3

PY_FILES := $(wildcard *.py)
TASKS := $(wildcard task*)

GET=hadoop dfs -get
CP=hadoop dfs -cp
EXE=hadoop jar /opt/hadoop/hadoop-0.20.2/contrib/streaming/hadoop-0.20.2-streaming.jar
OUT_DIR=/user/s1140740
IN_DIR=/user/s1250553/ex2
OPTS=-mapper mapper.py -reducer reducer.py -file $@/mapper.py -file $@/reducer.py


all:	clean task1 task2 task3.1 task3.2 task3.3

task1:
		hadoop dfs -rmr $(OUT_DIR)/task_1.out
		$(EXE) -input $(IN_DIR)/task1/large -output $(OUT_DIR)/task_1.out $(OPTS) \
								-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
								-jobconf map.output.key.field.separator=' ' \
								-jobconf num.key.fields.for.partition=1
		rm -rf $@/out
		$(GET) $(OUT_DIR)/task_1.out $@/out

task2:
		hadoop dfs -rmr $(OUT_DIR)/task_2.out
		$(EXE) -input $(IN_DIR)/task1/large -output $(OUT_DIR)/task_2.out $(OPTS) \
								-file $@/terms.txt \
								-jobconf mapred.reduce.tasks=1
		rm -rf $@/out
		$(GET) $(OUT_DIR)/task_2.out $@/out

task3.1:
		hadoop dfs -rmr $(OUT_DIR)/task_3.1.out	
		$(EXE) -input $(IN_DIR)/task2/logsSmall.txt -output $(OUT_DIR)/task_3.1.out $(OPTS) 
		rm -rf $@/out
		$(GET) $(OUT_DIR)/task_3.1.out $@/out

task3.2:
		hadoop dfs -rmr $(OUT_DIR)/task_3.2.out
		$(EXE) -input $(IN_DIR)/task2/logsSmall.txt -output $(OUT_DIR)/task_3.2.out $(OPTS)
		rm -rf $@/out
		$(GET) $(OUT_DIR)/task_3.2.out $@/out

task3.3:
		hadoop dfs -rmr $(OUT_DIR)/task_3.3.out
		$(EXE) -input $(IN_DIR)/task2/logsSmall.txt -output $(OUT_DIR)/task_3.3.out $(OPTS) \
							-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
							-jobconf map.output.key.field.separator=' ' \
							-jobconf num.key.fields.for.partition=1 
		rm -rf $@/out
		$(GET) $(OUT_DIR)/task_3.3.out $@/out

task4.1:
		hadoop dfs -rmr $(OUT_DIR)/task_4.1.out
		$(EXE) -input $(IN_DIR)/task3/stackSmall.txt -output $(OUT_DIR)/task_4.1.out $(OPTS)
		rm -rf $@/out
		$(GET) $(OUT_DIR)/task_4.1.out $@/out

task4.2:
		hadoop dfs -rmr $(OUT_DIR)/task_4.2.out
		$(EXE) -input $(IN_DIR)/task3/stackSmall.txt -output $(OUT_DIR)/task_4.2.out $(OPTS)
		rm -rf $@/out
		$(GET) $(OUT_DIR)/task_4.2.out $@/out

task4.3:
		hadoop dfs -rmr $(OUT_DIR)/task_4.3.*
		$(EXE) -input $(IN_DIR)/task3/stackSmall.txt -output $(OUT_DIR)/task_4.3.tmp.out $(OPTS) \
						-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
						-jobconf map.output.key.field.separator=' ' \
						-jobconf num.key.fields.for.partition=1 
		$(EXE) -input $(OUT_DIR)/task_4.3.tmp.out -output $(OUT_DIR)/task_4.3.out \
						-mapper cat \
						-reducer reducer2.py \
						-file $@/reducer2.py \
						-jobconf mapred.reduce.tasks=1
		rm -rf $@/out
		$(GET) $(OUT_DIR)/task_4.3.out $@/out

clean:
		hadoop dfs -rmr /user/s1140740/*

