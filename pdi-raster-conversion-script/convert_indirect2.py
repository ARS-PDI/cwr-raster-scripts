# Converts GeoTIFF raster datasets in an folder of folders
# to MRF format in a specified output folder

import os
import sys
import arcpy

if __name__ == "__main__":
    if len(sys.argv) == 3:
        input_folder  = sys.argv[1]
        output_folder = sys.argv[2]
    else:
        print('Usage: python3 convert_indirect2.py "C:/Users/.../Input Folder" "C:/Users/.../Output Folder"')
        exit(1)

    arcpy.env.compression            = 'LERC 0'
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference('WGS 1984 UTM Zone 14N')
    arcpy.env.rasterStatistics       = 'STATISTICS 1 1'

    failed = []

    for folder in os.listdir(input_folder):
        try:
            os.mkdir(f'{output_folder}/{folder}')
        except FileExistsError:
            pass

        for subfolder in os.listdir(f'{input_folder}/{folder}'):
            try:
                os.mkdir(f'{output_folder}/{folder}/{subfolder}')
            except FileExistsError:
                pass

            for file in os.listdir(f'{input_folder}/{folder}/{subfolder}'):
                if file.endswith('.tif'):
                    input_raster  = file
                    output_raster = file.replace('.tif', '.mrf')

                    print(f'Converting {folder}/{subfolder}/{input_raster}')
                    try:
                        arcpy.management.CopyRaster(in_raster         = f'{input_folder}/{folder}/{subfolder}/{input_raster}',
                                                    out_rasterdataset = f'{output_folder}/{folder}/{subfolder}/{output_raster}',
                                                    background_value  = 0,
                                                    nodata_value      = 127,
                                                    format            = 'MRF',
                                                    transform         = 'NONE')
                    except:
                        print(f'Failed to convert {input_raster}. Skipping raster')
                        failed.append(f'{folder}/{subfolder}/{input_raster}')
                        continue

    print('The following rasters could not be converted:')
    for raster in failed:
        print(f'\t', raster)

    print('Finished converting')
