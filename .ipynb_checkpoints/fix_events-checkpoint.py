import pandas as pd
from bids import BIDSLayout
import os

# Load dataset and selected subjects
dataset_path = '/home/dingxuan/hu_project/ds005899'
try:
    layout = BIDSLayout(dataset_path, validate=False)
except Exception as e:
    print(fError loading BIDS layout: {e})
    exit(1)

selected_ids_file = '/home/dingxuan/hu_project/selected_subjects.tsv'
if not os.path.exists(selected_ids_file):
    print(fError: {selected_ids_file} not found)
    exit(1)
selected_ids = pd.read_csv(selected_ids_file, sep='\t')['participant_id'].tolist()

# Fix event files for all runs
for sub in selected_ids:
    event_files = layout.get(subject=sub, task='csst', suffix='events', run=None, extension='.tsv')
    if not event_files:
        print(fNo event files found for {sub})
        continue
    for event_file in event_files:
        try:
            df = pd.read_csv(event_file.path, sep='\t')
            df = df.fillna('n/a')
            df.to_csv(event_file.path, sep='\t', index=False)
            print(fUpdated {event_file.path})
        except Exception as e:
            print(fError updating {event_file.path}: {e})

print(Finished updating event files)
