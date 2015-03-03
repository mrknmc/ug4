CC=gcc
CFLAGS=-g -Wall
OBJ=aquadsequential.o

aquadsequential: $(OBJ)
		gcc -o bin/$@ $^ $(CFLAGS) -lm

clean:
	rm aquadsequential *.o
