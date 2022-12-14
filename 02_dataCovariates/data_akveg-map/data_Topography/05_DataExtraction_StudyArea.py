# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Extract predictor data to study area
# Author: Timm Nawrocki (modified by Jeff Wagner)
# Last Updated: 2021-11-20 (2022-07-19)
# Usage: Must be executed in an ArcGIS Pro Python 3.6 installation.
# Description: "Extract predictor data to study area" extracts a set of topographic predictor raster datasets to a study area to enforce the same extent on all rasters.
# ---------------------------------------------------------------------------

# Import packages
import arcpy
import os
from package_GeospatialProcessing import arcpy_geoprocessing
from package_GeospatialProcessing import extract_to_study_area

# Set root directory
drive = 'C:/'
root_folder = 'Users/jeffw/Dropbox/Pika/'

# Define folder structure
data_folder = os.path.join(drive, root_folder, 'GISdata/topography/Composite_10m')
project_folder = os.path.join(drive, 'Users/jeffw/OneDrive/Documents/Projects/Pika/Pika_distSamp')
grid_folder = os.path.join(drive, root_folder, 'GISdata/analyses/grid_major/studyarea/')
input_folder = os.path.join(data_folder, 'full/integer')
output_folder = os.path.join(data_folder, 'studyarea')

# Define work geodatabase
work_geodatabase = os.path.join(project_folder, 'Pika_distSamp.gdb')

# Define input datasets
area_raster = os.path.join(project_folder, 'data/AlaskaPika_TotalArea_1.tif')

# Define grids
grid_list = ['A1', 'A2', 'B1', 'B2']

#### EXTRACT DATA TO GRIDS

# Iterate through each buffered grid and create output rasters
for grid in grid_list:
    # Define folder structure
    output_path = os.path.join(output_folder, grid)

    # Make grid folder if it does not already exist
    if os.path.exists(output_path) == 0:
        os.mkdir(output_path)

    # Define the grid raster
    grid_raster = os.path.join(grid_folder, grid + '.tif')

    # Generate a list of input rasters
    raster_list = []
    arcpy.env.workspace = os.path.join(input_folder, grid)
    rasters = arcpy.ListRasters('', 'TIF')
    for raster in rasters:
        raster_list.append(os.path.join(arcpy.env.workspace, raster))

    # Set arcpy.env.workspace
    arcpy.env.workspace = work_geodatabase

    # Define raster list count
    total = len(raster_list)

    # Iterate through rasters and extract raster
    for input_raster in raster_list:
        # Identify raster index
        count = raster_list.index(input_raster) + 1

        # Define output raster
        output_raster = os.path.join(output_path, os.path.split(input_raster)[1])

        # If output raster does not exist then create output raster
        if arcpy.Exists(output_raster) == 0:
            # Create key word arguments
            kwargs_extract = {'work_geodatabase': work_geodatabase,
                              'input_array': [input_raster, area_raster, grid_raster],
                              'output_array': [output_raster]
                              }

            # Extract raster to study area
            print(f'\tExtracting raster {count} of {total} for Grid {grid}...')
            arcpy_geoprocessing(extract_to_study_area, **kwargs_extract)
            print('\t----------')
        else:
            print(f'\tRaster {count} of {total} for Grid {grid} already exists.')
            print('\t----------')
