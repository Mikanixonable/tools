"""
png画像を二値化してttfフォントを作るプログラム。nymwaさんのtwahiに触発されて作った https://github.com/nymwa/ttf-twahi

※このプログラムはfontforgeモジュールを使うため
fontforge-console.batを開くと出るCUIから使う(後述)

###使い方

##準備
magick https://imagemagick.org/index.php
png -> bmp 変換用
ダウンロードしてインストールすればpathが通って使える

potrace https://potrace.sourceforge.net/
bmp -> svg 変換用
ダウンロードしてpotrace.exeがあるフォルダに手動で環境変数を設定しpathを通せば使える
windows10の場合の手順:
設定>システム>詳細情報>システムの詳細設定>環境変数(N)>ユーザーの環境変数>編集(E)>新規
から「C:\p\potrace」などとpotrace.exeのあるフォルダを入力しOKを押す

fontforge https://fontforge.org/en-US/
svg -> ttf 変換用
ダウンロードしてインストールする


##実行
#1
uni0041.png のような形式でunicodeコードがファイル名のpng画像ファイルを用意してpng2ttf.pyと同じフォルダに置く
#2
このコードのname = "font1" の所を作りたいフォント名に書き換える
#3
fontforgeをインストールしたフォルダにあるfontforge-console.batを開けてfontforge python bindingが使えるCUIを開く
#4
「cd C:/Users/Tarou/Downloads」(png2ttfがあるディレクトリへの移動コマンド)「ffpython png2ttf.py」(実行コマンド)などのように打つ
#5
png画像と同じフォルダにttfフォントファイルが書き出される

macやlinuxユーザーならCUIを開かなくてもaptコマンドとかで普通にfontforgeモジュールをインストールしてもっと楽にプログラムを実行できると思う

"""
import os
import glob
import fontforge
# make new font
font = fontforge.font()
# 名前の設定
fontname = "font1"
font.fontname   = fontname
font.fondname   = fontname
font.fullname   = fontname
font.familyname = fontname
font.encoding   = "UnicodeFull"
font.version    = "1.0"

pngs = glob.glob("*.png")
pngs2names = lambda png : os.path.splitext(png)[0]
names = list(map(pngs2names, pngs))
for index, name in enumerate(names):
    os.system("magick " + name+".png " + name+".bmp") #png -> bmp
    os.system("potrace -s " + name+".bmp") #bmp -> svg
    
    hexCodepoint = name[3:] #uni0041 -> 0041
    glyph = font.createMappedChar(int("0x"+hexCodepoint, 16))       
    glyph.importOutlines(name+".svg") 

    os.system("del " + name+".bmp") #Tatsutori atowo nigosazu
    os.system("del " + name+".svg")
    print(str(index + 1)+"/"+str(len(names)))

font.generate(fontname + '.ttf')
font.close()

