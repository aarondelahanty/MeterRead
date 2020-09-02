import os
import matplotlib.pyplot as plt
from skimage import data
from skimage import io
from skimage import util

from skimage.color import rgb2gray
from skimage.filters import threshold_mean, threshold_local, threshold_otsu, rank
from skimage.morphology import erosion, dilation, opening, closing, white_tophat, disk, remove_small_objects
from skimage.transform import rescale

#Read in the original meter image
meter = io.imread('meter0001.jpg')

#Convert to grayscale and assign to preprocessed
grayscale = rgb2gray(meter)

#Define threshold
thresh = threshold_mean(grayscale)
binary = grayscale > thresh

#Otsu Threshold
thresh_otsu = threshold_otsu(grayscale)
binary_otsu = grayscale > thresh_otsu

#Local threshold is likely better:
block_size = 401
local_thresh = threshold_local(grayscale, block_size, offset = 0)
binary_local = grayscale > local_thresh

# Erode
selem = disk(8)
eroded = erosion(binary_local,selem)

# Dilate after erosion (same as 'opening')
selem = disk(12)
eroded_dilated = dilation(eroded,selem)

#White tophat method (ontop of erodeed-dialted)
selem = disk(24)
phantom = eroded_dilated.copy()
phantom[340:350, 200:210] = 255
phantom[100:110, 200:210] = 0
w_tophat = white_tophat(phantom, selem)

#Find the complementary (erode-dilate minus w_tophat)
complementary = eroded_dilated ^ w_tophat

#Inver for black letters on white background
invert = util.invert(complementary)

#Crop to two ROIs Meter I and Meter II
ROI_I = invert[380:840,310:2880]
ROI_II = invert[1940:2390,220:2770]

#Remove small objects (including edge objects, seems to only work with white on black, hence double invert)
meterI = util.invert(remove_small_objects(util.invert(ROI_I),min_size = 9000))
meterII = util.invert(remove_small_objects(util.invert(ROI_II),min_size = 9000))

#Finally resize to recommended 300dpi...
meterI = rescale(meterI, .25)
meterII = rescale(meterII, .25)

#Write out preprocessed image
io.imsave("preprocessed.png",complementary)
io.imsave("meterI.png",meterI)
io.imsave("meterII.png",meterII)
#For test purposes:
#
# fig, axes = plt.subplots(2, 4, figsize=(8, 4))
# ax = axes.ravel()
#
# ax[0].imshow(meter)
# ax[0].set_title("Original")
# ax[1].imshow(grayscale, cmap=plt.cm.gray)
# ax[1].set_title("Grayscale")
# ax[2].imshow(binary, cmap=plt.cm.gray)
# ax[2].set_title("Mean Threshold")
# ax[3].imshow(binary_otsu, cmap=plt.cm.gray)
# ax[3].set_title("Otsu Threshold")
# ax[4].imshow(binary_local, cmap=plt.cm.gray)
# ax[4].set_title("Local Threshold")
# ax[5].imshow(eroded, cmap=plt.cm.gray)
# ax[5].set_title("Eroded")
# ax[6].imshow(eroded_dilated, cmap=plt.cm.gray)
# ax[6].set_title("Dilated")
# ax[7].imshow(eroded_dilated ^ w_tophat, cmap=plt.cm.gray)
# ax[7].set_title("White hat")
#
# fig.tight_layout()
# plt.show()
