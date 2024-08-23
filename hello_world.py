#imports
import dimod
import dwave.inspector
import dwave.system

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

# Usig dWave
sampler = dwave.system.EmbeddingComposite(dwave.system.DWaveSampler())
sampleset = sampler.sample(bqm, num_reads=10)
dwave.inspector.show(sampleset)
