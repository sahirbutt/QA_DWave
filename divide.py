import dimod
import dwave.inspector
import dwave.system

# Empty dictionary for linear and quadratic part of the hamiltonian
# Length of these will be decided by the number of qubits we want to use
linear = {}
quadratic = {}
offset = 0.0
vartype = dimod.BINARY

# Number of qubits (R)
R = 3

# trying to find binary representation Q of x according to x = y/m; xE[-1,3)
y = 1
m = 3

# Fill linear and quadratic term according to
# Lin(r) = sum_r(0 to R-1) 4m2^(-r)[m2^(-r) - (y+m)]
# Quad(r) = sum_r(0 to R-1) sum_s(0 to R-1) (with r!=s) 4m^2 2^(-r-s)

for r in range(R):
	linear[r] = 4*m*m * 2**(-r) * (m*2**(-r) - (y+m))

for r in range(R):
	for s in range(R):
		if r==s:
			quadratic[r,s] = 4*m*m * 2**(-r-s)

print(linear)
print(quadratic)

bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype)

solver = dimod.ExactSolver()

results = solver.sample(bqm)

#print(results.first)
b 
for i in range(R):
	b[i] = results.first[0][i]

print(b)

#decimal conversion
x = 0
for i in range(R):
	x = 2* (b[i] * 2**(-i)) -1

print(x)


#print(results)

# with dWave
#sampler = dwave.system.EmbeddingComposite(dwave.system.DWaveSampler())
#sampleset = sampler.sample(bqm_k4, num_reads=10)
#dwave.inspector.show(sampleset)
