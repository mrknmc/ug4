import numpy as np


weights = {
    (0, 1): 2,
    (0, 2): 2,
    (0, 3): 3,
    (1, 4): 3,
    (2, 3): -1,
    (2, 4): 2,
    (2, 5): 3,
    (4, 5): 0,
    (4, 6): 2,
    (5, 6): 3,
    (5, 7): 3,
    (6, 7): 1,
    (6, 8): 3,
    (7, 8): -2
}

dist = np.empty((9, 9), float)
dist.fill(float('inf'))

np.fill_diagonal(dist, 0)

for (u, v), w in weights.items():
    dist[u][v] = 1

for k in range(9):
    for i in range(9):
        for j in range(9):
            if dist[i][j] > dist[i][k] + dist[k][j]:
                dist[i][j] = dist[i][k] + dist[k][j]

print(dist)
