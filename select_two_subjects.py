import pandas as pd

# Paths
subjects_file = '/home/dingxuan/hu_project/selected_subjects.tsv'
output_file = '/home/dingxuan/hu_project/selected_subjects_two.tsv'
ids_file = '/home/dingxuan/hu_project/selected_ids.txt'

# Load data
df = pd.read_csv(subjects_file, sep='\t')

# Select 1 ADHD, 1 TD
selected = df[df['participant_id'].isin(['sub-7565', 'sub-8150'])]

# Verify balance
adhd_count = (selected['ADHD'] == 1).sum()
td_count = (selected['ADHD'] == 0).sum()
print(f"ADHD: {adhd_count}, TD: {td_count}")
if adhd_count != 1 or td_count != 1:
    print("Error: Imbalanced groups")
    exit(1)

# Save new selected_subjects
selected.to_csv(output_file, sep='\t', index=False)
print(f"Saved {output_file}")

# Update selected_ids.txt
with open(ids_file, 'w') as f:
    f.write('\n'.join(selected['participant_id']) + '\n')
print(f"Updated {ids_file}")

# Commit
print("\nCommit with:")
print(f"git add select_two_subjects.py {output_file} {ids_file}")
print("git commit -m 'Selected sub-7565 (ADHD), sub-8150 (TD) for pipeline testing'")
print("git push origin main")

