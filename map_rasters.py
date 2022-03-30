import os
import sys
import time

import arcpy


def stdize(s):
    return s.replace('__', '_').replace(' ', '_').replace('-', '_').replace('.', '').replace('(', '').replace(')', '')


def create_gdb(name):
    arcpy.CreateFileGDB_management(arcpy.env.workspace, name)


def create_mosaics(gdb, mosaics):
    for mosaic in mosaics:
        arcpy.CreateMosaicDataset_management(
            gdb, mosaic, arcpy.SpatialReference('WGS 1984'))


def map_rasters(input_dir, workspace, rast_funcs, fgdb):
    fgdb_path = os.path.join(workspace, 'GDB', fgdb)

    for file in os.listdir(input_dir):
        input_rast_path = os.path.join(input_dir, file)
        local_time = time.localtime()
        print(time.strftime('[%I:%M:%S]', local_time), input_rast_path)

        mosaic = file.replace('.mrf', '')
        mosaic = stdize(mosaic)

        rast_func = None
        if 'ga50' in file:
            rast_func = rast_funcs['ga50']
        elif 'grsEx' in file:
            rast_func = rast_funcs['grsEx']
        elif 'grsIn_proAreas' in file:
            rast_func = rast_funcs['grsIn_proAreas']
        elif 'thrsld_median' in file:
            rast_func = rast_funcs['thrsld_median']

        mosaic_path = os.path.join(fgdb_path, mosaic)
        arcpy.AddRastersToMosaicDataset_management(
            mosaic_path,                                      # Target mosaic dataset
            'Raster Dataset',                                 # Raster type
            input_rast_path                                   # Path to input raster
        )

        rast_func_path = os.path.join(workspace, rast_func)
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

    root_dir = sys.argv[1]
    templates_dir = 'templates'
    rast_funcs = {
        'ga50': os.path.join(templates_dir, 'ga50.rft.xml'),
        'grsEx': os.path.join(templates_dir, 'grsEx.rft.xml'),
        'grsIn_proAreas': os.path.join(templates_dir, 'grsIn_proAreas.rft.xml'),
        'thrsld_median': os.path.join(templates_dir, 'thrsld_median.rft.xml'),
    }

    # Map rasters using custom raster function file and put them into file geodatabase
    map_rasters(root_dir, arcpy.env.workspace, rast_funcs, 'default.gdb')
