import sys
import arcpy
from os import path

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 map-rasters.py [workspace] [folder with MRF files]')
        exit()

    workspace = sys.argv[1]
    mrf_folder = sys.argv[2]
    test_mosaic = 'test_mosaic'
    test_raster = 'grs_pa_PAs_narea_areakm2.mrf'
    test_function = 'test_function.rft.xml'
    fgdb = 'workspace.gdb'

    # Create new file Geodatabase in project
    arcpy.CreateFileGDB_management(workspace, fgdb)

    # Create new mosaic dataset in file Geodatabase
    arcpy.env.workspace = path.join(workspace, fgdb)
    coord_sys = arcpy.SpatialReference('WGS 1984 UTM Zone 14N')
    arcpy.CreateMosaicDataset_management(arcpy.env.workspace, test_mosaic, coord_sys, 1)

    # Add raster file to dataset
    dataset_path = path.join(arcpy.env.workspace, test_mosaic)
    input_path = path.join(workspace, mrf_folder)
    arcpy.AddRastersToMosaicDataset_management(dataset_path, 'Raster Dataset', input_path)

    # Generate new raster from custom raster function
    arcpy.GenerateRasterFromRasterFunction_management(
        path.join(workspace, test_function),
        path.join(workspace, test_raster),
        'Raster ' + path.join(input_path, test_raster),
        format='MRF')
