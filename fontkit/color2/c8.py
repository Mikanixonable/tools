#色ごとに黒いシルエット画像を作るプログラム
import cv2
import numpy as np
import os
import glob
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

files = glob.glob("*.bmp")
for file in files:
	image = cv2.imread(file) # ファイル読み込み
	# bgrでの色抽出
	for index, palette in enumerate(palettes):
		n = index
		themec = np.array(palettes[n])  # 抽出する色の上限(bgr)
		img_mask = cv2.inRange(image, themec, themec) # bgrからマスクを作成
		extract = cv2.bitwise_or(image, image, mask=img_mask) # 元画像とマスクを合成

		# 特定の色を別の色に置換する
		black = [0, 0, 0]
		white = [255, 255, 255]
		extract[np.where((extract == black).all(axis=2))] = white #black2white
		extract[np.where((extract == themec).all(axis=2))] = black #theme2black

		dirname = str(palettes[n])
		if not os.path.exists(dirname):
			os.mkdir(dirname)
		cv2.imwrite(os.path.join(dirname, file),extract)  # 画像の保存
		# print(str(file) + " " + str(index+1) + "/" + str(len(files)))