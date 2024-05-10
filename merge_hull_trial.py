import numpy as np
import matplotlib.pyplot as plt
from collections import deque

def generate_points(distribution, n):
    if distribution == 'gaussian':
        return np.random.normal(0, 1, (n, 2))
    elif distribution == 'uniform':
        return np.random.uniform(-10, 10, (n, 2))

def cross_product(o, a, b):
    # Returns a positive value if the sequence (o, a, b) is counterclockwise, negative if clockwise
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def merge(left_hull, right_hull):
    # Find the rightmost point of the left hull
    leftmost = max(left_hull, key=lambda p: p[0])
    # Find the leftmost point of the right hull
    rightmost = min(right_hull, key=lambda p: p[0])
    
    # Upper tangent
    left_idx = left_hull.index(leftmost)
    right_idx = right_hull.index(rightmost)

    def next_idx(lst, idx):
        return (idx + 1) % len(lst)

    def prev_idx(lst, idx):
        return (idx - 1) % len(lst)

    def is_counter_clockwise(p1, p2, p3):
        return cross_product(p1, p2, p3) > 0

    while True:
        upper_changed = False
        # Move clockwise on the right hull
        while not is_counter_clockwise(left_hull[left_idx], right_hull[right_idx], right_hull[next_idx(right_hull, right_idx)]):
            right_idx = next_idx(right_hull, right_idx)
            upper_changed = True
        # Move counterclockwise on the left hull
        while not is_counter_clockwise(right_hull[right_idx], left_hull[left_idx], left_hull[prev_idx(left_hull, left_idx)]):
            left_idx = prev_idx(left_hull, left_idx)
            upper_changed = True
        if not upper_changed:
            break

    upper_left = left_idx
    upper_right = right_idx

    # Lower tangent
    left_idx = left_hull.index(leftmost)
    right_idx = right_hull.index(rightmost)

    while True:
        lower_changed = False
        # Move counterclockwise on the right hull
        while is_counter_clockwise(left_hull[left_idx], right_hull[right_idx], right_hull[prev_idx(right_hull, right_idx)]):
            right_idx = prev_idx(right_hull, right_idx)
            lower_changed = True
        # Move clockwise on the left hull
        while is_counter_clockwise(right_hull[right_idx], left_hull[left_idx], left_hull[next_idx(left_hull, left_idx)]):
            left_idx = next_idx(left_hull, left_idx)
            lower_changed = True
        if not lower_changed:
            break

    lower_left = left_idx
    lower_right = right_idx

    # Merge the two halves
    hull = deque()
    idx = upper_left
    while idx != lower_left:
        hull.append(left_hull[idx])
        idx = next_idx(left_hull, idx)
    hull.append(left_hull[lower_left])
    idx = lower_right
    while idx != upper_right:
        hull.append(right_hull[idx])
        idx = next_idx(right_hull, idx)
    hull.append(right_hull[upper_right])

    return list(hull)

def merge_hull(points):
    if len(points) <= 1:
        return points

    points = sorted(points, key=lambda point: (point[0], point[1]))
    mid = len(points) // 2
    left_hull = merge_hull(points[:mid])
    right_hull = merge_hull(points[mid:])

    return merge(left_hull, right_hull)

def visualize(points, hull):
    plt.figure(figsize=(10, 6))
    plt.scatter(points[:, 0], points[:, 1], color='blue')
    hull_closed = np.append(hull, [hull[0]], axis=0)
    plt.plot(hull_closed[:, 0], hull_closed[:, 1], 'r-', lw=2)
    plt.plot(hull[:, 0], hull[:, 1], 'ro')
    plt.show()

# Generate points and compute the Convex Hull using Merge Hull Algorithm
points = generate_points('uniform', 100)
hull = merge_hull(points)
visualize(points, hull)
