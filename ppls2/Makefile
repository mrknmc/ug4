CC=gcc

aquadsequential: aquadsequential.o
		gcc -o $@ $^ $(CFLAGS) -lm

stack: stack.o
	gcc -o $@ $^ $(CFLAGS) -lm

aquadPartA: aquadPartA.o stack
	/usr/lib64/openmpi/bin/mpicc -o $@ $^

clean:
	rm aquadsequential *.o
