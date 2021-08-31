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
                    copy_data_to_server=True,
                    folder_name='CWR',
                    summary=mos,
                    tags='ARS, CWR'
                )

                arcpy.StageService_server(sd_draft, sd)

                print('Uploading the service definition for', mos)
                arcpy.UploadServiceDefinition_server(
                    sd,
                    'https://pdiimagery.azurecloudgov.us/arcgis',
                    in_my_contents=True,
                    in_public=True,
                    in_organization='SHARE_ORGANIZATION'
                )
                print('Service successfully published')
            except:
                with open('publish_log.txt', 'a') as f:
                    f.write(f'{mos}\n')
            finally:
                # Clean up service definitions
                os.remove(os.path.join(workspace, f'{mos}.sddraft'))
                os.remove(os.path.join(workspace, f'{mos}.sd'))

if __name__ == '__main__':
    arcpy.SignInToPortal(
        'https://pdienterprise.azurecloudgov.us/portal',
        os.environ.get('AG_USERNM'),
        os.environ.get('AG_PASSWD')
    )

    workspace = sys.argv[1]

    publish_layers(workspace)
