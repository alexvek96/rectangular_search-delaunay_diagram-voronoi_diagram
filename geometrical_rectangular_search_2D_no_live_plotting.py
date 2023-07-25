# KD-tree implementation for geometric rectangular search in 2D, no live plotting

import random                       # for generating random coordinates
import numpy as np                  # matrix operations
import matplotlib.pyplot as plt     # for plotting
import time                         # for computation timing

print("\n------------------------------------------------------------------------------------")
print("               Geometric rectangular search in 2D, no live plotting                   ")
print("------------------------------------------------------------------------------------\n")


# KD-tree node class to represent a node in the KD-tree
class kdnode:
    def __init__(self, point, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right


# function building a KD-tree from a list of points
def build_kdtree(points, depth=0):

    if len(points) == 0:    # terminate if there are no point to build the KD-tree
        return None

    k = len(points[0])  # dimension of the points
    axis = depth % k    # axis to split the points

    indices = np.argsort(points[:, axis])  # get the indices that would sort the points based on the current axis
    points = points[indices]               # sort the points array using the indices
    median = len(points) // 2              # find the median index

    # left and right sub-tree recursive construction
    return kdnode(
        point=points[median],
        left=build_kdtree(points[:median], depth + 1),
        right=build_kdtree(points[median + 1:], depth + 1)
    )


# function performing a rectangular search in a KD-tree
def search_rectangular(node, rect_min, rect_max, depth=0, result=None):
    if node is None:
        return

    k = len(node.point)  # dimension of the points in the node
    axis = depth % k     # axis to compare with the current level

    if result is None:
        result = []

    # check if the current node's point falls within the query rectangle
    if rect_min[axis] <= node.point[axis] <= rect_max[axis]:
        if all(rect_min[i] <= node.point[i] <= rect_max[i] for i in range(k)):
            result.append(node.point)

    # recursive search on the left subtree
    if rect_min[axis] < node.point[axis]:
        search_rectangular(node.left, rect_min, rect_max, depth + 1, result)

    # recursive search on the right subtree
    if rect_max[axis] > node.point[axis]:
        search_rectangular(node.right, rect_min, rect_max, depth + 1, result)

    return result


# function generating points with random coordinates, and no 2 points have same 'x' or 'y'
def generate_points(n):

    points = set()
    while len(points) < n:
        x = random.randint(1, n * 10)   # 1<= x <=600
        y = random.randint(1, n * 10)   # 1<= y <=600
        point = (x, y)
        # checking that no 2 points have same 'x' or 'y'
        if all(point[0] != p[0] and point[1] != p[1] for p in points):
            # add the ne point in the set
            points.add(point)

    return list(points)

# function that generates a rectangular of random corners
def generate_rectangle():

    # generate random x and y coordinates for the rectangle's corners
    # to be inside the bigger coordinates frame of the 60 points
    x1 = random.randint(1, 595)
    y1 = random.randint(1, 595)
    x2 = random.randint(1, 595)
    y2 = random.randint(1, 595)

    # find the minimum and maximum x and y coordinates
    min_x = min(x1, x2)
    max_x = max(x1, x2)
    min_y = min(y1, y2)
    max_y = max(y1, y2)

    # now create the corners of the rectangular
    crn1 = (min_x, min_y)
    crn2 = (min_x, max_y)
    crn3 = (max_x, min_y)
    crn4 = (max_x, max_y)

    return [crn1, crn2, crn3, crn4]



n = 60  # number of random points to generate
random_points = np.array(generate_points(n))
print("\n---------------------------------------Random points (60)---------------------------------------\n")

# printing format for better visualization
for i in range(0, n, 10):
    row_points = random_points[i:i + 10]
    for point in row_points:
        print(f"({point[0]}, {point[1]})", end=' ')
    print()

print("\nInitializing the KD-tree...")
start_time = time.time()
# build the KDTree from the given points
kdtree = build_kdtree(random_points)
print("KD-tree initialized.")

print("\n-------------------------------Rectangular search frame corners-------------------------------\n")
rect_corners = generate_rectangle()
print(rect_corners)

# create arrays with max 'x' and 'y' coordinates
min_coords = np.array([rect_corners[0][0], rect_corners[0][1]])   # min 'x' and min 'y'
max_coords = np.array([rect_corners[3][0], rect_corners[3][1]])   # max 'x' and max 'y'

# rectangular search in the specified rectangular area
result_points = (search_rectangular(kdtree, min_coords, max_coords))
# convert the 'result_points' to the same printing format as before
result_points = [tuple(point) for point in result_points]

finish_time = time.time()

print("\n-----------------------------------Points in the search area----------------------------------\n")
# printing format for better visualization
for i in range(0, len(result_points), 5):
    row_points = result_points[i:i + 5]
    for point in row_points:
        print(point, end=' ')
    print()

# elapsed time
print("\nElapsed calculation time: ", "{:.8f}".format(finish_time - start_time), "seconds")

# plotting the initial points with blue color
plt.scatter(random_points[:, 0], random_points[:, 1], color='blue', s=15, label='Initial Points')

# plotting the search rectangle area with purple color
rect_corners = np.array(rect_corners)
rect_min_x, rect_min_y = rect_corners[0]
rect_max_x, rect_max_y = rect_corners[3]
rect_width = rect_max_x - rect_min_x
rect_height = rect_max_y - rect_min_y
rect = plt.Rectangle((rect_min_x, rect_min_y), rect_width, rect_height, linewidth=1.5, edgecolor='purple',
                     facecolor='none', label='Search Rectangle')
plt.gca().add_patch(rect)

# plot the 'result_points' with green color
result_points = np.array(result_points)
for i in range(len(result_points)):
    plt.scatter(result_points[i][0], result_points[i][1], color='red', s=15, label='Points in Search Area')

# plot title and labels
plt.title("Initial 60 points, search area and points of interest")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()

