# replacement
import pandas as pd

# Load data
dataset_path = '/home/dingxuan/hu_project/ds005899'
participants = pd.read_csv(f'{dataset_path}/participants.tsv', sep='\t')
selected_subjects = pd.read_csv('/home/dingxuan/hu_project/selected_subjects.tsv', sep='\t')

# Verify subjects exist
replacements = {'sub-8168': 'sub-8121', 'sub-7957': 'sub-7899'}
for old_sub, new_sub in replacements.items():
    if old_sub not in selected_subjects['participant_id'].values:
        print(f"Error: {old_sub} not in selected subjects")
        continue
    if new_sub not in participants['participant_id'].values:
        print(f"Error: {new_sub} not in participants.tsv")
        continue

    # Get ADHD status
    old_adhd = selected_subjects[selected_subjects['participant_id'] == old_sub]['ADHD'].iloc[0]
    new_adhd = participants[participants['participant_id'] == new_sub]['ADHD'].iloc[0]
    if old_adhd != new_adhd:
        print(f"Warning: ADHD mismatch for {old_sub} (ADHD={old_adhd}) and {new_sub} (ADHD={new_adhd})")

    # Replace subject
    new_sub_data = participants[participants['participant_id'] == new_sub][['participant_id', 'ADHD']]
    selected_subjects = selected_subjects[selected_subjects['participant_id'] != old_sub]
    selected_subjects = pd.concat([selected_subjects, new_sub_data], ignore_index=True)
    print(f"Replaced {old_sub} with {new_sub} (ADHD={new_adhd})")

# Verify ADHD/TD balance
adhd_count = selected_subjects['ADHD'].sum()
td_count = len(selected_subjects) - adhd_count
print(f"ADHD count: {adhd_count}, TD count: {td_count}")
if adhd_count != 10 or td_count != 10:
    print("Warning: ADHD/TD balance not maintained")

# Save updated lists
selected_subjects.to_csv('/home/dingxuan/hu_project/selected_subjects.tsv', sep='\t', index=False)
selected_subjects['participant_id'].to_csv('/home/dingxuan/hu_project/selected_ids.txt', index=False, header=False)
print("Updated subjects:", selected_subjects['participant_id'].tolist())

