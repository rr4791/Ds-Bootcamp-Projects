import pandas as pd

# Load dataset
df = pd.read_csv('https://raw.githubusercontent.com/selva86/datasets/master/Cars93_miss.csv')

# Check missing values before
print("Missing values before:\n", df[['Min.Price', 'Max.Price']].isna().sum())

# Replace missing values with column mean
df['Min.Price'].fillna(df['Min.Price'].mean(), inplace=True)
df['Max.Price'].fillna(df['Max.Price'].mean(), inplace=True)

# Verify replacement
print("\nMissing values after:\n", df[['Min.Price', 'Max.Price']].isna().sum())

# Optional: Show first few rows
print("\nUpdated columns:\n", df[['Min.Price', 'Max.Price']].head())
