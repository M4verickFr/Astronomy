# coding: utf-8
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
from astropy.utils.data import download_file, download_files_in_parallel
from astropy.io import fits

def coordinateToUrl(r, x):
    return f"https://archive.stsci.edu/cgi-bin/dss_search?v=3&r={r}&d={x}+0&h=10&w=10&f=fits"  

def download_one_fits(url, location):
    image_file = download_file(url, cache=True, pkgname=location)
    return image_file

def download_several_fits(urls, location):
    image_file = download_files_in_parallel(urls, cache=True, pkgname=location)
    return image_file

def displayImage(image_file):
    image_data = fits.getdata(image_file)
    plt.imshow(image_data, cmap='gray')
    plt.colorbar()

def get_supernovae_fits(path_url_txt):
    f = open(path_url_txt, "r")
    urls = []
    for url in f:
        urls.append(url)
    all_supernovae_fits = download_several_fits(f, "supernovae")
    return all_supernovae_fits


if __name__ == "__main__":
    all_supernovae_fits = get_supernovae_fits("supernovae_url.txt")