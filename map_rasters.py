import os
import sys
import time

import arcpy

mosaics = {
    'distribution': 'distr',
    'ex_situ_eco_gaps': 'ex_eco_gaps',
    'in_situ_eco_gaps': 'in_eco_gaps',
    'ex_situ_collections': 'ex_coll',
    'ex_situ_geo_gaps': 'ex_geo_gaps',
    'in_situ_geo_gaps': 'in_geo_gaps'
}


def create_gdb(name):
    arcpy.CreateFileGDB_management(arcpy.env.workspace, name)


def create_mosaics(gdb):
    global mosaics

    for mosaic in mosaics:
        arcpy.CreateMosaicDataset_management(
            gdb, mosaic, arcpy.SpatialReference('WGS 1984'))


def get_raster_func(file):
    templates_dir = 'templates'
    rast_funcs = {
        'distr': os.path.join(templates_dir, 'distr.rft.xml'),
        'ex_coll': os.path.join(templates_dir, 'ex_coll.rft.xml'),
        'ex_geo_gaps': os.path.join(templates_dir, 'ex_geo_gaps.rft.xml'),
        'in_geo_gaps': os.path.join(templates_dir, 'in_geo_gaps.rft.xml')
    }

    for img_type in rast_funcs:
        if img_type in file:
            return rast_funcs[img_type]


def add_rasters_to_mosaics(input_dir, fgdb):
    global mosaics

    rasters = os.listdir(input_dir)

    for img_type in mosaics:
        mosaic_rasts = [r for r in rasters if img_type in r]
        mosaic_path = os.path.join(fgdb, mosaics[img_type])

        arcpy.AddRastersToMosaicDataset_management(
            mosaic_path,
            'Raster Dataset',
            [os.path.join(input_dir, r) for r in mosaic_rasts]
        )


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
    create_gdb(fgdb)
    create_mosaics(fgdb)

    input_dir = sys.argv[1]

    add_rasters_to_mosaics(input_dir, fgdb)

    # Map rasters using custom raster function file and put them into file geodatabase
    map_rasters(input_dir, fgdb)
