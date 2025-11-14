import pandas as pd
import numpy as np

# Define input and output file paths
input_file = "data/pra_water_quality.csv"
output_file = "data/pra_water_quality_cleaned.csv"

# Read the CSV file
print(f"Reading data from {input_file}...")
df = pd.read_csv(input_file)

# Log initial shape of the data
print(f"Initial data shape: {df.shape}")

# 1. Handle missing values
# Replace missing numerical values with the median for pollutants
for col in ['mercury', 'turbidity', 'arsenic', 'lead']:
    df[col] = df[col].fillna(df[col].median())

# Replace missing latitude/longitude with 0 (or drop rows if preferred)
df['latitude'] = df['latitude'].fillna(0)
df['longitude'] = df['longitude'].fillna(0)

# Replace missing dates with a placeholder
df['date'] = df['date'].fillna('2025-01-01')

# Replace missing location with 'Unknown'
df['location'] = df['location'].fillna('Unknown')

# 2. Validate data types and ranges
# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Ensure numerical columns are float
for col in ['mercury', 'turbidity', 'arsenic', 'lead', 'latitude', 'longitude']:
    df[col] = df[col].astype(float)

# 3. Remove outliers (e.g., negative values for pollutants)
for col in ['mercury', 'turbidity', 'arsenic', 'lead']:
    df[col] = df[col].apply(lambda x: x if x >= 0 else np.nan)
    df[col] = df[col].fillna(df[col].median())

# 4. Log final shape of the data
print(f"Final data shape after cleaning: {df.shape}")

# Save the cleaned data
print(f"Saving cleaned data to {output_file}...")
df.to_csv(output_file, index=False)
print("Cleaning complete!")
