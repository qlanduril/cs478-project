import numpy as np
import matplotlib.pyplot as plt

# Stores the result (points of convex hull)
hull = set()

# Returns the side of point p with respect to line
# joining points p1 and p2.
def findSide(p1, p2, p):
    val = (p[1] - p1[1]) * (p2[0] - p1[0]) - (p2[1] - p1[1]) * (p[0] - p1[0])
    if val > 0:
        return 1
    if val < 0:
        return -1
    return 0

# Returns a value proportional to the distance
# between the point p and the line joining the
# points p1 and p2
def lineDist(p1, p2, p):
    return abs((p[1] - p1[1]) * (p2[0] - p1[0]) - (p2[1] - p1[1]) * (p[0] - p1[0]))

# End points of line L are p1 and p2. side can have value
# 1 or -1 specifying each of the parts made by the line L
def quickHull(a, n, p1, p2, side):
    ind = -1
    max_dist = 0

    # Finding the point with maximum distance
    # from L and also on the specified side of L.
    for i in range(n):
        temp = lineDist(p1, p2, a[i])
        if (findSide(p1, p2, a[i]) == side) and (temp > max_dist):
            ind = i
            max_dist = temp

    # If no point is found, add the end points
    # of L to the convex hull.
    if ind == -1:
        hull.add(tuple(p1))
        hull.add(tuple(p2))
        return

    # Recur for the two parts divided by a[ind]
    quickHull(a, n, a[ind], p1, -findSide(a[ind], p1, p2))
    quickHull(a, n, a[ind], p2, -findSide(a[ind], p2, p1))

def printHull(a, n):
    # Sort the points based on x-coordinate
    a.sort(key=lambda x: x[0])

    # Finding the point with minimum and
    # maximum x-coordinate
    min_x = 0
    max_x = 0
    for i in range(1, n):
        if a[i][0] < a[min_x][0]:
            min_x = i
        if a[i][0] > a[max_x][0]:
            max_x = i

    # Recursively find convex hull points on
    # one side of line joining a[min_x] and
    # a[max_x]
    quickHull(a, n, a[min_x], a[max_x], 1)

    # Recursively find convex hull points on
    # other side of line joining a[min_x] and
    # a[max_x]
    quickHull(a, n, a[min_x], a[max_x], -1)

    # Sort the points in the hull to be in counterclockwise order
    hull_points = list(hull)
    centroid = np.mean(hull_points, axis=0)
    hull_points.sort(key=lambda p: np.arctan2(p[1] - centroid[1], p[0] - centroid[0]))

    print("The points in Convex Hull are:")
    for element in hull_points:
        print("(", element[0], ",", element[1], ") ", end=" ")

    return hull_points

def visualize(points, hull):
    points = np.array(points)  # Convert to NumPy array
    hull = np.array(hull)  # Convert hull to NumPy array
    plt.figure(figsize=(10, 6))
    plt.scatter(points[:, 0], points[:, 1], color='blue')  # all points
    # Ensure the hull is closed by connecting the last point back to the first
    hull_closed = np.append(hull, [hull[0]], axis=0)
    plt.plot(hull_closed[:, 0], hull_closed[:, 1], 'r-', lw=2)  # hull lines
    plt.plot(hull[:, 0], hull[:, 1], 'ro')  # hull points
    plt.show()

# Driver code
a = [[0, 3], [1, 1], [2, 2], [4, 4],
     [0, 0], [1, 2], [3, 1], [3, 3]]
n = len(a)
hull_points = printHull(a, n)
visualize(a, hull_points)