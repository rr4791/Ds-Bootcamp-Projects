import numpy as np

# Define a custom numpy array
A = np.array([2, 5, 7, 10, 12, 4, 9])

# Extract numbers between 5 and 10
filtered_values = A[(A >= 5) & (A <= 10)]

print("Array A:", A)
print("Numbers between 5 and 10:", filtered_values)
