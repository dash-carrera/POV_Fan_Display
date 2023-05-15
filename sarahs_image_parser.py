# sarah tests
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image

image_name = "ghost.png"

def get_polar_coordinates(x, y):
  # Given an x,y coordinate pair, output the coordinates in percent polar coordinates
  # (percent_around_circle, radius)
  r = np.sqrt(pow(x, 2)+pow(y, 2))
  theta = np.arctan2(y, x)
  percent_around_circle = (theta+np.pi)/(2*np.pi)
  return percent_around_circle, r

def cartesian_to_polar(x, y):
  # Given an x,y coordinate pair, output the polar coordinates
  r = np.sqrt(pow(x, 2)+pow(y, 2))
  theta = np.arctan2(y, x)
  return r, theta

def polar_to_cartesian(r, theta):
  # Given an r, theta coordinate pair, output the cartesian coordinates
  theta = theta * math.pi / 180.
  # print(theta)
  x = r * np.cos(theta)
  y = r * np.sin(theta)
  return x, y

def downsample_image(image_path):
  # # Open the image
  # image = Image.open(image_path).convert("RGB")
  # # print(image)
  # # image size should be 623x623 (RGB)
  # image.thumbnail((49,49), Image.Resampling.LANCZOS)
  # # print(image)
  # image.save('resized_image.png')
  # # Convert the image to a numpy array
  # img_array = np.array(image.getdata())

  # rgb_arr = img_array.reshape((49,49,3))
  # rgb_arr = rgb_arr[:, :, :3] #Remove alpha channel if present
  # return rgb_arr
  image = Image.open(image_path)
  resized_image = image.resize((49, 49), Image.Resampling.LANCZOS)
  resized_image.save('resized_image.png')
  # Convert the image to a numpy array
  rgb_arr = np.array(resized_image)
  rgb_arr = rgb_arr[:, :, :3] #Remove alpha channel if present
  return rgb_arr

def led_strip_to_pixel(degree=0):
  # Given a degree, output the pixel number on the LED strip
  # LED strip has 72 lights
  pixel_indices = np.zeros((72,2)) # should be shape (72,2)
  # go backwards for left side
  # print("degree: ", degree)
  # print("degree + 180: ", (degree + 180) % 360)
  i = 0
  for r in np.linspace(35,0,36):
    x,y = polar_to_cartesian(r, (degree + 180) % 360)
    x = math.floor(x)
    y = math.floor(y)
    if x > 24 or y > 24 or x < -24 or y < -24:
      pixel_indices[i] = np.array((-1, -1))
      i = i + 1
    else:
      pixel_indices[i] = np.array((x+24, 24-y))
      i = i + 1

  # go forwards for right side
  for r in np.linspace(0,35,36):
    x,y = polar_to_cartesian(r, degree % 360)
    x = math.floor(x)
    y = math.floor(y)
    if x > 24 or y > 24 or x < -24 or y < -24:
      pixel_indices[i] = np.array((-1, -1))
      i = i + 1
    else:
      pixel_indices[i] = np.array((x+24, 24-y))
      i = i + 1

  return pixel_indices

max_degree = 360
anim_pixels = []
for degree in range(0,max_degree):
  pixel_indices = led_strip_to_pixel(degree)
  print(pixel_indices.shape)
  anim_pixels.append(pixel_indices)
  # for i in range(72):
  #   print(pixel_indices[i])
print(len(anim_pixels))

img = downsample_image(image_name)
# t = anim_pixels[0]
# print(t[15,:])
# t = t.astype(int)
# print(t)
# if t[15,0] != -1:
#   print("true")
#   print(img[t])
# s = img[t]
# print(s.shape)

# # create the figure and axes objects
# fig, ax = plt.subplots()

# # function that draws each frame of the animation
# def animate(i):
#   ax.clear()
#   pixel_indices = anim_pixels[i]
#   pixel_indices = pixel_indices.astype(int)
#   x = pixel_indices[:,0]
#   y = pixel_indices[:,1]
#   ax.set_xlim(0,49)
#   ax.set_ylim(0,49)
#   ax.scatter(x,y, c=img[x,y]/255, s=100)

# # run the animation
# ani = FuncAnimation(fig, animate, frames=range(0,max_degree), interval=5, repeat=False)
# ani.save('ghost.gif', writer='imagemagick', fps=30)

# plt.show()



with open('./image.h', 'w') as f: 
  f.write('const float image[360][290] ICACHE_FLASH_ATTR = {\n');
  for degree in range(0,max_degree):
    f.write('{')
    inds = anim_pixels[degree]
    print(inds.shape)
    print(img.shape)
    ind = inds[15]
    print(inds)
    # print(img[tuple(ind.astype(int))])
    img_pixels = img[inds[:,0].astype(int), inds[:,1].astype(int)]
    for i in range(72):
      ind = inds[i]
      if ind[0] != -1:
        if not (img_pixels[i,0] == 0 and img_pixels[i,1] == 0 and img_pixels[i,2] == 0):
          f.write(f'{i}, {img_pixels[i,0]}, {img_pixels[i,1]}, {img_pixels[i,2]},')
    print(img_pixels.shape)
    f.write('-1},\n')
  f.write('};')