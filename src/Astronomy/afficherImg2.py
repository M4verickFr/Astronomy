from matplotlib import pyplot as plt

from astropy.io import fits
from astropy.wcs import WCS
from astropy.utils.data import download_file
import numpy as np
import imutils
import cv2


fits_file = 'https://archive.stsci.edu/cgi-bin/dss_search?v=3&r=03+44.4&d=-44+40&h=10&w=10&f=fits'
image_file = download_file(fits_file, cache=True)
hdu = fits.open(image_file)[0]
# wmap = WCS(hdu.header)
data = hdu.data

img = np.array(data/255, dtype = np.uint8) #Converting float32 to uint8

# Apply adaptive threshold with gaussian size 51x51
thresh_gray = cv2.adaptiveThreshold(img, 255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=255, C=0)

# Find contours, and get the contour with maximum area
cnts = cv2.findContours(thresh_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cnts = imutils.grab_contours(cnts)

c = max(cnts, key=cv2.contourArea)


# Draw contours with maximum size on new mask
mask2 = np.zeros_like(thresh_gray)
ellipse = cv2.fitEllipse(c)
mask2=cv2.ellipse(mask2, ellipse, (36,255,12), -1)

img[(mask2==0)] = 0






























plt.subplot(1, 2, 1)
plt.imshow(data)
plt.subplot(1, 2, 2)
plt.imshow(img)
plt.show()
