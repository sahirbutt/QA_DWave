from dwave.system import DWaveSampler, EmbeddingComposite
import numpy as np
import networkx as nx
from dwave.system import LeapHybridSampler

# Example TSP instance
distance_matrix = np.array([
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
])

def create_qubo_from_distance_matrix(dist_matrix):
    n = len(dist_matrix)
    Q = {}
    for i in range(n):
        for j in range(i + 1, n):
            Q[(i, j)] = dist_matrix[i, j] + dist_matrix[j, i]
    return Q

def solve_tsp_with_dwave(dist_matrix):
    Q = create_qubo_from_distance_matrix(dist_matrix)
    
    sampler = EmbeddingComposite(DWaveSampler())
    response = sampler.sample_qubo(Q, num_reads=1000)
    
    # Extract best solution
    sample = response.first.sample
    tour = [i for i in range(len(dist_matrix)) if sample.get(i, 0)]
    
    # Calculate total distance
    distance = sum(dist_matrix[tour[i], tour[i + 1]] for i in range(len(tour) - 1)) + dist_matrix[tour[-1], tour[0]]
    
    return tour, distance

# Solve TSP
best_solution, best_distance = solve_tsp_with_dwave(distance_matrix)
print(f"Best Solution: {best_solution}")
print(f"Best Distance: {best_distance}")

