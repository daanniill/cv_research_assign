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
for img_set, quadrants in results.items():
  print(f"Results for {img_set}:")
  for quadrant, variances in quadrants.items():
    names = [img_name for img_name, _ in variances]
    print(f"  Quadrant {quadrant}: files={names}")
    for img_name, variance in variances:
      print(f"    {img_name}: {variance}")
