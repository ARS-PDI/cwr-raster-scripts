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
        'ga50': 'ex_coll.tif',
        'grsEx': 'ex_geo_gaps.tif',
        'grsIn': 'in_geo_gaps.tif',
        'thrsld': 'distr.tif'
    }

    for key in img_type_map:
        if key in file:
            raster_name = stdize(file)
            raster_name = raster_name.split(f'_{key}')[0]
            img_type = img_type_map[key]

            return f'{raster_name}_{img_type}'

    return stdize(file).replace('_reclass', '').replace('tif', '.tif')


def process_grs_ex(input_dir, input_raster, output_dir, output_raster):
    reclass_raster = arcpy.sa.Reclassify(os.path.join(
        input_dir, input_raster), 'VALUE', '0 NODATA;1 1', 'DATA')

    reclass_file = f"{output_raster.replace('.tif', '_reclass.tif')}"
    reclass_raster_path = os.path.join(input_dir, reclass_file)
    reclass_raster.save(reclass_raster_path)

    copy2(os.path.join(input_dir, reclass_file),
          os.path.join(output_dir, output_raster))


def reclassify_grs_in(input_dir, input_raster, output_raster):
    input_raster_path = os.path.join(input_dir, input_raster)
    reclass_raster = f"{output_raster.replace('.tif', '_reclass.tif')}"
    output_raster_path = os.path.join(input_dir, reclass_raster)

    base = arcpy.sa.Reclassify(
        input_raster_path, 'VALUE', '1 1;NODATA 0', 'DATA')

    input_basename = os.path.basename(input_dir)
    arcpy.ddd.Minus(os.path.join(
        input_dir, f'{input_basename}__thrsld_median.tif'), base, output_raster_path)

    arcpy.sa.Reclassify(output_raster_path, 'VALUE', '0 NODATA;1 1', 'DATA')

    return reclass_raster


def process_grs_in(input_dir, input_raster, output_dir, output_raster):
    reclass_raster = reclassify_grs_in(input_dir, input_raster, output_raster)
    copy2(os.path.join(input_dir, reclass_raster),
          os.path.join(output_dir, output_raster))


def copy_grs_img(input_dir, input_raster, output_dir, output_raster):
    try:
        if 'grsEx' in input_raster:
            process_grs_ex(input_dir, input_raster, output_dir, output_raster)
        else:
            process_grs_in(input_dir, input_raster, output_dir, output_raster)
    except:
        print('Failed to process', os.path.join(input_dir, input_raster))
        print_exc()


def convert_raster(input_dir, output_dir):
    for input_file in os.listdir(input_dir):
        if input_file.endswith('.tif'):
            output_file = input_file

            if 'ga50' in input_file:
                output_file = f'{os.path.basename(input_dir)}_ga50.tif'

            output_rast = get_output_raster(output_file)

            if 'grs' in input_file:
                copy_grs_img(input_dir, input_file, output_dir, output_rast)
            else:
                copy2(os.path.join(input_dir, input_file),
                      os.path.join(output_dir, output_rast))
        elif os.path.isdir(os.path.join(input_dir, input_file)):
            convert_raster(os.path.join(input_dir, input_file), output_dir)


def print_usage_msg():
    raise ValueError(
        'Usage: python3 convert_rasters.py [input folder] [output folder]')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_usage_msg()

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.isdir(input_dir) or not os.path.isdir(output_dir):
        print_usage_msg()

    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(
        'WGS 1984 UTM Zone 14N')
    arcpy.env.rasterStatistics = 'STATISTICS 1 1'
    arcpy.env.overwriteOutput = True

    print('Copying rasters from', input_dir, 'to', output_dir)

    convert_raster(input_dir, output_dir)
