import glob
import os

dirs = glob.glob('*/')
for dir in dirs:
    # print(dir)
    heics = glob.glob(f'{dir}/*.MOV')
    for heic in heics:
        print(heic)
        jpg = heic.split('.')[0]+'.mp4'
        
        os.system(f'ffmpeg -i {heic} -codec:v mpeg4 {jpg}')
        os.remove(f'{heic}')
