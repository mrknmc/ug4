import sys
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
next = np.empty((9, 9))
dist.fill(float('inf'))
next.fill(np.nan)

np.fill_diagonal(dist, 0)

for (u, v), w in weights.items():
    dist[u][v] = 1
    next[u][v] = v

# print next

for k in range(9):
    for i in range(9):
        for j in range(9):
            if dist[i][j] > dist[i][k] + dist[k][j]:
                dist[i][j] = dist[i][k] + dist[k][j]
                next[i][j] = next[i][k]

print dist
# print next

for u in range(9):
    for v in range(9):
        if np.isnan(next[u][v]):
            continue
        else:
            path = [u]
            while u != v:
                print u
                u = next[u][v]
                path.append(u)
            # print('Path from {} to {}:'.format(u, v))
            # print(path)
