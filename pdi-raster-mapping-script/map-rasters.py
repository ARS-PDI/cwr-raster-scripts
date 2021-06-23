import arcpy
import arcgis

DEBUG = True

if __name__ == '__main__':
    if DEBUG:
        exit()

    # 1. TODO: Add/access cloud storage connection?
    # 2. TODO: Create new file Geodatabase in project
    arcpy.CreateFileGDB_management('path', 'fgdb.gdb')
    # 3. TODO: Create new mosaic dataset in file Geodatabase
    #    - WGS_1984_Web_Mercator_Auxiliary_Sphere coordinate system
    arcpy.CreateMosaicDataset_management()
    # 4. TODO: Add raster file to dataset
    arcpy.AddRastersToMosaicDataset_management()
    # 5. TODO: Create raster function template
    #    - Raster -> Remap
    arcgis.raster.remap()
    #    - Remap -> Attribute table
    #    - Page 8
