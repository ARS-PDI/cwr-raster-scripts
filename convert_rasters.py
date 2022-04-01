# Converts all GeoTIFF raster datasets existing in a root directory to MRFs

import os
import sys
from shutil import copy2
from traceback import print_exc

import arcpy


def stdize(s):
    return s.replace('__', '_').replace(' ', '_').replace('-', '_').replace('.', '').replace('(', '').replace(')', '')


def get_output_raster(file):
    img_type_map = {
        'ersEx_ecos': 'ex_eco_gaps.tif',
        'ersIn_ecos': 'in_eco_gaps.tif',
        'ga50': 'ex_coll.mrf',
        'grsEx': 'ex_geo_gaps.mrf',
        'grsIn': 'in_geo_gaps.mrf',
        'thrsld': 'distr.mrf'
    }

    for key in img_type_map:
        if key in file:
            raster_name = stdize(file)
            raster_name = raster_name.split(f'_{key}')[0]
            img_type = img_type_map[key]

            return f'{raster_name}_{img_type}'

    raise RuntimeError(f'Unknown image type: {file}')


def convert_raster(input_dir, output_dir):
    """
    Recursive function that converts all raster datasets under an input directory
    into an output folder
    """
    pixel_t = '8_BIT_UNSIGNED'
    nodata_val = 255  # max unsigned 8-bit val

    for file in os.listdir(input_dir):
        if file.endswith('.tif'):
            filename = file

            if 'ga50' in file:
                filename = f'{os.path.basename(input_dir)}_ga50.mrf'

            output_rast = get_output_raster(filename)

            if output_rast.endswith('.tif'):
                copy2(os.path.join(input_dir, file),
                      os.path.join(output_dir, output_rast))
                continue

            try:
                arcpy.CopyRaster_management(
                    in_raster=os.path.join(input_dir, file),
                    out_rasterdataset=os.path.join(output_dir, output_rast),
                    background_value=nodata_val,
                    nodata_value=nodata_val,
                    pixel_type=pixel_t,
                    format='MRF',
                    transform='NONE')
            except arcpy.ExecuteError:
                print('Failed to convert', os.path.join(input_dir, file))
                print_exc()
        elif os.path.isdir(os.path.join(input_dir, file)):
            convert_raster(os.path.join(input_dir, file), output_dir)


def raise_os_error():
    raise OSError(
        'Usage: python3 convert_rasters.py [input folder] [output folder]')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise_os_error()

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.isdir(input_dir) or not os.path.isdir(output_dir):
        raise_os_error()

    arcpy.env.compression = 'LERC 0'
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(
        'WGS 1984 UTM Zone 14N')
    arcpy.env.rasterStatistics = 'STATISTICS 1 1'
    arcpy.env.overwriteOutput = False

    convert_raster(input_dir, output_dir)
    print('Finished converting')
