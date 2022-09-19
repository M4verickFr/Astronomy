# coding: utf-8

import sqlite3
import matplotlib.pyplot as plt
from astropy.utils.data import download_file
from astropy.io import fits

def coordinateToUrl():
    return None  

def getImages(path):
    image_file = download_file('http://data.astropy.org/tutorials/FITS-images/HorseHead.fits', cache=True )
    return image_file

def displayImage(image_file):
    image_data = fits.getdata(image_file)
    plt.imshow(image_data, cmap='gray')
    plt.colorbar()

if __name__ == "__main__":
    url = "https://archive.stsci.edu/cgi-bin/dss_search\?v\=3\&r\=13+39+53.2\&d\=-31+40+15.0\&h\=10.0\&w\=10.0\&f\=fits"
    image_file = getImages("url")
    displayImage(image_file)