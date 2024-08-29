from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS
from astropy import units as u
from astropy.nddata import Cutout2D
import matplotlib.pyplot as plt

import warnings
warnings.simplefilter("ignore")

position = SkyCoord('14h03m38.56s +54d18m41.9s', frame='icrs')
#fits_image_filename = 'JVAR/gSDSS/images/j02-20230816T204329-01_proc.fz'
size = u.Quantity((1, 1), u.arcmin)

def plot_cutout(myImageName, myID):
    hdul = fits.open(myImageName)
    #print(hdul.info())
    image = hdul[1].data
    #print(hdul[1].header['DATE-OBS'])
    wcs = WCS(hdul[1].header)
    cutout = Cutout2D(image, position=position, size=size, wcs=wcs)
    plt.title(hdul[1].header['DATE-OBS'][:10])
    plt.imshow(cutout.data, origin='lower')
    hdul.close()
    outputName = 'cutout_g/tmp' + str(myID).rjust(3,'0') + '.png'
    plt.savefig(outputName)

imageList = open('list_of_images_gSDSS.txt','r')
for index,eachImage in enumerate(imageList):
    if eachImage[0] != '#':
        print(eachImage.strip())
        plot_cutout(eachImage.strip(),index)
imageList.close()

from PIL import Image
import glob

fp_in = "cutout_g/*.png"
fp_out = "gsdss.gif"

# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=500, loop=0)
