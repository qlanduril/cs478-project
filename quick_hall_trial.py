import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.animation import FuncAnimation
import time

# Initialize the figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# A function to compute the distance of a point from a line (line_1 to line_2)
def distance(line_1, line_2, point):
    return abs((line_2[1] - line_1[1]) * point[0] - (line_2[0] - line_1[0]) * point[1] + line_2[0] * line_1[1] - line_2[1] * line_1[0]) / math.sqrt((line_2[1] - line_1[1]) ** 2 + (line_2[0] - line_1[0]) ** 2)

# A function to determine if points are to the right of a line
def points_to_right(points, line_1, line_2):
    def is_right(p):
        return (line_2[0] - line_1[0]) * (p[1] - line_1[1]) - (line_2[1] - line_1[1]) * (p[0] - line_1[0]) > 0
    return [p for p in points if is_right(p)]

# List to store frames for animation
frames = []

def find_hull(points, line_1, line_2):
    if len(points) == 0:
        return [line_1]
    
    furthest = None
    furthest_distance = -math.inf
    for point in points:
        distance_from_line = distance(line_1, line_2, point)
        if distance_from_line > furthest_distance:
            furthest = point
            furthest_distance = distance_from_line
    
    # Add a frame for the current step
    frames.append((line_1, line_2, furthest, points.copy()))
    
    s1 = points_to_right(points, line_1, furthest)
    s2 = points_to_right(points, furthest, line_2)

    s1_hull = find_hull(s1, line_1, furthest)
    s2_hull = find_hull(s2, furthest, line_2)

    return s1_hull + s2_hull

def quickhull(points):
    min_x = min(points, key=lambda item: item[0])
    max_x = max(points, key=lambda item: item[0])

    points.remove(min_x)
    points.remove(max_x)

    s1 = points_to_right(points, min_x, max_x)
    s2 = points_to_right(points, max_x, min_x)

    s1_hull = find_hull(s1, min_x, max_x)
    s2_hull = find_hull(s2, max_x, min_x)

    points.append(min_x)
    points.append(max_x)

    return np.array(s1_hull + [max_x] + s2_hull)

"""
def animate(i):
    ax.clear()
    # Plot all points
    ax.scatter(points[:, 0], points[:, 1], color='blue')
    
    # Draw the lines and points for each frame
    for j in range(i + 1):
        line_1, line_2, furthest, current_points = frames[j]
        ax.plot([line_1[0], line_2[0]], [line_1[1], line_2[1]], 'g-', lw=2)
        if furthest:
            ax.plot([line_1[0], furthest[0]], [line_1[1], furthest[1]], 'r--', lw=2)
            ax.plot([line_2[0], furthest[0]], [line_2[1], furthest[1]], 'r--', lw=2)
            ax.scatter([furthest[0]], [furthest[1]], color='red')
            triangle = np.array([line_1, line_2, furthest, line_1])
            ax.plot(triangle[:, 0], triangle[:, 1], 'r-', lw=1)

def visualize(points, hull):
    global frames
    frames = []
    
    hull_points = quickhull(points.tolist())
    
    ani = FuncAnimation(fig, animate, frames=len(frames), interval=1000, repeat=False)
    plt.show()
"""

def generate_points(distribution, n):
    if distribution == 'gaussian':
        return np.random.normal(0, 1, (n, 2))
    elif distribution == 'uniform':
        return np.random.uniform(-10, 10, (n, 2))

# Generate points
points = generate_points('uniform', 100)

# Time the QuickHull algorithm
start_time = time.time()
hull = quickhull(points.tolist())
end_time = time.time()
print(hull)

print(f"QuickHull algorithm took {end_time - start_time} seconds")

# Compute the Convex Hull using the QuickHull algorithm and visualize
# hull = quickhull(points.tolist())

# Visualize the result
# visualize(points, hull)