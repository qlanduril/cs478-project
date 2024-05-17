import numpy as np
import matplotlib.pyplot as plt

def generate_points(distribution, n):
    if distribution == 'gaussian':
        return np.random.normal(0, 1, (n, 2))
    elif distribution == 'uniform':
        return np.random.uniform(-10, 10, (n, 2))

def jarvis_march(points, speed):
    if len(points) < 3:
        return points  # Convex Hull cannot exist if fewer than 3 points

    # Find the leftmost point to start the hull
    start = min(points, key=lambda p: p[0])
    hull = [start]
    current = start

    def plot_step(current, candidate, hull):
        plt.clf()
        plt.scatter(points[:, 0], points[:, 1], color='blue')
        if len(hull) > 0:
            hull_points = np.array(hull)
            plt.plot(hull_points[:, 0], hull_points[:, 1], 'ro')
            hull_closed = np.append(hull_points, [hull_points[0]], axis=0)
            plt.plot(hull_closed[:, 0], hull_closed[:, 1], 'r-', lw=2)
        plt.scatter([current[0]], [current[1]], color='green', zorder=5)
        plt.scatter([candidate[0]], [candidate[1]], color='yellow', zorder=5)
        plt.pause(speed)

    while True:
        next_point = points[0]
        for candidate in points:
            if np.array_equal(candidate, current):
                continue
            # Cross product calculation
            cross_product = (next_point[0] - current[0]) * (candidate[1] - current[1]) - (next_point[1] - current[1]) * (candidate[0] - current[0])
            if cross_product < 0 or (cross_product == 0 and np.linalg.norm(candidate - current) > np.linalg.norm(next_point - current)):
                next_point = candidate
                plot_step(current, candidate, hull)

        if np.array_equal(next_point, start):
            break

        hull.append(next_point)
        current = next_point
        plot_step(current, next_point, hull)

    return np.array(hull)

def visualize(points, hull):
    plt.figure(figsize=(10, 6))
    plt.scatter(points[:, 0], points[:, 1], color='blue')
    hull_closed = np.append(hull, [hull[0]], axis=0)
    plt.plot(hull_closed[:, 0], hull_closed[:, 1], 'r-', lw=2)
    plt.plot(hull[:, 0], hull[:, 1], 'ro')
    plt.show()

# Generate points and compute the Convex Hull using the Jarvis March algorithm with speed control
points = generate_points('uniform', 1000)
speed = 0.05  # Adjust this value to make the visualization faster or slower
hull = jarvis_march(points, speed)
visualize(points, hull)