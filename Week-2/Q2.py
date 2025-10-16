import numpy as np

# Define two custom numpy arrays
A = np.array([1, 2, 3, 4, 5])
B = np.array([4, 5, 6, 7, 8])

# Find common elements (intersection)
common_elements = np.intersect1d(A, B)

print("Array A:", A)
print("Array B:", B)
print("Common Elements:", common_elements)
