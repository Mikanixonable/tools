from matplotlib import pyplot as plt
import cv2 as cv2
import numpy as np

img = cv2.imread("s.jpg")
img = cv2.resize(img,(64,64))

print(img)
r = img[:,:,2]
g = img[:,:,1]
b = img[:,:,0]

rgb = np.dstack((r, g, b))
rgb_flat = rgb.reshape((rgb.shape[0]*rgb.shape[1], 3))
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)
cCodes = np.apply_along_axis(rgb_to_hex, 1, rgb_flat)


# print(cCodes)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
ax.scatter(b, g, r, c=cCodes,alpha=1)
plt.savefig("po.png")
plt.show()