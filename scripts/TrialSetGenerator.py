import csv
import os
import random
from itertools import product, combinations, cycle
from collections import defaultdict, Counter
import pandas as pd

# Konfiguration
categories = ["nature", "indoor", "urban"]
attributes = {
    "size": ["small", "big"],
    "form": ["symmetrical", "asymmetrical"],
    "background": ["dominant", "contrary"]
}
n_images_per_category = 15
n_subjects = 10
output_dir = "subject_lists"

# random seed für Replizierbarkeit
random.seed(5534)

# Bildnamen erzeugen
def generate_image_list(n, category):
    return [f"{category}_{i+1}" for i in range(n)]

images_by_category = {cat: generate_image_list(n_images_per_category, cat) for cat in categories}

# Attributkombinationen generieren
def generate_all_image_attribute_combinations():
    combinations_all = []
    for cat in categories:
        for img in images_by_category[cat]:
            for attr, values in attributes.items():
                for val in values:
                    combinations_all.append({
                        "image": img,
                        "category": cat,
                        "attribute": attr,
                        "value": val
                    })
    return combinations_all

# Trials generieren
def generate_all_trials(image_combos):
    trials = []
    all_images = [img for cat in categories for img in images_by_category[cat]]
    comparison_pool = cycle(all_images)
    used_as_comparison = set()

    for combo in image_combos:
        attr_img = combo["image"]
        attr = combo["attribute"]
        val = combo["value"]
        cat = combo["category"]

        valid_other_images = [
            img for c in categories if c != cat
            for img in images_by_category[c]
            if img != attr_img
        ]

        comparison_img = None
        while True:
            candidate = next(comparison_pool)
            if candidate in valid_other_images:
                comparison_img = candidate
                break

        used_as_comparison.add(comparison_img)

        trials.append({
            "img_left": attr_img,
            "img_right": comparison_img,
            "attribute": attr,
            "value": val,
            "target_image": "img_left",
            "cb_index": f"{attr}_{val}_L"
        })

        trials.append({
            "img_left": comparison_img,
            "img_right": attr_img,
            "attribute": attr,
            "value": val,
            "target_image": "img_right",
            "cb_index": f"{attr}_{val}_R"
        })

    return trials

# Baseline-Trials generieren
def generate_baseline_trials():
    trials = []
    cat_pairs = list(combinations(categories, 2))
    for cat1, cat2 in cat_pairs:
        img_pairs = list(zip(images_by_category[cat1], images_by_category[cat2])) 
        for img1, img2 in img_pairs:
            target_pos = random.choice(["img_left", "img_right"])
            trials.append({
                "img_left": img1,
                "img_right": img2,
                "attribute": "none",
                "value": "none",
                "target_image": target_pos,
                "cb_index": f"baseline_{cat1}-{cat2}_L"
            })
            target_pos = random.choice(["img_left", "img_right"])
            trials.append({
                "img_left": img2,
                "img_right": img1,
                "attribute": "none",
                "value": "none",
                "target_image": target_pos,
                "cb_index": f"baseline_{cat2}-{cat1}_R"
            })
    return trials

# Balanced Listen für Probanden
def generate_subject_lists_balanced():
    os.makedirs(output_dir, exist_ok=True)
    all_attr_trials = generate_all_trials(generate_all_image_attribute_combinations())
    baseline_trials = generate_baseline_trials()
    total_trials = all_attr_trials + baseline_trials

    random.shuffle(total_trials)
    balanced_lists = [[] for _ in range(n_subjects)]

    # Round Robin auf die Probanden verteilen
    for i, trial in enumerate(total_trials):
        balanced_lists[i % n_subjects].append(trial)

    # Einzelne Probandenliste nochnmal mischen
    for i, subject_trials in enumerate(balanced_lists):
        random.shuffle(subject_trials)
        filename = os.path.join(output_dir, f"subject_{i+1}.csv")
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["trial_number", "img_left", "img_right", "attribute", "value", "target_image", "cb_index"])
            writer.writeheader()
            for j, trial in enumerate(subject_trials, start=1):
                trial_with_number = trial.copy()
                trial_with_number["trial_number"] = j
                writer.writerow(trial_with_number)

    return balanced_lists

# Logs über die Attributverteilung
def log_attribute_distribution(subject_lists):
    results = []

    for i, trials in enumerate(subject_lists):
        counts = Counter()
        for trial in trials:
            key = trial['cb_index']
            counts[key] += 1

        total = sum(counts.values())
        summary = {"Subject": f"subject_{i+1}"}
        summary.update(counts)
        summary["Total"] = total
        results.append(summary)

    return pd.DataFrame(results)

# Logs über die Bildverteilung
def log_image_distribution(subject_lists):
    usage_counts = defaultdict(lambda: {"as_img_left": 0, "as_img_right": 0, "as_target": 0, "as_comparison": 0})

    for trials in subject_lists:
        for trial in trials:
            img1 = trial["img_left"]
            img2 = trial["img_right"]
            target = trial["target_image"]

            usage_counts[img1]["as_img_left"] += 1
            usage_counts[img2]["as_img_right"] += 1
            usage_counts[target]["as_target"] += 1

            # Vergleichsbild ist das andere Bild, das nicht das Target ist
            comparison = img2 if target == img1 else img1
            usage_counts[comparison]["as_comparison"] += 1

    # DataFrame erzeugen
    data = []
    for image, counts in usage_counts.items():
        entry = {"image": image}
        entry.update(counts)
        entry["total"] = sum(counts.values())
        data.append(entry)

    df = pd.DataFrame(data)
    df = df.sort_values("image").reset_index(drop=True)
    return df



# Ausführen
subject_lists = generate_subject_lists_balanced()

log_attribute_distribution = log_attribute_distribution(subject_lists)
log_attribute_distribution.to_csv("log/attribute_distribution.csv", index=False)

log_image_distribution = log_image_distribution(subject_lists)
log_image_distribution.to_csv("log/image_distribution.csv", index=False)
