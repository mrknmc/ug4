
END=2;

for task in $(seq 1 $END); do
    diff -r "task$task/output" "samples/task$task"
    if [[ $? == 0 ]]; then
        echo "Task $task passes."
    else
        echo "Task $task output differs."
    fi
done
