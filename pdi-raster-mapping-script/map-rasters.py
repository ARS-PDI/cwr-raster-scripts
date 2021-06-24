import sys
import arcpy
from os import path
import arcgis

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 map-rasters.py [workspace] [folder with MRF files]')
        exit()

    workspace = sys.argv[1]
    mrf_folder = sys.argv[2]
    test_mosaic = 'test_mosaic'
    fgdb = 'workspace.gdb'

    # TODO?: Add/access cloud storage connection

    # Create new file Geodatabase in project
    arcpy.CreateFileGDB_management(workspace, fgdb)

    # Create new mosaic dataset in file Geodatabase
    # - WGS_1984_UTM_Zone_14N coordinate system
    arcpy.env.workspace = path.join(workspace, fgdb)
    coord_sys = arcpy.SpatialReference('WGS 1984 UTM Zone 14N')
    arcpy.CreateMosaicDataset_management(arcpy.env.workspace, test_mosaic, coord_sys, 1)

    # Add raster file to dataset
    dataset_path = path.join(arcpy.env.workspace, test_mosaic)
    input_path = path.join(workspace, mrf_folder) # FIXME
    arcpy.AddRastersToMosaicDataset_management(dataset_path, 'Raster Dataset', input_path)

    # TODO: Raster -> Remap
    curr_rast = path.join(arcpy.env.workspace, test_mosaic)
    input_ranges = [1, 10, 20]
    output_ranges = [10, 20, 30]
    arcgis.raster.functions.remap(test_mosaic, input_ranges, output_ranges)

    # TODO: Remap -> Attribute table (Page 8)
