import numpy as np

# Define two custom numpy arrays
A = np.array([[1, 2, 3],
              [4, 5, 6]])

B = np.array([[7, 8, 9],
              [10, 11, 12]])

# Stack arrays vertically
vertical_stack = np.vstack((A, B))

# Stack arrays horizontally
horizontal_stack = np.hstack((A, B))

print("Array A:\n", A)
print("Array B:\n", B)
print("\nVertically Stacked Array:\n", vertical_stack)
print("\nHorizontally Stacked Array:\n", horizontal_stack)
