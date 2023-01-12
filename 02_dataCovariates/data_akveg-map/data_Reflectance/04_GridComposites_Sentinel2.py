# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Create Sentinel-2 composite
# Author: Timm Nawrocki (modified by Jeff Wagner)
# Last Updated: 2021-11-22 (2022-08-03)
# Usage: Must be executed in an ArcGIS Pro Python 3.6 installation.
# Description: "Create Sentinel-2 composite" merges Sentinel-2 tiles by month and property per predefined grid.
# ---------------------------------------------------------------------------

# Import packages
import arcpy
import glob
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import merge_spectral_tiles
arcpy.CheckOutExtension("Spatial")

# Set root directory
drive = 'C:/'
root_folder = 'Users/jeffw/OneDrive/Desktop'

# Define folder structure
data_folder = os.path.join(drive, root_folder, 'GISdata/imagery/sentinel-2')
project_folder = os.path.join(drive, 'Users/jeffw/OneDrive/Documents/Projects/Pika/Pika_distSamp')
grid_folder = os.path.join(drive, root_folder, 'GISdata/analyses/grid_major/studyarea/')
processed_folder = os.path.join(data_folder, 'processed/sa')
output_folder = os.path.join(data_folder, 'gridded')

# Define geodatabases
work_geodatabase = os.path.join(project_folder, 'Pika_distSamp.gdb')

# Define input datasets
nab_raster = os.path.join(project_folder, 'data/AlaskaPika_TotalArea_1.tif')

# Define grids
grid_list = ['A1', 'A2', 'B1', 'B2']

# Define month and property values
months = ['06',
          '07',
          '08',
          '09']
bands = ['evi2',
         'ndvi']

# Create a list of all month-property combinations
metrics_list = []
for month in months:
    for band in bands:
        month_band = month + '_' + band
        metrics_list.append(month_band)
metrics_length = len(metrics_list)

#### CREATE COMPOSITE DATA

# Iterate through each buffered grid and create spectral composite
for metric in metrics_list:
    # Create list of all metric tiles
    file_search = 'Sent2_' + metric + '*.tif'
    metric_tiles = glob.glob(os.path.join(processed_folder, file_search))

    # Set initial count
    count = 1

    # For each grid, process the spectral metric
    for grid in grid_list:
        # Define folder structure
        output_path = os.path.join(output_folder, grid)
        output_raster = os.path.join(output_path, 'Sent2_' + metric + '_' + grid + '.tif')

        # Make grid folder if it does not already exist
        if os.path.exists(output_path) == 0:
            os.mkdir(output_path)

        # Define the grid raster
        grid_raster = os.path.join(grid_folder, grid + '.tif')

        # If output raster does not exist then create output_raster
        if arcpy.Exists(output_raster) == 0:
            # Create key word arguments
            kwargs_merge = {'cell_size': 10,
                            'output_projection': 3338,
                            'work_geodatabase': work_geodatabase,
                            'input_array': [nab_raster, grid_raster] + metric_tiles,
                            'output_array': [output_raster]
                            }

            # Process the merge tiles function
            print(f'Processing {metric} grid {count} of {len(grid_list)}...')
            arcpy_geoprocessing(merge_spectral_tiles, **kwargs_merge)
            print('----------')
        else:
            print(f'Spectral grid {count} of {len(grid_list)} for {metric} already exists.')
            print('----------')

        # Increase counter
        count += 1

