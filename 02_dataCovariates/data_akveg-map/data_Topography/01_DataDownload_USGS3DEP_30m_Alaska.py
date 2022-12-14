# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Download USGS 3DEP 30m Alaska Tiles
# Author: Timm Nawrocki (modified by Jeff Wagner)
# Last Updated: 2021-11-22 (2022-07-11)
# Usage: Can be executed in an Anaconda Python 3.7 distribution or an ArcGIS Pro Python 3.6 distribution.
# Description: "Download USGS 3DEP 30m Alaska Tiles" contacts a server to download a series of files specified in a csv table. The full url to the resources must be specified in the table. The table can be generated from The National Map Viewer web application.
# ---------------------------------------------------------------------------

# Import packages
from package_GeospatialProcessing import download_from_csv
import os

# Define base folder structure
drive = 'C:/'
root_folder = 'Users/jeffw/Dropbox/Pika/'

# Define data folder
data_folder = os.path.join(drive, root_folder, 'GISdata/topography/USGS_3DEP_30m/')
directory = os.path.join(data_folder, 'tiles')

# Define input csv table
input_table = os.path.join(data_folder, 'USGS_3DEP_30m_20220711.csv')
url_column = 'url'

# Download files
download_from_csv(input_table, url_column, directory)
