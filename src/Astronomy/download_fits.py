# coding: utf-8
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
from astropy.utils.data import download_file, download_files_in_parallel
from astropy.io import fits

def coordinateToUrl(r, x):
    return f"https://archive.stsci.edu/cgi-bin/dss_search?v=3&r={r}&d={x}+0&h=10&w=10&f=fits"  

def download_on_fits(url, location):
    image_file = download_file(url, cache=True, pkgname=location)
    return image_file

def download_several_fits(urls, location):
    image_file = download_files_in_parallel(urls, cache=True, pkgname=location)
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
        urls = []
        while(r < 360):
            # Récupérer l'image
            url = coordinateToUrl(r, x)
            print(url)
            urls.append(url)
            # all_sky_fits.append(download_fits(url, "sky"))
            '''
            drap += 1
            if(drap > 5):
                break
            '''
            drap += 1

            # Incrémentation
            r += step
        t = download_files_in_parallel(urls, cache=True)
        print(t)
        all_sky_fits += t
    return all_sky_fits

def get_supernovae_fits(path_url_txt):
    f = open(path_url_txt, "r")
    urls = []
    for url in f:
        urls.append(url)
    all_supernovae_fits = download_several_fits(f, "supernovae")
    return all_supernovae_fits


if __name__ == "__main__":
    # all_sky_fits = get_sky_fits()
    x = np.arange(0., 90., 0.2)
    plt.plot(x, 11.5/(90-np.abs(x)), 'b--')
    plt.plot([0, 45, 70, 80, 85, 89], [0.2, 0.282, 0.585, 1.2, 2.3, 11.5], 'ro')
    
    plt.show()

    all_supernovae_fits = get_supernovae_fits("supernovae_url.txt")

    # test()
