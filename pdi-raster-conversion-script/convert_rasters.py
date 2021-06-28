# Converts all GeoTIFF raster datasets existing in a root directory to MRFs

import os
import sys
import arcpy

# Recursive function that converts all
def convert_raster(input_dir, output_dir):
    for file in os.listdir(input_dir):
        if file.endswith('.tif'):
            output_rast = file.replace('.tif', '.mrf')

            print(f'Converting {input_dir}/{file}')
            try:
                arcpy.CopyRaster_management(in_raster         = f'{input_dir}/{file}',
                                            out_rasterdataset = f'{output_dir}/{output_rast}',
                                            background_value  = 0,
                                            nodata_value      = 127,
                                            format            = 'MRF',
                                            transform         = 'NONE')
            except KeyboardInterrupt:
                exit()
            except:
                print('Failed to convert raster. Skipping')
                continue
        elif os.path.isdir(f'{input_dir}/{file}'):
            os.mkdir(f'{output_dir}/{file}')
            convert_raster(f'{input_dir}/{file}', f'{output_dir}/{file}')
    
if __name__ == "__main__":
    if len(sys.argv) == 3:
        input_dir  = sys.argv[1]
        output_dir = sys.argv[2]
    else:
        print('Usage: python3 convert_rasters.py [input folder] [output folder]')
        exit()

    arcpy.env.compression            = 'LERC 0'
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference('WGS 1984 UTM Zone 14N')
    arcpy.env.rasterStatistics       = 'STATISTICS 1 1'

    convert_raster(input_dir, output_dir)
    print('Finished converting')
