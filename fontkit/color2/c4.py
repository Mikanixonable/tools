#パレットのうち最近傍の色で塗るプログラム
import cv2
import numpy as np
import os
file = 'b.png'
img = cv2.imread(file)
h, w = img.shape[:2]
palettes = [
    [255,255,255],#白
    [0,0,0],#黒
    [143,179,70],#青
    [227,192,48],#青
    [76,161,28],#緑
    [167,228,119],#黄色
    [24,34,239],#黄色
    [137,120,11],#aou
    [217,119,38],#ao
    [213,34,67],#purpl
    [105,50,20],#ai
    [6,153,255],#赤
    [127,123,246],#赤
]

#色と色の距離を計算する関数
def cLength(arr1,arr2):
    return np.sqrt((arr1[0]-arr2[0])**2 + (arr1[1]-arr2[1])**2 + (arr1[2]-arr2[2])**2)

#色を与えるとパレットの中から一番近い色を返す関数
def cSelect(color,palettes):
    lengArr = []
    for palette in palettes:
        lengArr.append(cLength(palette,color))
    fillc = palettes[lengArr.index(min(lengArr))]
    return fillc

# 色の変更
for i in range(h):
    for j in range(w):
        b, g, r = img[i, j]
        color = [b,g,r]
        img[i, j] = cSelect(color,palettes)
cv2.imwrite(os.path.basename(file) + "_c" + ".png",img)  # 画像の保存
# cv2.imwrite(file,img)  # 画像の保存