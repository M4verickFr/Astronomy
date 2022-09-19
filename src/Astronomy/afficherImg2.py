from matplotlib import pyplot as plt

from astropy.io import fits
from astropy.wcs import WCS
from astropy.utils.data import download_file
import numpy as np
import imutils
import cv2


fits_file = 'https://archive.stsci.edu/cgi-bin/dss_search?v=3&r=09+09.6&d=+33+08&h=10&w=10&f=fits'
image_file = download_file(fits_file, cache=True)
hdu = fits.open(image_file)[0]
wmap = WCS(hdu.header)
data = hdu.data

img = np.array(data/255, dtype = np.uint8) #Converting float32 to uint8

# Apply adaptive threshold with gaussian size 51x51
thresh_gray = cv2.adaptiveThreshold(img, 255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=255, C=0)

# Find connected components (clusters)
nlabel,labels,stats,centroids = cv2.connectedComponentsWithStats(thresh_gray, connectivity=8)

# Find second largest cluster (the cluster is the background):
max_size = np.max(stats[1:, cv2.CC_STAT_AREA])
max_size_idx = np.where(stats[:, cv2.CC_STAT_AREA] == max_size)[0][0]

mask = np.zeros_like(thresh_gray)

# Draw the cluster on mask
mask[labels == max_size_idx] = 255

# Use "open" morphological operation for removing some artifacts
mask = cv2.morphologyEx(thresh_gray, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5)))

# Find contours, and get the contour with maximum area
cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cnts = imutils.grab_contours(cnts)

c = max(cnts, key=cv2.contourArea)

ellipse = cv2.fitEllipse(c)
cv2.ellipse(img, ellipse, (36,255,12), 2)

# Draw contours with maximum size on new mask
mask2 = np.zeros_like(mask)
mask2=cv2.ellipse(mask2, ellipse, (36,255,12), -1)
# cv2.drawContours(mask2, [c], -1, 255, -1)

img[(mask2==0)] = 0






























plt.subplot(1, 2, 1)
plt.imshow(data)
plt.subplot(1, 2, 2)
plt.imshow(img)
plt.show()
