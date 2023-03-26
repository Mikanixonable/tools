#txtファイルにある文字列の画像を一字ずつ描画するプログラム
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw
import os

with open("JIS1.txt", encoding="utf-8") as f:
    text = f.read()
    
dirname = "kanji"
if not os.path.exists(dirname):
    os.mkdir(dirname)
data_dir = Path(dirname)
font_file = r'.\SourceHanSerif-Heavy.otf'
font_size = 512
font = ImageFont.truetype(font=font_file, size=font_size, index=0)
background_color = (255, 255, 255)
font_color =  (0, 0, 0)
position = (0, -140)
image_size = (512, 512)

for (n, letter) in enumerate(text):
    
    im = Image.new(mode='RGB', size=image_size, color=background_color)
    draw = ImageDraw.Draw(im)

    draw.text(xy=position, text=letter, font=font, fill=font_color)
    bbox = im.getbbox()
    im_crop = im.crop(box=bbox)
    code_point = "uni"+hex(ord(letter))[2:]
    name = f'{code_point}.bmp'
    file = data_dir.joinpath(name)
    im_crop.save(file)