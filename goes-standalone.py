import numpy as np
import matplotlib
matplotlib.use('agg')  # Set the backend for matplotlib plotting
import matplotlib.pyplot as plt
import os
import glob
from google.cloud import storage
import sys
import argparse
from netCDF4 import Dataset  # Used to read the GOES .nc files

def mk_argparser():
    """Sets up the argument parser"""
    parser = argparse.ArgumentParser(description="Pull GOES images from GCP \
                                     bucket")
    parser.add_argument('input', nargs='?', 
                        type=argparse.FileType('r'), 
                        default=sys.stdin)
    parser.add_argument('--band', '-b',
                        default='13',
                        type=str,
                        help='Spectral band for which to pull imagery, \
                            integer from 1 thru 16')
    parser.add_argument('--goes_folder', '-g', 
                        default='./', 
                        type=str, 
                        help='Path into which to store retrieved GOES images, \
                            of form /filepath/')
    parser.add_argument('--goes_image_time', '-t', 
                        default='2020-146-00',
                        type=str, 
                        help='Starting time for GOES-image. Format: \
                            2020-146-00 (YYYY-DDD-HH)')
    return parser


def download_blobs(bucket_name, prefix, filepath):
    '''
    Downloads blobs from the specified GCP bucket

    Parameters
    ----------
    bucket_name : string
        Name of the GCP bucket from which data is downloaded.
    prefix : string
        Blob prefix containing the date/time and frequency band.
    filepath : string
        Where to download the blobs.

    Returns
    -------
    None.

    '''
    storage_client = storage.Client.create_anonymous_client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix, delimiter=None)

    for blob in blobs:
        temp = blob.name
        newstr = temp.rsplit('/', 1)
        filename = newstr[1]
        filespec = filepath + filename
        if os.path.exists(filespec) == False:
            with open(filespec, "wb") as file_obj:
                blob.download_to_file(file_obj) 
                print("Downloaded ", filespec)
    return


def plot_img(ncfilename, outfile):
    '''
    Generates a .jpg file of the radiance values from the *.nc blob file 

    Parameters
    ----------
    ncfilename : string
        The blob containing the radiance values to be plotted.
    outfile : string
        Filename of the .jpg file to be created.

    Returns
    -------
    None.

    '''
    
    with Dataset(ncfilename, 'r') as nc:
       rad = nc.variables['Rad'][:]
       ref = (rad * np.pi * 0.3) / 663.274497
       ref = np.minimum( np.maximum(ref, 0.0), 1.0 )
       # crop to area of interest
       
       # do gamma correction to stretch the values
       ref = np.sqrt(ref)
       # plotting to jpg file
       plt.imsave(outfile, ref, vmin=0.0, vmax=1.0, cmap='gist_ncar_r') # or 'Greys_r' without color
       plt.close('all')
       return


parser = mk_argparser()
args = parser.parse_args()
filepath = args.goes_folder

bucket_name = 'gcp-public-data-goes-16'
band = args.band

# Parse the date string into year, Julian day, hour
syear = args.goes_image_time[0:4]  # "2020"
sday = args.goes_image_time[5:8]  # "236"
shour = args.goes_image_time[9:11]  #"08"

print(sday, shour, band)

# Download the blobs matching this date & time
datestring = 'ABI-L1b-RadF/' + syear + '/' + sday + '/' + shour + '/'
object_name = datestring + 'OR_ABI-L1b-RadF-M6C' + band
download_blobs(bucket_name, object_name, filepath)

# Generate plots from the blobs
for file in glob.glob(os.path.join(filepath,'*.nc')):  # 'glob' fetches each filename
    plotfile = file.rsplit('.',0)[0] # Supposed to split the extension off the filename, but doesn't work
    plotfile = plotfile + '.jpg'
    print('Plotting ', plotfile)
    plot_img(file,plotfile)
