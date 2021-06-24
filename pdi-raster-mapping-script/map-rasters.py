import os
import sys
import arcpy
import arcgis

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 map-rasters.py [workspace]')
        exit()

    arcpy.env.workspace = workspace = sys.argv[1]
    fgdb = 'workspace.gdb'

    # TODO?: Add/access cloud storage connection

    # Create new file Geodatabase in project
    arcpy.CreateFileGDB_management(workspace, fgdb)

    # Create new mosaic dataset in file Geodatabase
    # - WGS_1984_UTM_Zone_14N coordinate system
    coord_sys = arcpy.SpatialReference('WGS 1984 UTM Zone 14N')
    arcpy.CreateMosaicDataset_management(arcpy.env.workspace, 'test-mosaic', coord_sys, 1)

    # TODO: Add raster file to dataset
    dataset_path = os.path.join(workspace, fgdb)
    input_path = os.path.join(workspace) # FIXME
    arcpy.AddRastersToMosaicDataset_management(dataset_path, 'Raster Dataset', input_path)

    # TODO: Raster -> Remap
    arcgis.raster.remap()

    # TODO: Remap -> Attribute table (Page 8)
