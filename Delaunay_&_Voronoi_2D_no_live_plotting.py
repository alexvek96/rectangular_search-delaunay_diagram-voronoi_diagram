# Voronoi and Delaunay schematics in 2D, no live plotting

import random                                           # for generating random coordinates
import numpy as np                                      # matrix operations
import matplotlib.pyplot as plt                         # for plotting
import time                                             # for computation timing
from scipy.spatial import Voronoi, voronoi_plot_2d      # for Voronoi calculation and plotting
from scipy.spatial import Delaunay                      # for Delaunay calculation

print("\n------------------------------------------------------------------------------------")
print("              Voronoi and Delaunay schematics in 2D, no live plotting                  ")
print("------------------------------------------------------------------------------------\n")


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


# number of random points to generate
n = random.randint(5, 100)
random_points = np.array(generate_points(n))
min_x = random_points[0][0]
max_x = random_points[0][0]
min_y = random_points[0][1]
max_y = random_points[0][1]

for i in range(len(random_points)):     # we will need coordinate boundaries later in the plots
    if random_points[i][0] > max_x:
        max_x = random_points[i][0]
    if random_points[i][0] < min_x:
        min_x = random_points[i][0]
    if random_points[i][1] > max_y:
        max_y = random_points[i][1]
    if random_points[i][1] < min_y:
        min_y = random_points[i][1]

print(f"\n---------------------------------------Random points ({n})---------------------------------------\n")

# printing format for better visualization
for i in range(0, n, 10):
    row_points = random_points[i:i + 10]
    for point in row_points:
        print(f"({point[0]}, {point[1]})", end=' ')
    print()

# Voronoi schematic
print(f"\n---------------------------------------Voronoi schematic---------------------------------------")
print("\nCalculating Voronoi schematic...")
start_time = time.time()

# Compute Voronoi diagram
voronoi_scheme = Voronoi(random_points)
print("Voronoi schematic calculated.")
finish_time = time.time()

# elapsed time
print("\nElapsed calculation time: ", "{:.8f}".format(finish_time - start_time), "seconds")

# plot Voronoi schematic
voronoi_plot_2d(voronoi_scheme, show_vertices=False)
# plot the original points
plt.plot(random_points[:, 0], random_points[:, 1], 'o', color='red', markeredgecolor='black', markersize=5, markeredgewidth=1.5)
# plot intersection points with red color
plt.plot(voronoi_scheme.vertices[:, 0], voronoi_scheme.vertices[:, 1], 'ro', markersize=4)

plt.xlim(min_x - 5, max_x + 20)  # plot boundaries + an extra space for better visualization
plt.ylim(min_y - 5, max_y + 20)


# Delaunay schematic
print(f"\n---------------------------------------Delaunay schematic---------------------------------------")
print("\nCalculating Delaunay schematic...")
start_time_2 = time.time()

# Delaunay computation
Del = Delaunay(random_points)
print("Delaunay schematic calculated.")
finish_time_2 = time.time()

# elapsed time
print("\nElapsed calculation time: ", "{:.8f}".format(finish_time_2 - start_time_2), "seconds")

plt.triplot(random_points[:, 0], random_points[:, 1], Del.simplices.copy(), color='red', linewidth=1)

# plot title and labels
plt.title("Voronoi (black) and Delaunay (red) line schematics")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()




