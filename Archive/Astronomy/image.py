# coding: utf-8
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
from astropy.utils.data import download_file
from astropy.io import fits

def coordinateToUrl(r, x):
    return f"https://archive.stsci.edu/cgi-bin/dss_search?v=3&r={r}&d={x}&h=12&w=12&f=fits"  

def getImages(path):
    image_file = download_file('http://data.astropy.org/tutorials/FITS-images/HorseHead.fits', cache=True )
    return image_file

def displayImage(image_file):
    image_data = fits.getdata(image_file)
    plt.imshow(image_data, cmap='gray')
    plt.colorbar()

if __name__ == "__main__":
    all_images = []
    for i in range(-900, 900, 2):
        r = 0.01
        x= i/10
        step = 0.2 + 5.478128918342 * (10**-36) * np.exp(0.938859*np.abs(x))
        if 77.5<np.abs(x)<87.5:
            step+=(0.2*np.abs(x)-15.5)
        drap=0
        while(r < 360):
            # Récupérer l'image
            url = coordinateToUrl(r, x)
            print(url)
            all_images.append(getImages(url))
            '''
            drap += 1
            if(drap > 5):
                break
            '''

            # Incrémentation
            r += step
    
    fig = plt.figure(figsize = (16,16))

    for i in range(len(all_images)):
        plt.subplot(3,2,i+1)
        displayImage(all_images[i])
    plt.show()
