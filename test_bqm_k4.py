import dimod
import dwave.inspector
import dwave.system

linear = {1: 1,
          2: 2,
          3: 3,
          4: 0}

quadratic = {(1, 1): 10, (1, 2): 13, (1, 3): 14, (1, 4): 11,
             (2, 1): 23, (2, 2):  0, (2, 3): 34, (2, 4): 11,
             (3, 1): 12, (3, 2): 24, (3, 3):  0, (3, 4): 11,
             (4, 1): -55, (4, 2): 56, (4, 3): 34, (4, 4):  0}

offset = -50.0

vartype = dimod.BINARY

bqm_k4 = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype)

solver = dimod.ExactSolver()

results = solver.sample(bqm_k4)

print(results)

# with dWave
sampler = dwave.system.EmbeddingComposite(dwave.system.DWaveSampler())
sampleset = sampler.sample(bqm_k4, num_reads=10)
dwave.inspector.show(sampleset)
