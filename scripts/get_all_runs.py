from bids import BIDSLayout
import os
layout = BIDSLayout('/home/dingxuan/hu_project/ds005899', validate=False)
selected_ids = pd.read_csv('/home/dingxuan/hu_project/selected_subjects.tsv', sep='\t')['participant_id'].tolist()
for sub in selected_ids:
    bold_files = layout.get(subject=sub, task='csst', suffix='bold', run=None, extension='.nii.gz')
    event_files = layout.get(subject=sub, task='csst', suffix='events', run=None, extension='.tsv')
    t1w_files = layout.get(subject=sub, suffix='T1w', extension='.nii')
    for f in bold_files + event_files + t1w_files:
        print(fGetting {f.path})
        os.system(fdatalad get {f.path})
