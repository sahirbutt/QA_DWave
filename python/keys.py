# Create an empty dictionary
my_dict = {}

# Create a list of keys
keys = ['key1', 'key2', 'key3']
double_key = {}
R = 5
for x in range(R):
	for y in range(R):
		double_key[x,y]=R
print(double_key)

# Populate the dictionary with values using a for loop
i=0
for key in keys:
	i=i+1
	my_dict[key] = i

# Print the resulting dictionary
print(my_dict)
