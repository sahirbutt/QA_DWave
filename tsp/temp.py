import numpy as np
import random
import math

# Example TSP distance matrix
distance_matrix = np.array([
    [0, 10, 15, 20, 10],
    [10, 0, 35, 25, 10],
    [15, 35, 0, 30, 10],
    [20, 25, 30, 0, 10],
    [10, 10, 10, 10, 0]
])

# Function to compute the total distance of a given tour
def total_distance(tour, dist_matrix):
    return sum(dist_matrix[tour[i], tour[i + 1]] for i in range(len(tour) - 1)) + dist_matrix[tour[-1], tour[0]]

# Simulated Annealing algorithm
def simulated_annealing(dist_matrix, initial_temp, cooling_rate, n_iterations, nc):
    n = len(dist_matrix)  # Number of cities
    current_solution = list(range(n))  # Initial solution (e.g., [0, 1, 2, 3])
    current_distance = total_distance(current_solution, dist_matrix)  # Cost of initial solution
    
    best_solution = current_solution[:]  # Track the best solution
    best_distance = current_distance  # Track the best distance
    
    temperature = initial_temp  # Starting temperature
    iteration_count = 0  # To count the number of iterations
    stagnation_count = 0  # To count iterations without improvement
    
    for iteration in range(n_iterations):
        iteration_count += 1
        # Generate a neighboring solution by swapping two cities
        new_solution = current_solution[:]
        i, j = random.sample(range(n), 2)  # Randomly pick two indices
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]  # Swap
        
        # Compute the distance of the new solution
        new_distance = total_distance(new_solution, dist_matrix)
        delta = new_distance - current_distance  # Change in distance
        
        # Acceptance criterion
        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperature):
            current_solution = new_solution
            current_distance = new_distance
            
            # Update the best solution if the new solution is better
            if current_distance < best_distance:
                best_solution = current_solution[:]
                best_distance = current_distance
                stagnation_count = 0  # Reset stagnation count
            else:
                stagnation_count += 1  # Increment stagnation count
        else:
            stagnation_count += 1  # Increment stagnation count
        
        # Cool down the temperature
        temperature *= cooling_rate
        
        # Stop if no improvement for NC iterations
        if stagnation_count >= nc:
            print(f"Converged after {iteration_count} iterations.")
            break
    
    return best_solution, best_distance, iteration_count

# Parameters
initial_temp = 1000  # Initial temperature
cooling_rate = 0.995  # Cooling rate (temperature reduction factor)
n_iterations = 10000  # Maximum number of iterations
nc = 10  # Number of iterations without improvement before stopping

# Solve TSP
best_solution, best_distance, iteration_count = simulated_annealing(distance_matrix, initial_temp, cooling_rate, n_iterations, nc)
print(f"Best Solution: {best_solution}")
print(f"Best Distance: {best_distance}")
print(f"Number of Iterations: {iteration_count}")
