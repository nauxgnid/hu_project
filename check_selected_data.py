from bids import BIDSLayout
import pandas as pd

# Load dataset
dataset_path = '/home/dingxuan/hu_project/ds005899'
try:
    layout = BIDSLayout(dataset_path, validate=False)
except Exception as e:
    print(f"Error loading BIDS layout: {e}")
    exit(1)
selected_ids = pd.read_csv('/home/dingxuan/hu_project/selected_subjects.tsv', sep='\t')['participant_id'].tolist()
participants = pd.read_csv(f'{dataset_path}/participants.tsv', sep='\t')

# Check data completeness
data_info = []
for sub in selected_ids:
    t1w_files = layout.get(subject=sub, suffix='T1w', extension='.nii')
    bold_files = layout.get(subject=sub, task='csst', suffix='bold', run=None, extension='.nii.gz')
    event_files = layout.get(subject=sub, task='csst', suffix='events', run=None, extension='.tsv')
    data_info.append({
        'subject': sub,
        'has_t1w': len(t1w_files) > 0,
        'num_bold_runs': len(bold_files),
        'num_event_files': len(event_files),
        'ADHD': participants[participants['participant_id'] == sub]['ADHD'].iloc[0]
    })
data_df = pd.DataFrame(data_info)
valid_subjects = data_df[(data_df['has_t1w']) & (data_df['num_bold_runs'] > 0) & (data_df['num_event_files'] > 0)]

print("Selected subjects data:")
print(data_df[['subject', 'ADHD', 'has_t1w', 'num_bold_runs', 'num_event_files']])
print("\nValid subjects (complete data):")
print(valid_subjects[['subject', 'ADHD', 'has_t1w', 'num_bold_runs', 'num_event_files']])
data_df.to_csv('/home/dingxuan/hu_project/selected_subjects_data.csv', index=False)


