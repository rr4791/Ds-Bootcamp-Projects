import pandas as pd

# Load dataset
df = pd.read_csv('https://raw.githubusercontent.com/selva86/datasets/master/Cars93_miss.csv')

# Select every 20th row starting from 0
filtered_df = df.loc[::20, ['Manufacturer', 'Model', 'Type']]

print(filtered_df)
