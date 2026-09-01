import numpy as np

# implement focus detection by method of laplacion operator
def laplace_alg(img_arr):

  laplace_kernel = np.array([[0, 1, 0],
                              [1, -4, 1],
                              [0, 1, 0]])

  # ----------- CONVOLUTION -----------
  img_h, img_w = img_arr.shape
  k_h, k_w = laplace_kernel.shape

  # output dims
  out_h = img_h - k_h + 1
  out_w = img_w -k_w + 1
  output = np.zeros((out_h, out_w))

  # sliding kernel across image
  for y in range(out_h):
    for x in range(out_w):
      # getting cur window 3x3
      window = img_arr[y:y+k_h, x:x+k_w]
      # Mult and sum elements
      output[y, x] = np.sum(window * laplace_kernel)

  # ----------- FINAL OUT -----------

  # calculating variance
  mean_val = np.mean(output)
  variance = np.mean((output - mean_val) ** 2)

  return variance