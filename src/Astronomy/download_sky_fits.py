# coding: utf-8
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
from astropy.utils.data import download_file
from astropy.io import fits

def coordinateToUrl(r, x):
    return f"https://archive.stsci.edu/cgi-bin/dss_search?v=3&r={r}&d={x}+0&h=12&w=12&f=fits"  

def download_fits(url):
    image_file = download_file(url, cache=True)
    return image_file

def displayImage(image_file):
    image_data = fits.getdata(image_file)
    plt.imshow(image_data, cmap='gray')
    plt.colorbar()

def get_sky_fits():
    all_sky_fits = []
    drap=0
    for i in range(-900, 900, 2):
        print(f"********************** angle {i} **********************")
        r = 0.01
        x= i/10
        step = 11.5/(90-np.abs(x))
        
        while(r < 360):
            # Récupérer l'image
            url = coordinateToUrl(r, x)
            print(url)
            all_sky_fits.append(download_fits(url))
            '''
            drap += 1
            if(drap > 5):
                break
            '''
            drap += 1

            # Incrémentation
            r += step
    return all_sky_fits

def get_supernovae_fits(path_url_txt):
    f = open(path_url_txt, "r")
    all_supernovae_fits = []
    for url in f:
        print(url)
        all_supernovae_fits.append(download_fits(url))
    return all_supernovae_fits


if __name__ == "__main__":
    all_sky_fits = get_sky_fits()
    x = np.arange(0., 90., 0.2)
    plt.plot(x, 11.5/(90-np.abs(x)), 'b--')
    plt.plot([0, 45, 70, 80, 85, 89], [0.2, 0.282, 0.585, 1.2, 2.3, 11.5], 'ro')
    
    plt.show()

    all_supernovae_fits = get_supernovae_fits()

    # test()
