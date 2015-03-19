/*
 * FARMER ALGORITHM:
 * - State of workers is tracked in a boolean array called working.
 * - Number of idle workers is tracked in an int var called workers.
 * - Initial range [A B] is put on the stack.
 * - Iterations of the algorithm are perfomed until termination. The algorithm
 *   terminates when the stack is empty and all workers are idle.
 * - In every iteration of the algorithm, ranges are popped from the stack and
 *   sent to idle workers in a an array [l r].
 * - Once (or if) the stack is empty or there are no idle workers the farmer
 *   tries to receive a message.
 * - If the message contains two new ranges, these are put on the stack and
 *   next iteration of the algorithm is executed.
 * - Otherwise if the message contains the result within EPSILON accuracy, the
 *   result is added to the running total.
 * - In any case, the worker becomes idle and is ready to receive another
 *   range.
 * - Once the algorithm terminates, messages are sent to the workers to inform
 *   them about termination.
 *
 * WORKER ALGORITHM:
 * - status.MPI_TAG signifies whether a message is a terminating message or a
 *   message defining new range.
 * - The worker continuously listens to messages.
 * - If the message has MPI_TAG == 0 that is the signal to break out of the
 *   loop.
 * - Otherwise the message contains a definition of a new range. The algorithm
 *   for Adaptive Quadrature is executed.
 * - If the result is within EPSILON the result is sent back.
 * - Otherwise a definition for two new ranges is sent back.
 * - The ranges are sent back as an array of three values [l m r]. This defines
 *   two new ranges [l m] and [m r].
 *
 * NOTES:
 * - MPI_Send is used to send the terminating messages. MPI_Bcast could not be
 *   used to send the messages because workers would need to call MPI_Bcast as
 *   well and the workers need to receive ranges with MPI_Recv to perform the
 *   algorithm.
 * - MPI_Send is used to send messages containing new range definitions.
 * - Alternatively MPI_ISend or any other type of sends could have been used
 *   but MPI_Send was chosen to simplify implementation. The same applies to
 *   MPI_Recv over its alternatives.
 *
 * */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <mpi.h>
#include "stack.h"

#define EPSILON 1e-3
#define F(arg)  cosh(arg)*cosh(arg)*cosh(arg)*cosh(arg)
#define A 0.0
#define B 5.0

#define SLEEPTIME 1

int *tasks_per_process;

double farmer(int);

void worker(int);

int main(int argc, char **argv ) {
  int i, myid, numprocs;
  double area, a, b;

  MPI_Init(&argc, &argv);
  MPI_Comm_size(MPI_COMM_WORLD,&numprocs);
  MPI_Comm_rank(MPI_COMM_WORLD,&myid);

  if(numprocs < 2) {
    fprintf(stderr, "ERROR: Must have at least 2 processes to run\n");
    MPI_Finalize();
    exit(1);
  }

  if (myid == 0) { // Farmer
    // init counters
    tasks_per_process = (int *) malloc(sizeof(int)*(numprocs));
    for (i=0; i<numprocs; i++) {
      tasks_per_process[i]=0;
    }
  }

  if (myid == 0) { // Farmer
    area = farmer(numprocs);
  } else { //Workers
    worker(myid);
  }

  if(myid == 0) {
    fprintf(stdout, "Area=%lf\n", area);
    fprintf(stdout, "\nTasks Per Process\n");
    for (i=0; i<numprocs; i++) {
      fprintf(stdout, "%d\t", i);
    }
    fprintf(stdout, "\n");
    for (i=0; i<numprocs; i++) {
      fprintf(stdout, "%d\t", tasks_per_process[i]);
    }
    fprintf(stdout, "\n");
    free(tasks_per_process);
  }
  MPI_Finalize();
  return 0;
}

double farmer(int numprocs) {
  stack *stack = new_stack();
  double points[2];
  int working[numprocs];
  double result[3];
  double *points_p;
  double total = 0.0;
  MPI_Status status;
  int i;
  int who;
  int workers = numprocs - 1;

  for (i = 0; i < numprocs; i++) {
    working[i] = 0;
  }

  // 1. Place initial tasks into bag
  points[0] = A;
  points[1] = B;
  push(points, stack);

  while (!is_empty(stack) || workers < numprocs - 1) {
    for (i = 1; i < numprocs; i++) {
      // idle and stack not empty => Send
      if (0 == working[i] && !is_empty(stack)) {
        points_p = pop(stack);
        MPI_Send(points_p, 2, MPI_DOUBLE, i, 1, MPI_COMM_WORLD);
        working[i] = 1;
        tasks_per_process[i] += 1;
        workers--;
      }
    }
    // receive while you can
    MPI_Recv(result, 3, MPI_DOUBLE, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
    who = status.MPI_SOURCE;
    working[who] = 0;
    workers++;
    if (0 == status.MPI_TAG) {
      // result was within Epsilon, add to total
      total += result[0];
    } else {
      // put on stack
      push(result, stack);
      push(result + 1, stack);
    }
  }

  // Terminate all the workers
  for (workers = numprocs - 1; workers > 0; workers--) {
    MPI_Send(points_p, 2, MPI_DOUBLE, workers, 0, MPI_COMM_WORLD);
  }

  return total;
}

void worker(int mypid) {
  double points[2];
  double result[3];
  double fleft, fright, mid, fmid, larea, rarea, lrarea;
  MPI_Status status;

  while(1) {
    MPI_Recv(points, 2, MPI_DOUBLE, 0, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
    if (0 == status.MPI_TAG) {
      break;
    }
    fleft = F(points[0]);
    fright = F(points[1]);
    mid = (points[0] + points[1]) / 2;
    fmid = F(mid);
    larea = (fleft + fmid) * (mid - points[0]) / 2;
    rarea = (fmid + fright) * (points[1] - mid) / 2;
    lrarea = (fleft + fright) * (points[1] - points[0]) / 2;
    usleep(SLEEPTIME);
    if (fabs((larea + rarea) - lrarea) > EPSILON) {
      result[0] = points[0];
      result[1] = mid;
      result[2] = points[1];
      MPI_Send(result, 3, MPI_DOUBLE, 0, 1, MPI_COMM_WORLD);
    } else {
      result[0] = larea + rarea;
      MPI_Send(result, 3, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
    }
  }
}
