from zipfile import ZipFile

SCRATCH_PATH = '/scratch/alanyon/data_science/tweets'


with ZipFile(f'{SCRATCH_PATH}/OneDrive_12_2-23-2022.zip', 'r') as zip:
    zip.extractall(path=f'{SCRATCH_PATH}')
    # zip.printdir()

# for hour in range(6, 24):
#     with ZipFile(f'{SCRATCH_PATH}/geoEurope_20210602{hour:02d}.zip', 'r') as zip:
#         zip.extractall(path=f'{SCRATCH_PATH}')
