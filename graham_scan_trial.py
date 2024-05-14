import numpy as np
import matplotlib.pyplot as plt
import gc  # Garbage collector interface

def generate_points(distribution, n):
    if distribution == 'gaussian':
        return np.random.normal(0, 1, (n, 2))
    elif distribution == 'uniform':
        return np.random.uniform(-10, 10, (n, 2))

def graham_scan(points, speed=0.1):
    # Sort the points lexicographically (tuples compare lexicographically).
    points = sorted(points, key=lambda point: (point[0], point[1]))

    # Boring case: no points or a single point, possibly repeated multiple times.
    if len(points) <= 1:
        return np.array(points)

    # 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
    # Returns a positive value, if OAB makes a counter-clockwise turn,
    # negative for clockwise turn, and zero if the points are collinear.
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Initialize the plot
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter([p[0] for p in points], [p[1] for p in points], color='blue')  # all points

    def plot_hull(hull_points):
        if len(hull_points) > 1:
            hull_closed = np.append(hull_points, [hull_points[0]], axis=0)
            ax.plot(hull_closed[:, 0], hull_closed[:, 1], color='r', linestyle='-', lw=2)  # hull lines
            ax.plot(hull_points[:, 0], hull_points[:, 1], 'ro')  # hull points
        plt.draw()
        plt.pause(speed)

    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
            ax.clear()
            ax.scatter([p[0] for p in points], [p[1] for p in points], color='blue')
            plot_hull(np.array(lower))
        lower.append(p)
        ax.clear()
        ax.scatter([p[0] for p in points], [p[1] for p in points], color='blue')
        plot_hull(np.array(lower))

    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
            ax.clear()
            ax.scatter([p[0] for p in points], [p[1] for p in points], color='blue')
            plot_hull(np.array(lower))
            plot_hull(np.array(upper))
        upper.append(p)
        ax.clear()
        ax.scatter([p[0] for p in points], [p[1] for p in points], color='blue')
        plot_hull(np.array(lower))
        plot_hull(np.array(upper))

    # Concatenate lower and upper hull to make the full hull. The last point of each half is omitted because it's repeated at the beginning of the other half.
    full_hull = lower[:-1] + upper[:-1]
    
    # Final plot to show the complete hull
    ax.clear()
    ax.scatter([p[0] for p in points], [p[1] for p in points], color='blue')
    plot_hull(np.array(full_hull))
    
    # Turn off interactive plotting and show the final result
    plt.ioff()
    plt.show()
    
    # It's advisable to clear out garbage after the computation.
    gc.collect()
    
    return np.array(full_hull)

def visualize(points, hull):
    plt.figure(figsize=(10, 6))
    plt.scatter(points[:, 0], points[:, 1], color='blue')  # all points
    # Ensure the hull is closed by connecting the last point back to the first
    hull_closed = np.append(hull, [hull[0]], axis=0)
    plt.plot(hull_closed[:, 0], hull_closed[:, 1], 'r-', lw=2)  # hull lines
    plt.plot(hull[:, 0], hull[:, 1], 'ro')  # hull points
    plt.show()


points = generate_points('uniform', 100)
speed = 0.05  # Adjust this value to make the visualization faster or slower
hull = graham_scan(points, speed)
visualize(points, hull)