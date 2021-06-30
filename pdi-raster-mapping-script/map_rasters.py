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
            input_rast_path = os.path.join(input_dir, file)
            mosaic = file.replace('.mrf', '')
            mosaic_path = os.path.join(arcpy.env.workspace, fgdb, mosaic)

            # Create new mosaic dataset in file Geodatabase
            arcpy.CreateMosaicDataset_management(
                    os.path.join(arcpy.env.workspace, fgdb),          # Path to new mosaic
                    mosaic,                                           # Mosaic name
                    arcpy.SpatialReference('WGS 1984 UTM Zone 14N'),  # Coordinate system
                    1)                                                # No. of bands

            # Generate new raster from custom raster function
            arcpy.GenerateRasterFromRasterFunction_management(
                    rast_func,                                        # Raster function dir/name
                    mosaic_path,                                      # Output raster dir/name
                    'Raster ' + input_rast_path,                      # Raster function args
                    format='MRF')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 map_rasters.py [root folder] [raster function file]')
        exit()

    root_dir = sys.argv[1]
    rast_func = sys.argv[2]
    fgdb = 'mosaics.gdb'

    # Set environment variables
    arcpy.env.workspace = os.getcwd()
    arcpy.env.overwriteOutput = True

    # Create new file Geodatabase in current directory and set environment variables
    arcpy.CreateFileGDB_management(os.getcwd(), fgdb)

    # Map rasters using custom raster function file and put them into file geodatabase
    map_rasters(root_dir, arcpy.env.workspace, rast_func, fgdb)
