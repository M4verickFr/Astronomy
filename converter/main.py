#!/usr/bin/env python

from pymongo import MongoClient
from matplotlib import pyplot as plt

from utils import *

from astropy.io import fits
from astropy.wcs import WCS
from astropy.utils.data import download_file
import numpy as np
import imutils
import cv2
import skimage.exposure
import operator
import json

# Setup MongoDB client
client = MongoClient("mongo:27017")
db = client.Spativis
sn_collection = db["supernovas"]

try:
    client.admin.command('ismaster')
except:
    print("Server not available")
    exit()

# Get supernova to convert
sn = sn_collection.find_one({'name': '2015ay'})
print(sn['url'])

# Download fits file of supernova
image_file = download_file(sn['url'], cache=True)
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
ellipse = cv2.fitEllipse(c)
mask1 = np.zeros_like(thresh_gray)
mask1=cv2.ellipse(mask1, ellipse, (255,255,255),-1)

# apply mask
data[mask1==0] = 0
# data[mask1<1] = 0

# Extract region
x,y,w,h = cv2.boundingRect(c)
region = data[y-10:y+h+10, x-10:x+w+10]

# Export fits
hdu = fits.PrimaryHDU(region)
hdul = fits.HDUList([hdu])
hdul.writeto('/data/image.fits', overwrite=True)