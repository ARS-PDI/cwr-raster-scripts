# import os, sys
import arcpy

# Set input and output folders
in_folder      = r'C:\Users\josh.birlingmair\Documents\.USDA\ARS-PDI\pdi-raster-conversion-script'
out_folder     = r'C:\Users\josh.birlingmair\Documents\.USDA\RaBET\output'

input_raster   = 'WC_MLRA_65_2008_2011.tif'
output_raster  = 'WC_MLRA_65_2008_2011.mrf'

# Do not change
input_dataset  = f'{in_folder}\\{input_raster}'
output_dataset = f'{out_folder}\\{output_raster}'

print(f'Testing conversion of {input_raster} to {output_raster}')
arcpy.management.CopyRaster(in_raster=input_dataset,
                            out_rasterdataset=output_dataset,
                            pixel_type='8 bit signed',
                            format='MRF')
print('Finished converting', input_raster)