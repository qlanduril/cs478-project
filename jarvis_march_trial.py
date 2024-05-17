import numpy as np
import matplotlib.pyplot as plt

def generate_points(distribution, n):
    if distribution == 'gaussian':
        return np.random.normal(0, 1, (n, 2))
    elif distribution == 'uniform':
        return np.random.uniform(-10, 10, (n, 2))

def jarvis_march(points):
    if len(points) < 3:
        return points  # Convex Hull cannot exist if fewer than 3 points

    # Find the leftmost point to start the hull
    start = min(points, key=lambda p: p[0])
    hull = [start]
    current = start

    while True:
        next_point = points[0]
        for candidate in points:
            if np.array_equal(candidate, current):
                continue
            # Cross product calculation
            cross_product = (next_point[0] - current[0]) * (candidate[1] - current[1]) - (next_point[1] - current[1]) * (candidate[0] - current[0])
            if cross_product < 0 or (cross_product == 0 and np.linalg.norm(candidate - current) > np.linalg.norm(next_point - current)):
                next_point = candidate
        
        if np.array_equal(next_point, start):
            break

        hull.append(next_point)
        current = next_point

    return np.array(hull)

def visualize(points, hull):
    plt.figure(figsize=(10, 6))
    plt.scatter(points[:, 0], points[:, 1], color='blue')
    hull_closed = np.append(hull, [hull[0]], axis=0)
    plt.plot(hull_closed[:, 0], hull_closed[:, 1], 'r-', lw=2)
    plt.plot(hull[:, 0], hull[:, 1], 'ro')
    plt.show()

# Generate points and compute the Convex Hull using the Jarvis March algorithm
points = generate_points('uniform', 100)
hull = jarvis_march(points)
print(hull)
"""visualize(points, hull)"""
