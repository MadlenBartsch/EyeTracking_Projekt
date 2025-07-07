import os
import random
import pandas as pd
from itertools import combinations

# Set random seed
random.seed(42)

# CONFIGURATION
NUM_SUBJECTS = 20
TRIALS_PER_SUBJECT = 120
IMAGES_PER_CATEGORY = 100
CATEGORIES = ['nature', 'urban', 'indoor']

BASELINE_RATIO = 0.2
NUM_BASELINE = int(TRIALS_PER_SUBJECT * BASELINE_RATIO)
NUM_MANIPULATED = TRIALS_PER_SUBJECT - NUM_BASELINE
MANIPULATION_TYPES = ['size', 'form', 'background']
MANIPULATION_LEVELS = {
    'size': ['big', 'small'],
    'form': ['symmetrical', 'asymmetrical'],
    'background': ['dominant', 'contrary']
}

# Generate image names
images = {
    cat: [f"{cat}_{i:03d}.jpg" for i in range(1, IMAGES_PER_CATEGORY + 1)]
    for cat in CATEGORIES
}

# Generate all unique sorted image pairs
base_pairs = []
for cat1, cat2 in combinations(CATEGORIES, 2):
    for img1 in images[cat1]:
        for img2 in images[cat2]:
            pair = tuple(sorted((img1, img2)))
            base_pairs.append(pair)

random.shuffle(base_pairs)

# Initialize structures
subject_trials = [[] for _ in range(NUM_SUBJECTS)]
used_images_per_subject = [set() for _ in range(NUM_SUBJECTS)]
manipulation_counts_per_subject = [
    {f"{m}_{l}": 0 for m in MANIPULATION_TYPES for l in MANIPULATION_LEVELS[m]}
    for _ in range(NUM_SUBJECTS)
]
baseline_counts_per_subject = [0 for _ in range(NUM_SUBJECTS)]

# Assign each pair to two distinct subjects: normal and mirrored
subject_cycle = list(range(NUM_SUBJECTS))
pair_index = 0

for pair in base_pairs:
    if pair_index + 1 >= NUM_SUBJECTS:
        pair_index = 0

    s1 = subject_cycle[pair_index]
    s2 = subject_cycle[pair_index + 1]

    left, right = pair
    can_assign_s1 = left not in used_images_per_subject[s1] and right not in used_images_per_subject[s1] and len(subject_trials[s1]) < TRIALS_PER_SUBJECT
    can_assign_s2 = left not in used_images_per_subject[s2] and right not in used_images_per_subject[s2] and len(subject_trials[s2]) < TRIALS_PER_SUBJECT

    if not (can_assign_s1 and can_assign_s2):
        pair_index += 2
        continue

    # Assign normal
    trial1 = {'img_left': left, 'img_right': right}
    if baseline_counts_per_subject[s1] < NUM_BASELINE:
        trial1['attribute'] = 'none'
        trial1['value'] = 'none'
        trial1['target_image'] = random.choice(['img_left', 'img_right'])
        cat_l = left.split('_')[0]
        cat_r = right.split('_')[0]
        trial1['cb_index'] = f"baseline_{cat_l}-{cat_r}_{'L' if trial1['target_image'] == 'img_left' else 'R'}"
        baseline_counts_per_subject[s1] += 1
    else:
        possible = [(m, l) for m in MANIPULATION_TYPES for l in MANIPULATION_LEVELS[m]]
        random.shuffle(possible)
        for m_type, m_level in possible:
            key = f"{m_type}_{m_level}"
            if manipulation_counts_per_subject[s1][key] < NUM_MANIPULATED // (len(MANIPULATION_TYPES) * 2):
                trial1['attribute'] = m_type
                trial1['value'] = m_level
                side = random.choice(['img_left', 'img_right'])
                trial1['target_image'] = side
                suffix = 'L' if side == 'img_left' else 'R'
                trial1['cb_index'] = f"{m_type}_{m_level}_{suffix}"
                manipulation_counts_per_subject[s1][key] += 1
                break
        else:
            pair_index += 2
            continue

    trial1['trial_number'] = len(subject_trials[s1]) + 1
    subject_trials[s1].append(trial1)
    used_images_per_subject[s1].update([left, right])

    # Assign mirrored
    trial2 = {'img_left': right, 'img_right': left}
    if baseline_counts_per_subject[s2] < NUM_BASELINE:
        trial2['attribute'] = 'none'
        trial2['value'] = 'none'
        trial2['target_image'] = random.choice(['img_left', 'img_right'])
        cat_l = right.split('_')[0]
        cat_r = left.split('_')[0]
        trial2['cb_index'] = f"baseline_{cat_l}-{cat_r}_{'L' if trial2['target_image'] == 'img_left' else 'R'}"
        baseline_counts_per_subject[s2] += 1
    else:
        possible = [(m, l) for m in MANIPULATION_TYPES for l in MANIPULATION_LEVELS[m]]
        random.shuffle(possible)
        for m_type, m_level in possible:
            key = f"{m_type}_{m_level}"
            if manipulation_counts_per_subject[s2][key] < NUM_MANIPULATED // (len(MANIPULATION_TYPES) * 2):
                trial2['attribute'] = m_type
                trial2['value'] = m_level
                side = random.choice(['img_left', 'img_right'])
                trial2['target_image'] = side
                suffix = 'L' if side == 'img_left' else 'R'
                trial2['cb_index'] = f"{m_type}_{m_level}_{suffix}"
                manipulation_counts_per_subject[s2][key] += 1
                break
        else:
            pair_index += 2
            continue

    trial2['trial_number'] = len(subject_trials[s2]) + 1
    subject_trials[s2].append(trial2)
    used_images_per_subject[s2].update([left, right])

    pair_index += 2

# Save all subject CSV files
output_folder = "subject_sets"
os.makedirs(output_folder, exist_ok=True)

for subj, trials in enumerate(subject_trials):
    if trials:
        # Trials Mischen, damit Baselines nicht nur am Anfang sind
        random.shuffle(trials)

        # trial_number neu setzen
        for idx, trial in enumerate(trials):
            trial['trial_number'] = idx + 1

        df = pd.DataFrame(trials)[[
            'trial_number', 'img_left', 'img_right', 'attribute',
            'value', 'target_image', 'cb_index'
        ]]
        df.to_csv(f"{output_folder}/subject_{subj + 1:02d}.csv", index=False)
    else:
        print(f"Achtung: Keine gültigen Trials für subject_{subj + 1:02d}")

