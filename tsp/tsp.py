import numpy as np
import dimod
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix

# Define the number of cities
n = 4


# Assumed coordinates for the four cities
# You can change these coordinates to any other set that you prefer
city_coordinates = np.array([
    [0, 0],  # City 0
    [10, 1],  # City 1
    [5, 10],  # City 2
    [0, 20]   # City 3
])

# Calculate the distance matrix
distances = np.sqrt(((city_coordinates[:, np.newaxis] - city_coordinates) ** 2).sum(axis=2))

# Print the distance matrix
print("Distance matrix:")
print(distances)


# Define the distance matrix for four cities (already provided)
#distances = np.array([[0, 10, 15, 20],
#                      [10, 0, 35, 25],
#                      [15, 35, 0, 30],
#                      [20, 25, 30, 0]])

# Coordinates for cities will be inferred from the distance matrix
# We'll use a simple method for finding coordinates
#city_coordinates = np.array([[0, 0],  # City 0
#                             [10, 0],  # City 1 at a distance of 10 units from City 0
#                             [10, 15],  # City 2 based on relative distance (15 units away)
#                             [0, 20]])  # City 3 based on relative distance (20 units away)

# Penalty coefficient
A = 100  # Strong penalty to enforce constraints

# Initialize the QUBO matrix as a dictionary
Q = {}

# Constraint 1: Each city is visited exactly once
for i in range(n):
    for j in range(n):
        # Linear term for city j being visited at position i
        Q[(i*n + j, i*n + j)] = - 2* A

        # Quadratic penalty terms: city j is not visited in multiple positions
        for k in range(i + 1, n):
            Q[(i*n + j, k*n + j)] = 2 * A

# Constraint 2: Each position is occupied by exactly one city
for i in range(n):
    for j in range(n):
        # Quadratic penalty terms: multiple cities do not occupy the same position
        for k in range(j + 1, n):
            Q[(i*n + j, i*n + k)] = 2 * A

# Objective function: minimize the total travel distance
for i in range(n):
    for j in range(n):
        for k in range(n):
            if j != k:
                # Add distance between city j and city k when they are in consecutive positions
                Q[(i*n + j, (i+1) % n * n + k)] = distances[j][k]
# Determine the size of the QUBO matrix
# Q is a dictionary with keys as tuples representing variable interactions (i, j)
# size = max(max(i, j) for i, j in Q.keys()) + 1

# # Initialize an empty NumPy matrix of size (size x size)
# qubo_matrix = np.zeros((size, size))

# # Populate the matrix using the QUBO dictionary
# for (i, j), value in Q.items():
#     qubo_matrix[i, j] = value
#     # QUBO matrices are symmetric, so fill both [i, j] and [j, i] if different
#     if i != j:
#         qubo_matrix[j, i] = value

# # Print the resulting matrix
# print("QUBO Matrix:")
# print(qubo_matrix)


# Solve the QUBO problem using ExactSolver
sampler = dimod.ExactSolver()
bqm = dimod.BinaryQuadraticModel.from_qubo(Q)
solution = sampler.sample(bqm)

# Get the best solution
best_solution = solution.first.sample
best_energy = solution.first.energy

# Extract the tour from the solution bit string
tour = [-1] * n
for i in range(n):
    for j in range(n):
        if best_solution[i*n + j] == 1:
            tour[i] = j

# Check if the tour is valid
if -1 in tour:
    print("Invalid solution: some positions in the tour are not filled properly.")
else:
    # Calculate the total distance traveled
    total_distance = 0
    for i in range(n):
        total_distance += distances[tour[i]][tour[(i+1) % n]]

    # Print the results
    print("Best solution (bitstring):", best_solution)
    print("Best solution (city order):", tour)
    print("Total distance traveled:", total_distance)

    # Plot the route on an actual scale using the city coordinates
    plt.figure(figsize=(6, 6))
    plt.title("Salesperson's Route on Actual Scale")
    
    # Plot the cities
    for i, (x, y) in enumerate(city_coordinates):
        plt.scatter(x, y, color='red', zorder=5)
        plt.text(x, y, f'City {i}', fontsize=12, ha='right')

    # Plot the tour
    for i in range(n):
        city_from = tour[i]
        city_to = tour[(i+1) % n]
        plt.plot([city_coordinates[city_from][0], city_coordinates[city_to][0]],
                 [city_coordinates[city_from][1], city_coordinates[city_to][1]], 'b-', zorder=1)

    plt.xlim(-5, 25)  # Adjust the limits based on coordinates
    plt.ylim(-5, 25)
    plt.grid(True)
    plt.show()
