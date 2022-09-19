from matplotlib import pyplot as plt

from astropy.io import fits
from astropy.wcs import WCS
from astropy.utils.data import download_file
import numpy as np
import imutils
import cv2


fits_file = 'https://archive.stsci.edu/cgi-bin/dss_search?v=3&r=11+23.8&d=-02+06&h=10&w=10&f=fits'
image_file = download_file(fits_file, cache=True)
hdu = fits.open(image_file)[0]
wmap = WCS(hdu.header)
data = hdu.data


img = np.array(data/255, dtype = np.uint8) #Converting float32 to uint8

# Apply adaptive threshold with gaussian size 51x51
thresh_gray = cv2.adaptiveThreshold(img, 255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=255, C=0)

# Find contours, and get the contour with maximum area
cnts = cv2.findContours(thresh_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cnts = imutils.grab_contours(cnts)

c = max(cnts, key=cv2.contourArea)

# Draw contours with maximum size on new mask
mask1 = np.zeros_like(thresh_gray)
ellipse = cv2.fitEllipse(c)
mask1=cv2.ellipse(mask1, ellipse, (36,255,12), -1)

# Smooth mask
kernel = np.ones((10, 10), 'uint8')
mask2 = cv2.dilate(mask1, kernel, iterations=1)
mask2 = cv2.distanceTransform(mask2, cv2.DIST_L2, 3)

# apply mask
data = data * mask2

# Extract region
x,y,w,h = cv2.boundingRect(c)
region = data[y-10:y+h+10, x-10:x+w+10]

# Export fits
hdu = fits.PrimaryHDU(region)
hdul = fits.HDUList([hdu])
hdul.writeto('data/new.fits', overwrite=True)

plt.subplot(1, 3, 1,projection=wmap)
plt.imshow(img)
plt.title('Full image')
plt.xlabel("RA")
plt.ylabel("Dec")

plt.subplot(1, 3, 2,projection=wmap)
plt.imshow(data)
plt.title('xxx')
plt.xlabel("RA")
plt.ylabel(" ")

plt.subplot(1, 3, 3,projection=wmap)
plt.imshow(region)
plt.title('xxx')
plt.xlabel("RA")
plt.ylabel(" ")

plt.show()