from pathlib import Path
import numpy as np
from PIL import Image

src = Path("dataset")

dataset = {}

for img_set in src.iterdir():
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
              dataset[img_set.name][quadrant.name].append(img_array) #add image array to that specific set of images
          except Exception as e:
            print(f"Error converting {img_path.name} in {img_set.name}/{quadrant.name}: {e}")
