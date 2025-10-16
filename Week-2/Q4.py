import numpy as np

# Load iris data (only numeric columns)
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
iris_2d = np.genfromtxt(url, delimiter=',', dtype='float', usecols=[0,1,2,3])

# Filter condition:
# petallength (col index 2) > 1.5
# sepallength (col index 0) < 5.0
filtered_rows = iris_2d[(iris_2d[:, 2] > 1.5) & (iris_2d[:, 0] < 5.0)]

print("Filtered rows (petallength > 1.5 and sepallength < 5.0):")
print(filtered_rows)
