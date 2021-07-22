import os
import sys
import arcpy

def publish_layers(workspace):
    """
    workspace: Folder containg GDB(s)
    """
    for gdb in os.listdir(workspace):
        arcpy.env.workspace = gdb_path = os.path.join(workspace, gdb)

        for mos in arcpy.ListDatasets(feature_type='Mosaic'):
            sd_draft = os.path.join(workspace, mos + '.sddraft')
            sd = os.path.join(workspace, mos + '.sd')

            try:
                arcpy.CreateImageSDDraft(
                    os.path.join(gdb_path, mos),
                    sd_draft,
                    mos,
                    'ARCGIS_SERVER',
                    folder_name='AgCROS',
                    summary=mos,
                    tags='ARS'
                )
            except:
                exit(arcpy.GetMessages())

            print('Staging service to create service definition')
            try:
                arcpy.StageService_server(sd_draft, sd)
            except:
                print(arcpy.GetMessages())
            
            try:
                print('Uploading the service definition and publishing image service')
                arcpy.UploadServiceDefinition_server(sd, 'HOSTING_SERVER')
                print('Service successfully published')
            except:
                exit(arcpy.GetMessages())

if __name__ == '__main__':
    arcpy.SignInToPortal(
        "https://usdaars.maps.arcgis.com",
        os.environ.get('AG_USERNM'),
        os.environ.get('AG_PASSWD')
    )

    workspace = sys.argv[1]

    publish_layers(workspace)
