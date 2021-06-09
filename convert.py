# import os, sys
import arcpy

# mult_folders  = False # Indicates to use a folder of folders or just a folder
# in_folder    = r'C:\Users\josh.birlingmair\Documents\.USDA\RaBET\...'
# out_folder   = r'C:\Users\josh.birlingmair\Documents\.USDA\RaBET\...'

input_raster  = 'WC_MLRA_65_2008_2011.tif'
output_raster = r'C:\Users\josh.birlingmair\Documents\.USDA\RaBET\output\WC_MLRA_65_2008_2011.mrf'

print('Testing CopyRaster')
arcpy.management.CopyRaster(in_raster=input_raster,
                            out_rasterdataset=output_raster,
                            format='MRF')