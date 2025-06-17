import pandas as pd
from utils import hex_to_int

# Load combined data
df = pd.read_csv('dataset/dataset.csv')
print(df.columns.tolist())

# Convert id
df['id'] = df['id'].apply(hex_to_int)

# Convert all data bytes
for i in range(8):
    df[f'data[{i}]'] = df[f'data[{i}]'].apply(hex_to_int)

# Save preprocessed data
print("Saving preprocessed file...")
df.to_csv('dataset/data_preprocessed.csv', index=False)