#paletteMaker
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