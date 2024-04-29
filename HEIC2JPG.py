import glob
import os

dirs = glob.glob('*/')
for dir in dirs:
    # print(dir)
    heics = glob.glob(f'{dir}/*.HEIC')
    for heic in heics:
        print(heic)
        jpg = heic.split('.')[0]+'.JPG'
        
        os.system(f'magick {heic} {jpg}')
        os.remove(f'{heic}')
