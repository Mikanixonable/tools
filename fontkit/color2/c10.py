#パレットのうち最近傍の色で塗るプログラム
import cv2
import numpy as np
import os
import glob

#色と色の二乗距離を計算する関数
def cLength(arr1,arr2):
    return (arr1[0]-arr2[0])**2 + (arr1[1]-arr2[1])**2 + (arr1[2]-arr2[2])**2

#色を与えるとパレットの中から一番近い色を返す関数
def cSelect(color,palettes):
    lengArr = []
    for palette in palettes:
        lengArr.append(cLength(palette,color))
    fillc = palettes[lengArr.index(min(lengArr))]
    return fillc

#階調化に必要な色の対応辞書をつくる関数。軽量化のため色空間32立方をまとめて1つの写像。フルカラーで8*8*8個
def cDicMaker1(palettes):
    cDic = [[[0 for _ in range(8)] for _ in range(8)] for _ in range(8)]
    for bi, bv in enumerate(cDic):
        for gi, gv in enumerate(bv):
            for ri, rv in enumerate(gv):
                cDic[bi][gi][ri] = cSelect([bi*32,gi*32,ri*32],palettes)
    return cDic

#色を与えると色対応辞書から近い色を返す関数
def cSelect2(color,cDic):
    x = color[0]//32
    y = color[1]//32
    z = color[2]//32
    return cDic[x][y][z]

#####################実行########################

palettDic = {
    "main": "#00000C",
    "sub1": "#082F7F",
    "sub2": "#1254D1",
    "light1": "#1A8BFD",
    "light2": "#7FC8FF",
    "white": "#FFFFFF"
}
# palettes = [
#     [255,255,255],#白
#     [0,0,0],#黒
#     [143,179,70],#青
#     [227,192,48],#青
#     [76,161,28],#緑
#     [167,228,119],#黄色
#     [24,34,239],#黄色
#     [137,120,11],#aou
#     [217,119,38],#ao
#     [213,34,67],#purpl
#     [105,50,20],#ai
#     [6,153,255],#赤
#     [127,123,246],#赤
# ]


#色辞書palettDicを配列化
palettes = []
for k, v in palettDic.items():
    palettes.append([int(v[5:7],16),int(v[3:5],16),int(v[1:3],16)])#rgbをbgrにして各色取り出し

#色空間で最近傍の色を対応付けるボロノイ写像マップをつくる
cDic = cDicMaker1(palettes)


files = glob.glob("*.bmp")
for index, file in enumerate(files):
    img = cv2.imread(file)
    h, w = img.shape[:2]
    # 色の変更
    for i in range(h):
        for j in range(w):
            b, g, r = img[i, j]
            #頻出する色はスルー
            if ([b,g,r] != [0,0,0]) and ([b,g,r] != [255,255,255]):
                img[i, j] = cSelect2([b,g,r],cDic)
    cv2.imwrite(os.path.basename(file) + "_c" + ".bmp",img)  # 画像の保存
    # cv2.imwrite(file,img)  # 画像の保存
    print(str(file) + " " + str(index+1) + "/" + str(len(files)))