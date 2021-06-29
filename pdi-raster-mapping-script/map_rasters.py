import os
import sys
import arcpy

def map_rasters(input_dir, workspace, rast_func, fgdb):
    # arg 1: Input directory w/ MRFs -- input_dir
    for file in os.listdir(input_dir):
        arcpy.env.workspace = workspace

        if os.path.isdir(os.path.join(input_dir, file)):
            map_rasters(os.path.join(input_dir, file), workspace, rast_func, fgdb)
        elif file.endswith('.mrf'):
            # Create new mosaic dataset in file Geodatabase
            mosaic = file.replace('.mrf', '')
            arcpy.CreateMosaicDataset_management(os.path.join(arcpy.env.workspace,
                                                              fgdb),
                                                 mosaic,
                                                 coord_sys,
                                                 1)

            # Generate new raster from custom raster function
            arcpy.GenerateRasterFromRasterFunction_management(
                os.path.join(os.getcwd(), rast_func),
                os.path.join(arcpy.env.workspace, fgdb, file),
                'Raster ' + os.path.join(input_dir, file),
                format='MRF')

            # Add raster file to dataset
            dataset_path = os.path.join(arcpy.env.workspace, fgdb, mosaic)
            raster = os.path.join(os.path.join(input_dir, file))
            arcpy.AddRastersToMosaicDataset_management(dataset_path, 'Raster Dataset', raster)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 map_rasters.py [root folder] [raster function file]')
        exit()

    root_dir = sys.argv[1]
    rast_func = sys.argv[2]
    fgdb = 'mosaics.gdb'

    # Create new file Geodatabase in current directory and set environment variables
    try:
        arcpy.CreateFileGDB_management(os.getcwd(), fgdb)
    except:
        pass

    coord_sys = arcpy.SpatialReference('WGS 1984 UTM Zone 14N')

    # Map rasters using custom raster function file and put them into file geodatabase
    map_rasters(root_dir, arcpy.env.workspace, rast_func)
