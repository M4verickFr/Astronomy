from matplotlib import pyplot as plt

from astropy.io import fits
from astropy.wcs import WCS
from astropy.utils.data import download_file
import numpy as np
import cv2


fits_file = 'https://archive.stsci.edu/cgi-bin/dss_search?v=3&r=09+09.6&d=+33+08&h=10&w=10&f=fits'
image_file = download_file(fits_file, cache=True)
hdu = fits.open(image_file)[0]
wmap = WCS(hdu.header)
data = hdu.data

fig = plt.figure()
ax1 = fig.add_subplot(121, projection=wmap)
ax2 = fig.add_subplot(122, projection=wmap)
# Scale input image
bottom, top = 0., 12000.
data = (((top - bottom) * (data - data.min())) / (data.max() - data.min())) + bottom


'''First plot'''
ax1.imshow(data, origin='lower', cmap='gist_heat_r')

# Now plot contours
xcont = np.arange(np.size(data, axis=1))
ycont = np.arange(np.size(data, axis=0))
colors = ['forestgreen','green', 'limegreen']
levels = [2000., 7000., 11800.]

ax1.contour(xcont, ycont, data, colors=colors, levels=levels, linewidths=0.5, smooth=16)
ax1.set_xlabel('RA')
ax1.set_ylabel('Dec')
ax1.set_title('Full image')



''' Second plot '''

ax2.imshow(data, origin='lower', cmap="gist_heat_r")
ax2.contour(xcont, ycont, data, colors=colors, levels=levels, linewidths=0.5, smooth=16)

ax2.set_xlabel('RA')
ax2.set_ylabel('')
ax2.set_title('Sliced image')
plt.show()