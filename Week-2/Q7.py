import pandas as pd
import numpy as np

# Create dataframe with random integers between 10 and 40
df = pd.DataFrame(np.random.randint(10, 40, 60).reshape(-1, 4),
                  columns=['A', 'B', 'C', 'D'])

# Filter rows where the row sum > 100
filtered_rows = df[df.sum(axis=1) > 100]

print("Original DataFrame:\n", df)
print("\nRows where row sum > 100:\n", filtered_rows)
