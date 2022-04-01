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


def create_gdb(name):
    arcpy.CreateFileGDB_management(arcpy.env.workspace, name)


def create_mosaics(gdb):
    global mosaics

    for mosaic in mosaics:
        arcpy.CreateMosaicDataset_management(
            gdb, mosaic, arcpy.SpatialReference('WGS 1984'))


def add_rasters_to_mosaics(input_dir, fgdb):
    global mosaics

    rasters = os.listdir(input_dir)

    for img_type in mosaics:
        mosaic_rasts = [r for r in rasters if img_type in r]
        mosaic_path = os.path.join(fgdb, mosaics[img_type])

        arcpy.AddRastersToMosaicDataset_management(mosaic_path,
                                                   'Raster Dataset',
                                                   [os.path.join(input_dir, r) for r in mosaic_rasts])


def get_raster_func(input):
    templates_dir = 'templates'
    rast_funcs = {
        'distribution': os.path.join(templates_dir, 'distr.rft.xml'),
        'ex_situ_collections': os.path.join(templates_dir, 'ex_coll.rft.xml'),
        'ex_situ_geo_gaps': os.path.join(templates_dir, 'ex_geo_gaps.rft.xml'),
        'in_situ_geo_gaps': os.path.join(templates_dir, 'in_geo_gaps.rft.xml')
    }

    for img_type in rast_funcs:
        if img_type in input:
            return rast_funcs[img_type]


def set_raster_funcs(fgdb):
    for mosaic in mosaics:
        try:
            raster_func = get_raster_func(mosaic)

            arcpy.SetMosaicDatasetProperties_management(os.path.join(fgdb, mosaic),
                                                        processing_templates=raster_func,
                                                        default_processing_template=raster_func)
        except KeyError:
            pass


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit('Usage: python3 map_rasters.py [root folder]')

    arcpy.env.workspace = os.getcwd()
    arcpy.env.overwriteOutput = True
    fgdb = 'CWR.gdb'

    create_gdb(fgdb)
    create_mosaics(fgdb)

    add_rasters_to_mosaics(sys.argv[1], fgdb)
    set_raster_funcs(fgdb)
