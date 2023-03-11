import cv2  # OpenCVのインポート

import os
import glob

files = glob.glob("*.bmp")
for file in files:
	img = cv2.imread(file) 
	img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)  # 色空間をBGRからHSVに
	s_magnification = 1  # 彩度(Saturation)の倍率
	v_magnification = 0.6  # 明度(Value)の倍率
	
	img_hsv[:,:,(1)] = img_hsv[:,:,(1)]*s_magnification  # 彩度の計算
	img_hsv[:,:,(2)] = img_hsv[:,:,(2)]*v_magnification  # 明度の計算
	img_bgr = cv2.cvtColor(img_hsv,cv2.COLOR_HSV2BGR)  # 色空間をHSVからBGRに変換
	cv2.imwrite(file,img_bgr)  # 画像の保存