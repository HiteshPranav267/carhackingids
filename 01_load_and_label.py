import pandas as pd
import os

def load_normal(file_path):
    needed_columns = ['Timestamp', 'ID', 'DLC'] + [f'data[{i}]' for i in range(8)]
    df = pd.read_csv(file_path)
    available_columns = [col for col in needed_columns if col in df.columns]
    df = df[available_columns]
    df.columns = ['timestamp', 'id', 'dlc'] + [f'data[{i}]' for i in range(len(df.columns)-3)]
    df['label'] = 0
    return df

def load_attack(file_path):
    needed_columns = ['Timestamp', 'ID', 'DLC'] + [f'data[{i}]' for i in range(8)] + ['R']
    df = pd.read_csv(file_path)
    available_columns = [col for col in needed_columns if col in df.columns]
    df = df[available_columns]
    # Remove 'R' from columns for renaming
    data_cols = [col for col in available_columns if col != 'R']
    df.columns = ['timestamp', 'id', 'dlc'] + [f'data[{i}]' for i in range(len(data_cols)-3)] + (['R'] if 'R' in available_columns else [])
    # Label: 0 for 'R', 1 for 'T'
    df['label'] = df['R'].apply(lambda x: 0 if str(x).strip().upper() == 'R' else 1)
    df = df.drop(columns=['R'])
    return df

data_dir = 'dataset'

# Load datasets and assign labels
normal = load_normal(os.path.join(data_dir, 'normal_run_data.csv'))
dos = load_attack(os.path.join(data_dir, 'DoS_dataset.csv'))
fuzzy = load_attack(os.path.join(data_dir, 'Fuzzy_dataset.csv'))
gear = load_attack(os.path.join(data_dir, 'gear_dataset.csv'))
rpm = load_attack(os.path.join(data_dir, 'RPM_dataset.csv'))

# Concatenate all data
full_df = pd.concat([normal, dos, fuzzy, gear, rpm], ignore_index=True)

# Shuffle the combined dataset
full_df = full_df.sample(frac=1).reset_index(drop=True)

# Save to CSV
full_df.to_csv('dataset/dataset.csv', index=False)