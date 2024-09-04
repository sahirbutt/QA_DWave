import numpy as np
import itertools

# Example TSP instance as a distance matrix
distance_matrix = np.array([
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
])

def total_distance(tour, dist_matrix):
    return sum(dist_matrix[tour[i], tour[i + 1]] for i in range(len(tour) - 1)) + dist_matrix[tour[-1], tour[0]]

def find_all_optimal_solutions(dist_matrix):
    n = len(dist_matrix)
    all_tours = itertools.permutations(range(n))
    min_distance = float('inf')
    optimal_tours = []

    for tour in all_tours:
        dist = total_distance(tour, dist_matrix)
        if dist < min_distance:
            min_distance = dist
            optimal_tours = [tour]
        elif dist == min_distance:
            optimal_tours.append(tour)

    # To handle rotational symmetry, normalize tours
    def normalize_tour(tour):
        # Convert tour to a normalized form starting from the smallest element
        min_index = tour.index(min(tour))
        return tour[min_index:] + tour[:min_index]
    
    unique_optimal_tours = set(normalize_tour(tour) for tour in optimal_tours)
    return min_distance, unique_optimal_tours

# Find and print all optimal solutions
optimal_distance, unique_optimal_tours = find_all_optimal_solutions(distance_matrix)

print(f"Optimal Distance: {optimal_distance}")
print(f"Number of Unique Optimal Solutions: {len(unique_optimal_tours)}")
print("Unique Optimal Solutions:")
for tour in unique_optimal_tours:
    print(tour)
