from pathlib import Path
from PIL import Image, ImageFont, ImageDraw

def main():

  

    data_dir = Path(r'C:\SDtool\trainf')


    font_file = r'C:\SDtool\wof\SourceHanSans-Light.otf'
    font_size = 512
    font = ImageFont.truetype(font=font_file, size=font_size, index=0)


    background_color = (255, 255, 255)


    font_color =  (0, 0, 0)

 
    position = (0, -140)

    image_size = (512, 512)


    for n in range(300):
        im = Image.new(mode='RGB', size=image_size, color=background_color)

        draw = ImageDraw.Draw(im)

        draw.text(xy=position, text=chr(int(0x3041)+n), font=font, fill=font_color)


        bbox = im.getbbox()


        im_crop = im.crop(box=bbox)


        code_point = int(0x3041)+n


        name = f'{"uni"+hex(code_point)[2:]}.bmp'


        file = data_dir.joinpath(name)


        im_crop.save(file)
    return

if __name__ == '__main__':
    main()