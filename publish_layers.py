import arcpy
import os
import sys
from time import gmtime, strftime

img_types = ['ersEx', 'ersIn', 'ga50', 'grsEx', 'grsIn', 'thrsld']


def _get_img_type(mos):
    for img_type in img_types:
        if img_type in mos:
            if img_type == 'thrsld':
                return 'median'
            return img_type

    raise ValueError('Unknown image type')


def create_name(mos):
    img_type = _get_img_type(mos)
    datetime = strftime('%m%d%y%H%M', gmtime())

    return f'{img_type}_{datetime}'


def _check_species(species):
    for kw in ['var', 'subsp']:
        if kw in species:
            species = species.replace(kw, f'{kw}.')

    return species.strip()


def get_species(name_list):
    type_idx = -1

    for i in range(len(img_types)):
        try:
            type_idx = name_list.index(img_types[i])
        except ValueError:
            continue

    if type_idx < 0:
        raise ValueError('No image type found.')

    species = ''

    for i in range(1, type_idx):
        species += f'{name_list[i]} '

    return _check_species(species), type_idx


def create_img_type(name_list, type_idx):
    img_type = name_list[type_idx]

    if type_idx < len(name_list) - 1:
        img_type += f'_{name_list[-1]}'

    return img_type


def _get_img_data(mos):
    name_list = mos.split('_')

    genus = name_list[0]
    species, type_idx = get_species(name_list)
    img_type = create_img_type(name_list, type_idx)

    return genus, species, img_type


def create_summary(mos):
    genus, species, img_type = _get_img_data(mos)

    return f'{genus}\n{genus + " " + species}\n{img_type}'


def create_tags(mos):
    return f'CWR,Imagery,{_get_img_type(mos)},ARS,PDI'


def publish_layers(workspace):
    """
    workspace: Folder containg GDB(s)
    """
    for gdb in os.listdir(workspace):
        arcpy.env.workspace = gdb_path = os.path.join(workspace, gdb)
        arcpy.env.overwriteOutput = False

        max_tries = 3
        mos_datasets = arcpy.ListDatasets(feature_type='Mosaic')
        mos_datasets_len = 0

        try:
            mos_datasets_len = len(mos_datasets)
        except:
            continue

        for i in range(mos_datasets_len):
            mos = mos_datasets[i]
            sd_draft = os.path.join(workspace, mos + '.sddraft')
            sd = os.path.join(workspace, mos + '.sd')

            for curr_try in range(max_tries):
                try:
                    arcpy.CreateImageSDDraft(
                        os.path.join(gdb_path, mos),
                        sd_draft,
                        create_name(mos),
                        'ARCGIS_SERVER',
                        copy_data_to_server=True,
                        folder_name='CWR',
                        summary=create_summary(mos),
                        tags=create_tags(mos)
                    )

                    break
                except:
                    pass

            for curr_try in range(max_tries):
                try:
                    arcpy.StageService_server(sd_draft, sd)

                    break
                except:
                    pass

            success = False

            for curr_try in range(max_tries):
                try:
                    print(
                        f'[{curr_try + 1}] Uploading the service definition for', mos)

                    arcpy.UploadServiceDefinition_server(
                        sd,
                        'https://pdiimagery.azurecloudgov.us/arcgis',
                        in_my_contents=True,
                        in_public=True,
                        in_organization='SHARE_ORGANIZATION'
                    )

                    print(f'{mos} successfully published')
                    success = True

                    break
                except:
                    pass

            if not success:
                with open('publish_log.txt', 'a') as f:
                    f.write(f'{mos}\n')

            try:
                os.remove(os.path.join(workspace, f'{mos}.sddraft'))
                os.remove(os.path.join(workspace, f'{mos}.sd'))

                print('Cleaned', mos, 'service definitions')
            except FileNotFoundError:
                pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit('Usage: python3 publish_layers.py [GDBs folder]')

    arcpy.SignInToPortal(
        'https://pdienterprise.azurecloudgov.us/portal',
        os.environ.get('AG_USERNM'),
        os.environ.get('AG_PASSWD')
    )

    workspace = sys.argv[1]

    publish_layers(workspace)
