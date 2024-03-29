import os
import sys

import arcpy

mosaics = {
    'distribution': 'distr',
    'ex_situ_eco_gaps': 'ex_eco_gaps',
    'in_situ_eco_gaps': 'in_eco_gaps',
    'ex_situ_collections': 'ex_coll',
    'ex_situ_geo_gaps': 'ex_geo_gaps',
    'in_situ_geo_gaps': 'in_geo_gaps'
}


def create_gdb(fgdb_dir, name):
    print('Creating file geodatabase:', name)

    arcpy.CreateFileGDB_management(fgdb_dir, name)


def create_mosaic(fgdb_dir, gdb, mosaic, img_type):
    if 'eco_gaps' in img_type:
        arcpy.CreateMosaicDataset_management(
            os.path.join(fgdb_dir, gdb), mosaic, arcpy.SpatialReference('WGS 1984'))
    else:
        arcpy.CreateMosaicDataset_management(
            os.path.join(fgdb_dir, gdb), mosaic, arcpy.SpatialReference('WGS 1984'), pixel_type='8_BIT_UNSIGNED')


def add_rasters_to_mosaics(input_dir, fgdb_dir, fgdb):
    global mosaics

    old_workspace = arcpy.env.workspace
    arcpy.env.workspace = input_dir
    rasters = arcpy.ListRasters('*')
    arcpy.env.workspace = old_workspace

    for mosaic in mosaics:
        print('Creating mosaic dataset:', mosaic)

        img_type = mosaics[mosaic]
        mosaic_rasts = [r for r in rasters if img_type in r]
        mosaic_path = os.path.join(fgdb_dir, fgdb, mosaic)

        create_mosaic(fgdb_dir, fgdb, mosaic, img_type)
        arcpy.AddRastersToMosaicDataset_management(mosaic_path,
                                                   'Raster Dataset',
                                                   [os.path.join(input_dir, r) for r in mosaic_rasts])


def get_raster_func(input):
    templates_dir = os.path.join(os.getcwd(), 'templates')
    rast_funcs = {
        'distribution': os.path.join(templates_dir, 'distr.rft.xml'),
        'ex_situ_collections': os.path.join(templates_dir, 'ex_coll.rft.xml'),
        'ex_situ_geo_gaps': os.path.join(templates_dir, 'ex_geo_gaps.rft.xml'),
        'in_situ_geo_gaps': os.path.join(templates_dir, 'in_geo_gaps.rft.xml')
    }

    for img_type in rast_funcs:
        if img_type in input:
            return rast_funcs[img_type]


def set_raster_funcs(fgdb_dir, fgdb):
    print('Setting raster function processing templates')

    for mosaic in mosaics:
        try:
            raster_func = get_raster_func(mosaic)

            arcpy.SetMosaicDatasetProperties_management(os.path.join(fgdb_dir, fgdb, mosaic),
                                                        processing_templates=raster_func,
                                                        default_processing_template=raster_func)
        except KeyError:
            pass


def main(input_dir):
    arcpy.env.workspace = os.getcwd()
    arcpy.env.overwriteOutput = True
    fgdb = 'CWR.gdb'

    fgdb_dir = os.path.dirname(input_dir)

    create_gdb(fgdb_dir, fgdb)
    add_rasters_to_mosaics(input_dir, fgdb_dir, fgdb)
    set_raster_funcs(fgdb_dir, fgdb)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit('Usage: python3 map_rasters.py [root folder]')

    main(sys.argv[1])
