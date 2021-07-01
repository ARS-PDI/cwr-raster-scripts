# Converts all GeoTIFF raster datasets existing in a root directory to MRFs

import os
import sys
import arcpy

def convert_raster(input_dir, output_dir, nodata_val, pixel_t):
    """
    Recursive function that converts all raster datasets under an input directory
    into an output folder
    """
    for file in os.listdir(input_dir):
        if file.endswith('.tif'):
            output_rast = file.replace('.tif', '.mrf')

            print(f'Converting {input_dir}/{file}')
            try:
                arcpy.CopyRaster_management(in_raster         = f'{input_dir}/{file}',
                                            out_rasterdataset = f'{output_dir}/{output_rast}',
                                            background_value  = nodata_val,
                                            nodata_value      = nodata_val,
                                            pixel_type        = pixel_t,
                                            format            = 'MRF',
                                            transform         = 'NONE')
            except KeyboardInterrupt:
                exit()
            except:
                pass
        elif os.path.isdir(f'{input_dir}/{file}'):
            try:
                os.mkdir(f'{output_dir}/{file}')
            except FileExistsError:
                pass

            convert_raster(f'{input_dir}/{file}', f'{output_dir}/{file}', nodata_val, pixel_t)

def checkup(input_dir, output_dir, no_match):
    """
    Double checks that for every TIF there is a corresponding MRF in all the root
    directory's subdirectories
    """
    for file in os.listdir(input_dir):
        if file.endswith('.tif'):
            if file.replace('.tif', '.mrf.aux.xml') not in os.listdir(output_dir):
                no_match.append(f'{input_dir}/{file}')
        elif os.path.isdir(f'{input_dir}/{file}'):
            checkup(f'{input_dir}/{file}', f'{output_dir}/{file}', no_match)

def cleanup(input_dir):
    """
    Cleans up unnecessary metadata XML files generated by arcpy.CopyRaster function
    Runs from the root directory
    """
    for file in os.listdir(input_dir):
        if file.endswith('.mrf.xml'):
            os.remove(f'{input_dir}/{file}')
        elif os.path.isdir(f'{input_dir}/{file}'):
            cleanup(f'{input_dir}/{file}')

def raise_os_error():
    raise OSError('Usage: python3 convert_rasters.py [input folder] [output folder]')
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise_os_error()

    input_dir  = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.isdir(input_dir) or not os.path.isdir(output_dir):
        raise_os_error()
    
    arcpy.env.compression            = 'LERC 0'
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference('WGS 1984 UTM Zone 14N')
    arcpy.env.rasterStatistics       = 'STATISTICS 1 1'

    pixel_t = '32_BIT_SIGNED'
    nodata_val = -2147483648     # 32-bit signed minimum
    
    convert_raster(input_dir, output_dir, nodata_val, pixel_t)
    print('Finished converting')

    no_match = []
    checkup(input_dir, output_dir, no_match)

    if no_match:
        print('The following rasters do not have no match:')
        for raster in no_match:
            print(raster)
    else:
        print('All TIFs have a matching MRF')

    cleanup(output_dir)
    print('Finished cleaning up metadata files')
