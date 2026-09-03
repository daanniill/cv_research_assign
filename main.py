import csv
from pathlib import Path
from itertools import islice
import numpy as np
from PIL import Image
from focus_detect_alg import laplace_alg

src = Path("dataset")

dataset = {}

for img_set in src.iterdir():   # just the first dataset folder (12 images)
  if img_set.is_dir(): 
    dataset[img_set.name] = {} # organize based on each specific set of images

    for quadrant in img_set.iterdir():
      if quadrant.is_dir():
        dataset[img_set.name][quadrant.name] = []

        imgs = quadrant.glob("*.png")
        for img_path in imgs:
          try:
            with Image.open(img_path) as img:
              # convert image to numpy array
              img_array = np.array(img)
              dataset[img_set.name][quadrant.name].append((img_path.name, img_array)) #add image name + array to that specific set of images
          except Exception as e:
            print(f"Error converting {img_path.name} in {img_set.name}/{quadrant.name}: {e}")


# run focus detection algorithm on each image and store the results
results = {}

for img_set, quadrants in dataset.items():
  results[img_set] = {}

  for quadrant, images in quadrants.items():
    results[img_set][quadrant] = []

    for img_name, img_array in images:
      try:
        height, width = img_array.shape

        if quadrant in ("Q1", "Q4"):
            roi = img_array[:, width // 2:]
        else:  # Q2 and Q3
            roi = img_array[:, :width // 2]

        variance = laplace_alg(roi)
        results[img_set][quadrant].append((img_name, variance))
      except Exception as e:
        print(f"Error processing {img_name} in {img_set}/{quadrant}: {e}")

# print the results
ground_truth = {}

with open("ground_truth_files.csv", newline="") as f:
  for row in csv.DictReader(f):
    key = (row["folder"], row["quadrant"])
    ground_truth[key] = row["ground_truth_filename"]

correct = 0
total = 0


for img_set, quadrants in results.items():
  for quadrant, variances in quadrants.items():
    key = (img_set, quadrant)
    focused_img = ground_truth.get(key)

    pred_file, highest_var = max(variances, key=lambda item: item[1])

    true_file = ground_truth[(img_set, quadrant)]
    is_correct = pred_file == true_file

    correct += int(is_correct)
    total += 1


success_rate = correct / total * 100

print(f"\nCorrect: {correct}/{total}")
print(f"Incorrect: {total - correct}/{total}")
print(f"Success rate: {success_rate:.1f}%")