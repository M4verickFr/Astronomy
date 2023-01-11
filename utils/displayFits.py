from matplotlib import pyplot as plt

from astropy.io import fits
from astropy.wcs import WCS
from astropy.utils.data import download_file
import numpy as np
import imutils
import cv2

hdu = fits.open("data/new.fits")[0]
wmap = WCS(hdu.header)
data = hdu.data

plt.subplot(1, 1, 1,projection=wmap)
plt.imshow(data)
plt.title('Full image')
plt.xlabel("RA")
plt.ylabel("Dec")

plt.show()