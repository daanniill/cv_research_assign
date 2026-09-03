import numpy as np

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