# coding: utf-8
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
from astropy.utils.data import download_file
from astropy.io import fits

def coordinateToUrl(r, x):
    return f"https://archive.stsci.edu/cgi-bin/dss_search?v=3&r={r}&d={x}+0&h=12&w=12&f=fits"  

def getImages(path):
    image_file = download_file(path, cache=True)
    print(image_file)
    return image_file

def displayImage(image_file):
    image_data = fits.getdata(image_file)
    plt.imshow(image_data, cmap='gray')
    plt.colorbar()

def astro():
    all_images = []
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
            all_images.append(getImages(url))
            '''
            drap += 1
            if(drap > 5):
                break
            '''
            drap += 1

            # Incrémentation
            r += step

    print(drap)
    '''
    fig = plt.figure(figsize = (16,16))

    for i in range(len(all_images)):
        plt.subplot(3,2,i+1)
        displayImage(all_images[i])
    plt.show()
    '''


def test():
    from matplotlib.cm import get_cmap
    import numpy as np

    import pyvista as pv
    from pyvista import examples

    sphere = pv.Sphere(
        radius=5, theta_resolution=179, phi_resolution=179, start_theta=270.001, end_theta=270
    )

    ellipsoid = pv.ParametricEllipsoid(xradius = 10, yradius=10, zradius = 10)

    # Initialize the texture coordinates array
    ellipsoid.active_t_coords = np.zeros((ellipsoid.points.shape[0], 2))



    # Populate by manually calculating
    

    # And let's display it with a world map
    tex = examples.load_globe_texture()
    ellipsoid.plot(texture=tex)

if __name__ == "__main__":
    astro()
    x = np.arange(0., 90., 0.2)
    plt.plot(x, 11.5/(90-np.abs(x)), 'b--')
    plt.plot([0, 45, 70, 80, 85, 89], [0.2, 0.282, 0.585, 1.2, 2.3, 11.5], 'ro')
    
    plt.show()

    drap = 0
    r = 0.01
    x= 0
    step = 11.5/(90-np.abs(x))
        
    while(r < 360):
        # Récupérer l'image
        url = coordinateToUrl(r, x)
        print(url)
        # all_images.append(getImages(url))
        '''
        drap += 1
        if(drap > 5):
            break
        '''
        drap += 1
        if(r > 3):
            break
        # Incrémentation
        r += step

    print(drap)

    # test()
