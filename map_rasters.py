import os
import sys
import time

import arcpy


def create_gdb(name):
    arcpy.CreateFileGDB_management(arcpy.env.workspace, name)


def create_mosaics(gdb, mosaics):
    for mosaic in mosaics:
        arcpy.CreateMosaicDataset_management(
            gdb, mosaic, arcpy.SpatialReference('WGS 1984'))


def get_raster_func(file):
    templates_dir = 'templates'
    rast_funcs = {
        'distribution': os.path.join(templates_dir, 'distribution.rft.xml'),
        'ex_coll': os.path.join(templates_dir, 'ex_coll.rft.xml'),
        'ex_geo_gaps': os.path.join(templates_dir, 'ex_geo_gaps.rft.xml'),
        'in_geo_gaps': os.path.join(templates_dir, 'in_geo_gaps.rft.xml')
    }

    for img_type in rast_funcs:
        if img_type in file:
            return rast_funcs[img_type]


def map_rasters(input_dir, fgdb):
    fgdb_path = os.path.join(arcpy.env.workspace, fgdb)

    for file in os.listdir(input_dir):
        input_rast_path = os.path.join(input_dir, file)
        local_time = time.localtime()
        print(time.strftime('[%I:%M:%S]', local_time), input_rast_path)

        mosaic = file.replace('.mrf', '').replace('.tif', '')

        rast_func = get_raster_func(file)

        mosaic_path = os.path.join(fgdb_path, mosaic)
        arcpy.AddRastersToMosaicDataset_management(
            mosaic_path,                                      # Target mosaic dataset
            'Raster Dataset',                                 # Raster type
            input_rast_path                                   # Path to input raster
        )

        rast_func_path = os.path.join(arcpy.env.workspace, rast_func)
        arcpy.SetMosaicDatasetProperties_management(
            mosaic_path,                                      # Target mosaic dataset
            processing_templates=rast_func_path,              # Processing templates
            default_processing_template=rast_func_path        # Default template
        )


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit('Usage: python3 map_rasters.py [root folder]')

    # Set environment variables
    arcpy.env.workspace = os.getcwd()
    arcpy.env.overwriteOutput = True

    fgdb = 'CWR.gdb'
    mosaics = ["Distribution", "Ex situ eco gaps", "In situ eco gaps",
               "Ex situ collections", "Ex situ geo gaps", "In situ geo gaps"]
    create_gdb(fgdb)
    create_mosaics(fgdb, mosaics)

    input_dir = sys.argv[1]

    # Map rasters using custom raster function file and put them into file geodatabase
    map_rasters(input_dir, fgdb)
