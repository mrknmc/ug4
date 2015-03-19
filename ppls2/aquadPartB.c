/* FARMER ALGORITHM:
 * - The range [A B] is divided into N equal-sized chunks where N is the number
 *   of workers. Every chunk is sent to one worker using MPI_Send.
 * - Afterwards, the farmer listens for N messages. These messages contain area
 *   for every chunk which are then added up and reported as result.
 * - Furthermore the message contains number of tasks executed by every worker.
 *   These are then stored back into the tasks_per_process array.
 *
 * WORKER ALGORITHM:
 * - Upon receiving a message from the farmer with MPI_Recv the recursive
 *   adaptive quadrature algorithm is computed and the result is sent back to
 *   the farmer with MPI_Send.
 * - Furthermore, the number of recursive steps is counted up and sent back to
 *   the farmer as well. The values are sent in an array [r c] where r is the
 *   local result of the worker and c is the number of steps executed.
 *
 * NOTES:
 * - Again, MPI_Send and MPI_Recv were chosen over their immediate alternatives
 *   to simplify implementation.
 * - Alternatively, the farmer could have send a MPI_Reduce message. However,
 *   this way the farmer would participate in the computation. Moreover, a
 *   custom operation would have to be implemented using MPI_Op_create or we
 *   could use the MPI_SUM operation and sent two messages from the workers: one
 *   for number of tasks executed and the other one for the result. In this
 *   case, each type would need a different tag so they are not mixed together.
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
  double result[2];
  double points[2];
  double total = 0.0;
  double chunk = (B - A) / (numprocs - 1);
  int i;
  MPI_Status status;

  // Send equal sized chunks
  for (i = 1; i < numprocs; i++) {
    points[0] = A + ((i - 1) * chunk);
    points[1] = A + (i * chunk);
    MPI_Send(points, 2, MPI_DOUBLE, i, 1, MPI_COMM_WORLD);
  }

  // Receive result from every worker and add it up
  for (i = 1; i < numprocs; i++) {
    MPI_Recv(&result, 2, MPI_DOUBLE, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
    total += result[0];
    tasks_per_process[i] = (int) result[1];
  }

  return total;
}

double quad(double left, double right, double *count) {
  double fleft, fright, mid, fmid, larea, rarea, lrarea;
  *count += 1;

  fleft = F(left);
  fright = F(right);
  mid = (left + right) / 2;
  fmid = F(mid);
  larea = (fleft + fmid) * (mid - left) / 2;
  rarea = (fmid + fright) * (right - mid) / 2;
  lrarea = (fleft + fright) * (right - left) / 2;
  if (fabs((larea + rarea) - lrarea) > EPSILON) {
    larea = quad(left, mid, count);
    rarea = quad(mid, right, count);
  }
  return larea + rarea;
}

void worker(int mypid) {
  double points[2];
  double result[2];
  MPI_Status status;

  MPI_Recv(points, 2, MPI_DOUBLE, 0, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
  result[0] = quad(points[0], points[1], &result[1]);
  MPI_Send(&result, 2, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
}
