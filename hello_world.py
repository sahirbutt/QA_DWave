#imports
import dimod

#solver
solver = dimod.ExactSolver()

#Define QUBO
Q = {('a','b'):-2,('a','a'):1,('b','b'):1}

#Get BQM
bqm = dimod.BinaryQuadraticModel.from_qubo(Q)

#Solve
results = solver.sample(bqm)

#print result
print(results)

