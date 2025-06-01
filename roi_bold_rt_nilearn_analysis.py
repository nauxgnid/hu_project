import os
import pandas as pd
import numpy as np
from nilearn.image import load_img, smooth_img
from nilearn.masking import apply_mask
from nilearn.input_data import NiftiSpheresMasker
import warnings
warnings.filterwarnings('ignore')

# Define paths
subjects_file = '/home/dingxuan/hu_project/selected_subjects_two.tsv'
output_dir = '/home/dingxuan/hu_project/results'
os.makedirs(output_dir, exist_ok=True)

# Read subjects using pandas to handle TSV with headers
subjects_df = pd.read_csv(subjects_file, sep='\t')
subjects = subjects_df['participant_id'].tolist()  # Extract participant_id column

# Define dlPFC ROI (sphere at MNI coordinates, e.g., right dlPFC: [40, 40, 30])
dlpfc_coords = [(40, 40, 30)]  # 5 mm radius sphere
masker = NiftiSpheresMasker(
    dlpfc_coords, radius=5, standardize=True, t_r=0.49, memory='nilearn_cache')

# Process each subject and run
for subject in subjects:
    for run in ['01', '02']:
        # Define file paths
        bold_path = f'/home/dingxuan/hu_project/output/{subject}/func/{subject}_task-csst_run-{run}_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz'
        confounds_path = f'/home/dingxuan/hu_project/output/{subject}/func/{subject}_task-csst_run-{run}_desc-confounds_timeseries.tsv'

        # Check if files exist
        if not os.path.exists(bold_path):
            print(f"BOLD file not found: {bold_path}")
            continue
        if not os.path.exists(confounds_path):
            print(f"Confounds file not found: {confounds_path}")
            continue

        # Load and smooth BOLD image
        bold_img = load_img(bold_path)
        smoothed_img = smooth_img(bold_img, fwhm=2)

        # Load confounds
        confounds = pd.read_csv(confounds_path, sep='\t')
        confounds_selected = confounds[['trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z', 'global_signal']].fillna(0).values

        # Extract dlPFC time series
        time_series = masker.fit_transform(smoothed_img, confounds=confounds_selected)

        # Save results
        output_file = os.path.join(output_dir, f'{subject}_task-csst_run-{run}_dlpfc_timeseries.csv')
        pd.DataFrame(time_series, columns=['dlpfc']).to_csv(output_file, index=False)
        print(f"Saved: {output_file}")

