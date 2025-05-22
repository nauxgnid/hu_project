import pandas as pd
import os

# Paths
dataset_dir = '/home/dingxuan/hu_project/ds005899'
subjects_file = '/home/dingxuan/hu_project/selected_subjects.tsv'
output_dir = '/home/dingxuan/hu_project/results'
os.makedirs(output_dir, exist_ok=True)

# Load data
try:
    participants = pd.read_csv(f'{dataset_dir}/participants.tsv', sep='\t')
    selected_subjects = pd.read_csv(subjects_file, sep='\t')
except FileNotFoundError as e:
    print(f"Error: File not found - {e}")
    exit(1)

# Check current data for sub-8121, sub-7899
print("Current data for sub-8121, sub-7899:")
print(selected_subjects[selected_subjects['participant_id'].isin(['sub-8121', 'sub-7899'])])

# Recode Gender (1.0=M, 2.0=F)
participants['sex'] = participants['Gender'].map({1.0: 'M', 2.0: 'F'})

# Use existing ADHD from selected_subjects.tsv
participants['ADHD_new'] = participants['ADHD'].astype(int)

# Merge all demographics
updated_subjects = selected_subjects[['participant_id', 'ADHD']].merge(
    participants[['participant_id', 'Age', 'sex', 'visit', 'session', 'runid1', 'runid2']],
    on='participant_id',
    how='left'
)
updated_subjects.rename(columns={'Age': 'age'}, inplace=True)

# Check for missing data
missing_data = updated_subjects[updated_subjects[['ADHD', 'age', 'sex']].isna().any(axis=1)]
if not missing_data.empty:
    print(f"Error: Missing data for:\n{missing_data[['participant_id', 'ADHD', 'age', 'sex']]}")
    exit(1)

# Ensure proper types
updated_subjects['ADHD'] = updated_subjects['ADHD'].astype(int)
updated_subjects['age'] = updated_subjects['age'].astype(float)
updated_subjects['sex'] = updated_subjects['sex'].astype(str)
updated_subjects['visit'] = updated_subjects['visit'].astype(float)
updated_subjects['session'] = updated_subjects['session'].astype(float)
updated_subjects['runid1'] = updated_subjects['runid1'].astype(float)
updated_subjects['runid2'] = updated_subjects['runid2'].astype(float)

# Validate group balance
adhd_count = (updated_subjects['ADHD'] == 1).sum()
td_count = (updated_subjects['ADHD'] == 0).sum()
print(f"\nADHD Group: {adhd_count} subjects")
print(f"TD Group: {td_count} subjects")
if adhd_count != 10 or td_count != 10:
    print("Error: Group imbalance (expected 10 ADHD, 10 TD)")
    exit(1)

# Save updated selected_subjects.tsv
updated_subjects.to_csv(subjects_file, sep='\t', index=False)
print(f"Updated {subjects_file} with all demographic data")

# Save demographics summary
demographics = updated_subjects.copy()
demographics['diagnosis'] = demographics['ADHD'].map({1: 'ADHD', 0: 'TD'})
demographics.to_csv(f'{output_dir}/demographics_summary.csv', index=False)

# Summarize demographics
adhd_group = demographics[demographics['ADHD'] == 1]
td_group = demographics[demographics['ADHD'] == 0]
print("\nADHD Group (n=10):")
print(f"Mean Age: {adhd_group['age'].mean():.2f} (SD: {adhd_group['age'].std():.2f})")
print(f"Sex: {adhd_group['sex'].value_counts().to_dict()}")
print("\nTD Group (n=10):")
print(f"Mean Age: {td_group['age'].mean():.2f} (SD: {td_group['age'].std():.2f})")
print(f"Sex: {td_group['sex'].value_counts().to_dict()}")

# Check updated sub-8121, sub-7899
print("\nUpdated data for sub-8121, sub-7899:")
print(updated_subjects[updated_subjects['participant_id'].isin(['sub-8121', 'sub-7899'])])

# Commit to GitHub
print("\nCommit results with:")
print(f"git add extract_all_demographics.py {subjects_file} results/demographics_summary.csv")
print("git commit -m 'Retrieved all demographic data for selected subjects, preserving sub-8121 ADHD status'")
print("git push origin main")

