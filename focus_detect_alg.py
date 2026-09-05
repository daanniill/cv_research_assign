import numpy as np
from PIL import Image

def generate_gaussian_kernel(size, sigma):
  if size % 2 == 0:
      raise ValueError("Gaussian kernel size must be odd")

  coordinates = np.arange(size) - size // 2
  x, y = np.meshgrid(coordinates, coordinates)

  kernel = np.exp(-(x**2 + y**2) / (2 * sigma**2))
  return kernel / np.sum(kernel)

# implement focus detection by method of laplacion operator
# appply slight gaussian blur to reduce noise before running through laplacian operator
def laplace_alg(img_arr):

  # Gaussian Kernel normalized by 1/16th
  gaussian_kernel = generate_gaussian_kernel(15, 2.5)

  laplace_kernel = np.array([[0, 1, 0],
                              [1, -4, 1],
                              [0, 1, 0]])

  # ----------- CONVOLUTION -----------
  img_h, img_w = img_arr.shape
  gk_h, gk_w = gaussian_kernel.shape
  lk_h, lk_w = laplace_kernel.shape

  # blurred image dims and arr
  blur_h = img_h - gk_h + 1
  blur_w = img_w - gk_w + 1
  blurred_img = np.zeros((blur_h, blur_w))

  for y in range(blur_h):
        for x in range(blur_w):
            window = img_arr[y:y+gk_h, x:x+gk_w]
            blurred_img[y, x] = np.sum(window * gaussian_kernel)

  # output dims
  out_h = blur_h - lk_h + 1
  out_w = blur_w - lk_w + 1
  output = np.zeros((out_h, out_w))

  # sliding kernel across image
  for y in range(out_h):
    for x in range(out_w):
      # getting cur window 3x3
      window = blurred_img[y:y+lk_h, x:x+lk_w]
      # Mult and sum elements
      output[y, x] = np.sum(window * laplace_kernel)

  # ----------- FINAL OUT -----------

  # calculating variance
  mean_val = np.mean(output)
  variance = np.mean((output - mean_val) ** 2)

  return variance

def process_data(src):
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

  return results