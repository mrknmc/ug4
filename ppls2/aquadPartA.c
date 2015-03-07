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
  double result[3];
  double *points_p;
  double total = 0.0;
  MPI_Status status;
  int workers = numprocs - 1;

  // 1. Place initial tasks into bag
  points[0] = A;
  points[1] = B;
  push(points, stack);

  while (!is_empty(stack)) {
    // send all you can
    while (workers > 0 && !is_empty(stack)) {
      points_p = pop(stack);
      MPI_Send(points_p, 2, MPI_DOUBLE, workers, 1, MPI_COMM_WORLD);
      tasks_per_process[workers] += 1;
      /*printf("Sending task to %d\n", workers);*/
      workers--;
    }
    while (workers < numprocs - 1) {
      MPI_Recv(result, 3, MPI_DOUBLE, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
      if (0 == status.MPI_TAG) {
        // result was within Epsilon, add to total
        total += result[0];
      } else {
        // add new tasks
        push(result, stack);
        push(result + 1, stack);
      }
      workers++;
    }
  }

  // Terminate all the workers
  for (workers = numprocs - 1; workers > 0; workers--) {
    /*printf("%d\n", workers);*/
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
    /*printf("Received %f %f\n", points[0], points[1]);*/
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
  /*printf("worker %d is done\n", mypid);*/
}
