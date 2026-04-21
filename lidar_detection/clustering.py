import numpy as np

def cluster_points(points, threshold=0.4):
    clusters = []
    visited = set()

    for i in range(len(points)):
        if i in visited:
            continue

        cluster = []
        queue = [i]
        visited.add(i)

        while queue:
            idx = queue.pop(0)
            cluster.append(points[idx])

            for j in range(len(points)):
                if j not in visited:
                    dist = np.linalg.norm(points[idx] - points[j])
                    if dist < threshold:
                        visited.add(j)
                        queue.append(j)

        clusters.append(np.array(cluster))

    return clusters
