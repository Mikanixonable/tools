#paletteMakettf
import PIL
import matplotlib.pyplot as plt
import extcolors
import glob
import math

import os

import cv2 as cv2
import numpy as np
from lxml import etree


#######################colorDic 自動生成################################################
n = 60
b = 256
def cLength(arr1,arr2):
    return (arr1[0]-arr2[0])**2 + (arr1[1]-arr2[1])**2 + (arr1[2]-arr2[2])**2
def imgJoin2(imgNameList, color="black"):
    k = -math.floor(-len(imgNameList)**(1/2))
    dst = PIL.Image.new("RGB", (b*k, b*k), color)
    for i, imgName in enumerate(imgNameList):
        img = PIL.Image.open(imgName).resize((b,b))
        dst.paste(img, (i%k*b, i//k*b))
    return dst

pngList = glob.glob("*png")
pngList =pngList[:800]
img = imgJoin2(pngList).resize((2048,2048))
img.save("palette.jpeg")

colors, pixelCount = extcolors.extract_from_image(img, tolerance = 18, limit = n) #tolerance 大きいほどカラフル、軽量

colorCodes = ['#{:02x}{:02x}{:02x}'.format(*rgb[0]) for rgb in colors]
colorRates = [rgb[1]**0.55 for rgb in colors]
colorDic = {str(colorCode) : str(colorCode) for colorCode in colorCodes}
colorValues = [[rgb[0][0],rgb[0][1],rgb[0][2]] for rgb in colors]
colorLengths = [cLength(colorValue,[255,255,255]) for colorValue in colorValues]

back = []
for i in range(len(colorCodes)):
    if colorLengths[i] < 15000:
        back.append(colorCodes[i])
print(back)
plt.pie(colorRates,labels=colorCodes,colors=colorCodes,startangle=90,counterclock=False,wedgeprops={"width":0.05})
plt.savefig("Color.jpeg")
plt.show()
#################################################################################




fontname = "test1"
svgbase = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 5120 5120">
</svg>
'''

#色辞書palettDicをbgr配列化
colorList = []
for k, v in colorDic.items():
    colorList.append([int(v[5:7],16),int(v[3:5],16),int(v[1:3],16)])#rgbをbgrにして各色取り出し

#フォルダ名づけ用の色名配列作成
colorDicList = list(colorDic.keys())
colorCodeList = list(colorDic.values())


#色を与えるとパレットの中から一番近い色を返す関数
def cSelect(color,palettes):
    lengArr = []
    for palette in palettes:
        lengArr.append(cLength(palette,color))
    fillc = palettes[lengArr.index(min(lengArr))]
    return fillc

#階調化に必要な色のボロノイマップ対応辞書をつくる関数。軽量化のため色空間32立方をまとめて1つの写像。フルカラーで8*8*8個
def makeBoronoi(palettes):
    boronoiMap = [[[0 for _ in range(8)] for _ in range(8)] for _ in range(8)]
    for bi, bv in enumerate(boronoiMap):
        for gi, gv in enumerate(bv):
            for ri, rv in enumerate(gv):
                boronoiMap[bi][gi][ri] = cSelect([bi*32,gi*32,ri*32],palettes)
    return boronoiMap

#色を与えると色対応辞書から近い色を返す関数
def cSelect2(color,boronoiMap):
    x = color[0]//32
    y = color[1]//32
    z = color[2]//32
    return boronoiMap[x][y][z]

#階調化画像と色リストから黒シルエットsvgを色数ぶん保存する関数
def gradDevider(image,colorList,colorDicList,file):
    root = etree.fromstring(svgbase)
    for index, palette in enumerate(colorList):
        if colorDicList[index] not in back:
        
            themec = np.array(colorList[index])  # 抽出する色(bgr)
            extract = cv2.inRange(image, themec, themec) #色の幅ゼロで色抽出
            extract = cv2.bitwise_not(extract) #白黒反転
            if not os.path.exists("SVGs"):
                os.mkdir("SVGs")
                        
            # #bmpを書いてsvgに変換
            name = os.path.splitext(file)[0]
            cv2.imwrite("tmp.bmp",extract)  # 画像の保存
            os.system("potrace -s tmp.bmp") #bmp -> svg
            os.system("del tmp.bmp")
            
            # baseSVGをパースする
            # baseSVG = etree.parse("tmp.svg")
            # g = baseSVG.find('.//svg:g', namespaces={"svg": "http://www.w3.org/2000/svg"})
            
            # 単色svgからpath要素を抜き出す
            b_tree = etree.parse("tmp.svg")
            paths = b_tree.xpath('//svg:path', namespaces={"svg": "http://www.w3.org/2000/svg"})
            # path要素にfill属性を追加して、g要素に加える
            for path in paths:
                path.set('fill', colorCodeList[index])
                #g.append(path)
                root.append(path)
            # a.svgに書き込む
            with open("./SVGs/"+name+".svg", "wb") as f:
                f.write(etree.tostring(root))
            os.system("del tmp.svg")
        
#####################実行########################

#色空間で最近傍の色を対応付けるボロノイ写像マップをつくる
boronoi = makeBoronoi(colorList)

pngNames = glob.glob("*.png")
for index, file in enumerate(pngNames):
    img = cv2.imread(file)
    img = cv2.flip(img, 0)
    h, w = img.shape[:2]

    # 階調化
    for i in range(h):
        for j in range(w):
            b, g, r = img[i, j]
        
            img[i, j] = cSelect2([b,g,r],boronoi)
    # if not os.path.exists("pngs"):
    #     os.mkdir("pngs")
    # cv2.imwrite("./pngs/"+file,img)
    # 色ごとに分離
    gradDevider(img,colorList,colorDicList,file)
    print(str(file) + " " + str(index+1) + "/" + str(len(pngNames)))

#COLR書き出し
text = "nanoemoji --family \"{}\" --color_format glyf_colr_1"
svgs = glob.glob("./SVGs/*.svg")
svgnames = ""
for svg in svgs:
    svgnames += " " + svg

command = text.format(fontname)+svgnames
os.system(command)


