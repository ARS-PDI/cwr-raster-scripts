# Converts GeoTIFF raster datasets in an folder to MRF format to an output
# @author Josh Birlingmair

import os
import sys
import arcpy

if len(sys.argv) == 3:
    input_folder  = sys.argv[1]
    output_folder = sys.argv[2]
else:
    print('Usage: python3 convert.py "C:/Users/.../Input Folder" "C:/Users/.../Output Folder"')
    exit(1)

arcpy.env.compression            = 'LERC 0'
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference('WGS 1984 UTM Zone 14N')
arcpy.env.rasterStatistics       = 'STATISTICS 1 1'

if __name__ == "__main__":
    for file in os.listdir(input_folder):
        if file.endswith('.tif'):
            input_raster  = file
            output_raster = file.replace('.tif', '.mrf')

            print(f'Converting {input_raster} to {output_raster}')
            arcpy.management.CopyRaster(in_raster         = f'{input_folder}/{input_raster}',
                                        out_rasterdataset = f'{output_folder}/{output_raster}',
                                        background_value  = 0,
                                        nodata_value      = 127,
                                        format            = 'MRF',
                                        transform         = 'NONE')
