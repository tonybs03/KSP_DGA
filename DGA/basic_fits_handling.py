#################################################################
# Name:     basic_fits_handling.py                              #
# Author:   TJJ Fan                                             #
# Version:  Oct, 3, 2024                                        #
# Function: Program contains various routines for calculating   #
#           cosmological quantities. Also contains constants.   #
#################################################################

#essential modules
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy import units as u
from astropy.nddata import Cutout2D
import matplotlib.pyplot as plt

#function: load and display the fits image showing a targeted DGC
#string, string, tuple
def display_DGC(fitsfile, coordinates, size, skyCoords = True, vmin=-15, vmax=5):
    # Open FITS file once and extract data and header
    with fits.open(fitsfile, memmap=True) as hdu:
        data = hdu[0].data
        header = hdu[0].header

    # Create WCS using the header (more efficient than reopening the file)
    w = WCS(header)
    
    # Define size and position
    size = u.Quantity(size, u.arcmin)

    # Determine the position for the cutout
    if skyCoords:
        from astropy.coordinates import SkyCoord
        position = SkyCoord(coordinates, frame='icrs')
    else:
        position = coordinates

    # Create the cutout object
    cutout = Cutout2D(data, position, size, wcs=w)
    
    # Calculate center for crosshairs using integer division
    centre = cutout.data.shape[0] // 2
    if cutout.data.shape[0] % 2 == 0:  # Check if the image size is even
        centre += 0.5

    # Plotting the cutout (negate only for display)
    plt.figure(figsize=(8, 8))
    plt.imshow(-1 * cutout.data, cmap='gray', vmin=vmin, vmax=vmax, origin='lower')
    plt.axvline(x=centre, linewidth=0.5, color='#1f77b4')
    plt.axhline(y=centre, linewidth=0.5)
    plt.show()





    