import dimod
import numpy as np
# from dwave.system.samplers import DWaveSampler
# from dwave.system.composites import EmbeddingComposite

S = [15, 5, 11, 31, 42, -10]
c=0
for s in S:
	c+=s

linear = {}
quadratic = {}
offset = 0.0
vartype = dimod.BINARY

for i,s_i in enumerate(S):
	for j,s_j in enumerate(S):
		if i==j:
			quadratic[i,j] = s_i * s_j - c * s_i
		else:
			quadratic[i,j] = s_i * s_j
print(f'c = ',c)


# #For the dict n_rows = max(i for i, j in quadratic.keys()) + 1
n_rows = len(S)
quad = np.zeros((n_rows,n_rows))

for i in range(n_rows):
	for j in range(n_rows):
		quad[i,j] = quadratic.get((i,j),0)


print(f'Quadratic = \n',quad)



bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype)


sampler = dimod.ExactSolver()
sample_set = sampler.sample(bqm)
# print("Using ExactSolver()")
# print(sample_set)

# Get the bitstrings with the lowest energy values
lowest_energy_samples = sample_set.lowest()

bitstrings = []
energies = []

for k, (sample, energy) in enumerate(lowest_energy_samples.data(['sample', 'energy'])):
    bitstring = [sample[i] for i in sorted(sample.keys())]  # Convert dict to bitstring
    print(f"Bitstring {k}: {bitstring}, Energy: {energy}")
    bitstrings.append(bitstring)
    energies.append(energy)

# print(bitstrings[1], energies[1])

# Find the two sets according to the lowest_bitstrings

set_1 = np.zeros((len(bitstrings),len(bitstrings[0])))
set_2 = np.zeros((len(bitstrings),len(bitstrings[0])))
sum_1_2 = np.zeros((len(bitstrings),2))

for i,bitstring in enumerate(bitstrings):
	for j,bit in enumerate(bitstring):
		if bit==1:
			set_1[i,j] = S[j]
			set_2[i,j] = 0.0
			sum_1_2[i,0] += S[j]
		else:
			set_2[i,j] = S[j]
			set_1[i,j] = 0.0
			sum_1_2[i,1] += S[j]

print('Solutions in Set_1: \n',set_1)
print('Solutions in Set_2: \n',set_2)
print('Sums for Set_1, Set_2: \n',sum_1_2)


