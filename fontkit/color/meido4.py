import cv2  # OpenCVのインポート
import numpy as np
import os
import glob

files = glob.glob("*.bmp")
for file in files:
	img = cv2.imread(file) 
	gamma     = 5                              # γ値を指定
	img2gamma = np.zeros((256,1),dtype=np.uint8)  # ガンマ変換初期値

	for i in range(256):
	    img2gamma[i][0] = 255 * (float(i)/255) ** (1.0 /gamma)

	gamma_img = cv2.LUT(img,img2gamma)
	cv2.imwrite(file,gamma_img)  # 画像の保存