import os
import sys
import arcpy

def publish_layers(workspace, ags):
    """
    workspace: Folder containg GDB(s)
    ags:       Path to server connection file
    """
    for gdb in os.listdir(workspace):
        gdb_path = os.path.join(workspace, gdb) #File geodatabase used to store a mosaic dataset

        for mos in arcpy.ListDatasets(feature_type='Mosaic'):
            sd_draft = os.path.join(workspace, mos + '.sddraft')
            sd = os.path.join(workspace, mos + '.sd')

            try:
                arcpy.CreateImageSDDraft(
                    os.path.join(gdb_path, mos),
                    sd_draft,
                    mos,
                    'FROM_CONNECTION_FILE',
                    ags,
                    'AgCROS',
                    mos,
                    'ARS'
                )
            except:
                print('Failed in creating sd draft')
                exit()

            # Analyze the service definition draft
            analysis = arcpy.mapping.AnalyzeForSD(sd_draft)
            print(analysis['messages'])
            print(analysis['warnings'])
            print(analysis['errors'])

            # Stage and upload the service if the sd_draft analysis did not contain errors
            if not analysis['errors']:
                print('Staging service to create service definition')
                arcpy.StageService_server(sd_draft, sd)
                
                try:
                    print('Uploading the service definition and publishing image service')
                    arcpy.UploadServiceDefinition_server(sd, ags)

                    print('Service successfully published')
                except:
                    print('Failed to stage and upload service')
                    exit()
            else:
                print('Service could not be published because errors were found during analysis.')
                print(arcpy.GetMessages())

if __name__ == '__main__':
    arcpy.SignInToPortal(
        "https://usdaars.maps.arcgis.com",
        os.environ.get('AG_USERNM'),
        os.environ.get('AG_PASSWD')
    )

    workspace = sys.argv[0]
    ags = sys.argv[1]
    publish_layers(workspace, ags)
