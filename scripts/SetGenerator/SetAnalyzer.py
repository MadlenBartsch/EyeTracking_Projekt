import os
import pandas as pd
from collections import Counter

# Folder containing the subject CSVs
input_folder = "subject_sets"
summary_rows = []

# Analyze each subject file
for filename in sorted(os.listdir(input_folder)):
    if filename.endswith(".csv"):
        subject_id = filename.split('_')[1].split('.')[0]
        df = pd.read_csv(os.path.join(input_folder, filename))

        num_trials = len(df)
        num_baseline = (df['attribute'] == 'none').sum()
        num_manipulated = num_trials - num_baseline

        # Count attributes
        attr_counts = Counter(df['attribute'])
        attr_size = attr_counts.get('size', 0)
        attr_form = attr_counts.get('form', 0)
        attr_background = attr_counts.get('background', 0)

        summary_rows.append({
            'subject_id': subject_id,
            'total_trials': num_trials,
            'num_baseline': num_baseline,
            'num_manipulated': num_manipulated,
            'size': attr_size,
            'form': attr_form,
            'background': attr_background
        })

# Create summary DataFrame
df_summary = pd.DataFrame(summary_rows)

# Save updated summary to CSV
output_folder = "distribution_analysis"
os.makedirs(output_folder, exist_ok=True)
df_summary.to_csv(os.path.join(output_folder, "subject_summary.csv"), index=False)

