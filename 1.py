#unicodeコードポイントの範囲を指定すると画像を出力するプログラム
startCode = "13000"

endCode =  "1342f"

from pathlib import Path
from PIL import Image, ImageFont, ImageDraw
    
data_dir = Path(r'C:\SDtool\c\egy')
font_file = r'seguihis'
font_size = 400
font = ImageFont.truetype(font=font_file, size=font_size, index=0)
background_color = (255, 255, 255)
font_color =  (0, 0, 0)
position = (20, -40)

image_size = (512, 512)

for n in range(int(startCode,16),int(endCode,16)+1):
    im = Image.new(mode='RGB', size=image_size, color=background_color)
    draw = ImageDraw.Draw(im)
    draw.text(xy=position, text=chr(n), font=font, fill=font_color)
    
    bbox = im.getbbox()
    im_crop = im.crop(box=bbox)
    code_point = n
    name = f'{"uni"+hex(code_point)[2:]}.bmp'
    
    file = data_dir.joinpath(name)
    im_crop.save(file)