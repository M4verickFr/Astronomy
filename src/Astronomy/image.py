# coding: utf-8
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
from astropy.utils.data import download_file
from astropy.io import fits

def coordinateToUrl(r, x):

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
    for i in range(-900, 900, 2):
        r = 0
        x= i/10
        step = 0.2 + 5.478128918342 * (10**-36) * np.exp(0.938859*np.abs(x))
        if 77.5<x<87.5:
            step+=(0.2*x-15.5)

        while(r < 360):
            # Récupérer l'image
            coordinateToUrl(r, i)
            image_file = getImages("url")

            # Incrémentation
            r += step
    
    
    
    displayImage(image_file)