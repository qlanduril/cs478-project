import pygame
import sys
import numpy as np
import graham_scan
# numpy-1.26.4 pygame-2.5.2


def generate_uniform_points(min, max, count):
    return np.random.uniform(minv,maxv,size=(count,2))

def generate_gaussian_points(min, max, count):
    return np.random.normal(minv,maxv,size=(count,2))
    
# Function to find orientation of triplet (p, q, r)
# The function returns the following values:
# 0 : Collinear points
# 1 : Clockwise points
# 2 : Counterclockwise points
def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # Collinear
    return 1 if val > 0 else 2  # Clockwise or Counterclockwise

# Function to perform Graham's scan algorithm to find convex hull
def convex_hull_graham_scan(points):
    # Number of points
    n = len(points)
    
    # If there are less than 3 points, convex hull is not possible
    if n < 3:
        return []
    
    # Find the point with the lowest y-coordinate (and the leftmost one if there are ties)
    min_idx = 0
    for i in range(1, n):
        if points[i][1] < points[min_idx][1] or (points[i][1] == points[min_idx][1] and points[i][0] < points[min_idx][0]):
            min_idx = i
    
    # Place the point with the lowest y-coordinate at the beginning of the list
    points[0], points[min_idx] = points[min_idx], points[0]
    
    # Sort the remaining points based on polar angle with respect to the first point
    def polar_angle(p):
        return (p[1] - points[0][1], p[0] - points[0][0])
    points[1:] = sorted(points[1:], key=polar_angle)
    
    # Initialize an empty stack
    stack = []
    
    # Push the first three points onto the stack
    stack.append(points[0])
    stack.append(points[1])
    stack.append(points[2])
    
    # Iterate over the remaining points
    for i in range(3, n):
        # Pop points from the stack while the angle formed by points at the top of the stack,
        # the point just below it, and the current point makes a non-left turn
        while len(stack) > 1 and orientation(stack[-2], stack[-1], points[i]) != 2:
            stack.pop()
        
        # Push the current point onto the stack
        stack.append(points[i])
    
    # The stack now contains the convex hull in counterclockwise order
    return stack

# Function to scale the coordinates to fit within the window size
def scale_points(points, width, height):
    min_x = np.min(points,0)[0]
    max_x = np.max(points,0)[0]
    min_y = np.min(points,0)[1]
    max_y = np.max(points,0)[0]
    
    scaled_points = []
    for x, y in points:
        scaled_x = int((x - min_x) / (max_x - min_x) * (width - 20) + 10)
        scaled_y = int((y - min_y) / (max_y - min_y) * (height - 20) + 10)
        scaled_points.append((scaled_x, scaled_y))
    
    return scaled_points

# Function to plot the convex hull and original points using Pygame
def plot_convex_hull(points, convex_hull):
    pygame.init()
    
    
    # Set window dimensions
    width, height = 1600, 900
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Convex Hull Visualization")

    # draw surface
    transparent_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    transparent_surface.fill((255, 255, 255, 0))  # 128 is the alpha value, 0 is fully transparent and 255 is fully opaque

    
    # Scale points to fit within the window size
    scaled_points = scale_points(points, width, height)
    scaled_convex_hull = scale_points(convex_hull, width, height)
    
    # Draw original points
    for point in scaled_points:
        pygame.draw.circle(screen, (0, 0, 255), point, 5)
    
    # Draw convex hull
    for i in range(len(scaled_convex_hull)):
        pygame.draw.line(transparent_surface, (255, 0, 0), scaled_convex_hull[i], scaled_convex_hull[(i + 1) % len(scaled_convex_hull)], 2)

    # Draw convex hull points
    #for point in scaled_convex_hull:
        #pygame.draw.circle(screen, (255, 0, 0), point, 5)

    current_frame = pygame.Surface((width, height))
    current_frame.blit(screen, (0, 0))
    screen.blit(transparent_surface,(0,0))
    screen.blit(current_frame,(0,0))
    
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    
    pygame.quit()

# Example usage
if __name__ == "__main__":
    # Example set of points
    r = 5000
    minv = 100
    maxv = 1000000

    points = generate_gaussian_points(minv,maxv,r)
    #points = generate_gaussian_points(minv, maxv, r)


    
    # Find the convex hull using Graham's scan algorithm
    convex_hull = convex_hull_graham_scan(points)
    
    # Plot convex hull and original points using Pygame
    plot_convex_hull(points, convex_hull)

    graham_scan.convexHull(points, r)

