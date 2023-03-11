#ライブラリインポート
import moviepy.editor as mp
#gif動画ファイルの読み込み
movie_file=mp.VideoFileClip('julia3.gif')
#mp4動画ファイルの保存
movie_file.write_videofile('1.mp4')
movie_file.close()