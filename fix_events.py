import pandas as pd
from bids import BIDSLayout
import os
import subprocess

# Load dataset
dataset_path = '/home/dingxuan/hu_project/ds005899'
print(f"Checking dataset path: {dataset_path}")
if not os.path.exists(dataset_path):
    print("Error: Dataset path does not exist")
    exit(1)

try:
    layout = BIDSLayout(dataset_path, validate=False)
except Exception as e:
    print(f"Error loading BIDS layout: {e}")
    exit(1)

# Load all subjects from participants.tsv
participants_file = f'{dataset_path}/participants.tsv'
if not os.path.exists(participants_file):
    print(f"Error: {participants_file} not found")
    exit(1)
participants = pd.read_csv(participants_file, sep='\t')
selected_ids = participants['participant_id'].tolist()

# Fix event files for all runs
modified_files = []
for sub in selected_ids:
    event_files = layout.get(subject=sub, task='csst', suffix='events', run=None, extension='.tsv')
    if not event_files:
        print(f"No event files found for {sub}")
        continue
    for event_file in event_files:
        try:
            # Unlock file to allow modifications
            print(f"Unlocking {event_file.path}")
            subprocess.run(['git', 'annex', 'unlock', event_file.path], check=True, cwd=dataset_path)

            # Read TSV, treating multiple NaN-like values as NaN
            df = pd.read_csv(event_file.path, sep='\t', na_values=['NaN', 'nan', 'NA', '', ' ', 'None'])
            if df.isna().any().any():
                print(f"Found NaN values in {event_file.path}")
                df = df.fillna('n/a')
                df.to_csv(event_file.path, sep='\t', index=False)
                print(f"Updated {event_file.path}")
                modified_files.append(event_file.path)
            else:
                print(f"No NaN values found in {event_file.path}")

            # Verify changes
            df_verify = pd.read_csv(event_file.path, sep='\t')
            if df_verify.isin(['NaN', 'nan', 'NA', '', ' ', 'None']).any().any() or df_verify.isna().any().any():
                print(f"Warning: {event_file.path} still contains NaN-like values or NaN")
            else:
                print(f"Verified: {event_file.path} has no NaN-like values")
        except Exception as e:
            print(f"Error processing {event_file.path}: {e}")

# Commit changes to prevent DataLad reversion
if modified_files:
    try:
        subprocess.run(['git', 'add'] + modified_files, check=True, cwd=dataset_path)
        subprocess.run(['git', 'commit', '-m', 'Fixed NaN values in event files'], check=True, cwd=dataset_path)
        print("Committed modified event files")
    except Exception as e:
        print(f"Error committing changes: {e}")

print("Finished updating event files")
