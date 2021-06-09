# Converts GeoTIFF raster datasets in a folder to MRF format
# @author Josh Birlingmair

import os
import arcpy

# Set input and output folders (These can be the same directory)
input_folder          = r'C:\Users\josh.birlingmair\Documents\.USDA\RaBET\Final 81B_rev'
output_folder         = r'C:\Users\josh.birlingmair\Documents\.USDA\RaBET\Output 81B'

arcpy.env.compression = 'LERC 0.000000' # Do not change

for file in os.listdir(input_folder):
    if file.endswith('.tif'):
        input_raster  = file
        output_raster = file.replace('.tif', '.mrf')

        print(f'Converting {input_raster} to {output_raster}')
        arcpy.management.CopyRaster(in_raster=f'{input_folder}\\{input_raster}',
                                    out_rasterdataset=f'{output_folder}\\{output_raster}',
                                    pixel_type='8 bit signed',
                                    format='MRF')
