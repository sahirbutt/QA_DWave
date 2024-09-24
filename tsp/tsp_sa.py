import numpy as np
import random
import math

# Example TSP instance as a distance matrix
#distance_matrix = np.array([
#    [0, 10, 15, 20],
#    [10, 0, 35, 25],
#    [15, 35, 0, 30],
#    [20, 25, 30, 0]
#])

# Assumed coordinates for the four cities
# You can change these coordinates to any other set that you prefer
city_coordinates = np.array([
    [0, 0],  # City 0
    [10, 1],  # City 1
    [5, 10],  # City 2
    [0, 20]   # City 3
])

# Calculate the distance matrix
distance_matrix = np.sqrt(((city_coordinates[:, np.newaxis] - city_coordinates) ** 2).sum(axis=2))

# Print the distance matrix
print("Distance matrix:")
print(distance_matrix)


def total_distance(tour, dist_matrix):
    return sum(dist_matrix[tour[i], tour[i + 1]] for i in range(len(tour) - 1)) + dist_matrix[tour[-1], tour[0]]

def simulated_annealing(dist_matrix, initial_temp, cooling_rate, n_iterations):
    n = len(dist_matrix)
    current_solution = list(range(n))
    current_distance = total_distance(current_solution, dist_matrix)
    
    best_solution = current_solution[:]
    best_distance = current_distance
    
    temperature = initial_temp
    
    for iteration in range(n_iterations):
        # Generate a neighboring solution
        new_solution = current_solution[:]
        i, j = random.sample(range(n), 2)
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
        
        new_distance = total_distance(new_solution, dist_matrix)
        delta = new_distance - current_distance
        
        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperature):
            current_solution = new_solution
            current_distance = new_distance
            
            if current_distance < best_distance:
                best_solution = current_solution[:]
                best_distance = current_distance
        
        # Cool down
        temperature *= cooling_rate
    
    return best_solution, best_distance

# Parameters
initial_temp = 1000
cooling_rate = 0.995
n_iterations = 1000

# Solve TSP
best_solution, best_distance = simulated_annealing(distance_matrix, initial_temp, cooling_rate, n_iterations)
print(f"Best Solution: {best_solution}")
print(f"Best Distance: {best_distance}")
