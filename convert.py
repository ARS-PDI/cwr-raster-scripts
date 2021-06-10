# Converts GeoTIFF raster datasets in an folder to MRF format to an output
# @author Josh Birlingmair

import os
import arcpy

# Set input and output folders (These can be the same directory)
input_folder  = r'C:\Users\josh.birlingmair\Documents\.USDA\RaBET\Final 81B_rev'
output_folder = r'C:\Users\josh.birlingmair\Documents\.USDA\RaBET\Output 81B'

# Do not change
arcpy.env.compression            = 'LERC 0'
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference('WGS 1984 UTM Zone 14N')
arcpy.env.rasterStatistics       = 'STATISTICS 1 1'

if __name__ == "__main__":
    for file in os.listdir(input_folder):
        if file.endswith('.tif'):
            input_raster  = file
            output_raster = file.replace('.tif', '.mrf')

            print(f'Converting {input_raster} to {output_raster}')
            arcpy.management.CopyRaster(in_raster         = f'{input_folder}\\{input_raster}',
                                        out_rasterdataset = f'{output_folder}\\{output_raster}',
                                        background_value  = 0,
                                        nodata_value      = 127,
                                        pixel_type        = '8_BIT_SIGNED',
                                        format            = 'MRF',
                                        transform         = 'NONE')

        # Clean up unneeded XML files
        for file in os.listdir(output_folder):
            if file.endswith('mrf.aux.xml') or file.endswith('.mrf.xml'):
                os.remove(f'{output_folder}\\{file}')
