# goes-standalone
This is a brief example of how to extract [NOAA GOES-16 satellite](https://www.nesdis.noaa.gov/GOES-R-Series-Satellites) dumps from the [GOES-16 Dataset](console.cloud.google.com/marketplace/product/noaa-public/goes-16) hosted in Google BigQuery.

# Setup
Assuming you have Python 3.7 or later installed, set up an environment, having installed the following modules with pip:
* numpy
* matplotlib
* glob
* google-cloud-storage
* netCDF4

# Running goes-standalone
goes-standalone features an argument parser where the user may specify:
* the spectral imaging band
* the folder in which to store the downloaded blobs and images
* the date/time for which to extract images, in Julian format, `YYYY-DDD-HH`, where `DDD` represents the day of the year.

For a brief explanation of the arguments, type `python goes-standalone --help`. I've coded default arguments, so that one can simply type `python goes-standalone` to produce sample results. It would be trivial to modify the code so that the default datetime is for the most recent imagery.

Code for post-processing the blobs into .jpg files was borrowed from [How to process weather satellite data in real-time in BigQuery](https://cloud.google.com/blog/products/gcp/how-to-process-weather-satellite-data-in-real-time-in-bigquery), credit to [Lak Lakshmanan](https://www.linkedin.com/in/valliappalakshmanan/).
