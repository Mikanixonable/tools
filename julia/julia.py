import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.animation import FuncAnimation

#高速化のためのおまじない
from numba import jit    
@jit   

def julia(width, height, N, c,theta):
    Re, Im = np.meshgrid(width, height)             # ReとImの組み合わせを計算
    n_grid = len(Re.ravel())                         # 組み合わせの総数
    z = np.zeros(n_grid)                             # ジュリア集合のデータ格納用空配列

    # zにジュリア集合に属するか否かのデータを格納していくループ
    for i in range(n_grid):                        

        # イタレーション回数nと複素数z0を初期化
        n = 0
        z0 = complex(Re.ravel()[i], Im.ravel()[i])

        # z0が無限大になるか、最大イタレーション数になるまでループする
        while np.abs(z0) < 2 and not n == N:
            z0 = z0 ** 6 + 1.01*z0 + 0.1*(np.sin(theta)+1j*np.cos(theta)-1j)                         # 漸化式を計算
            n += 1                                   # イタレーション数を増分

        # z0が無限大に発散する場合はn, 収束する場合は0を格納
        if n == N:
            z[i] = N
        else:
            z[i] = n


    z = np.reshape(z, Re.shape)                      # 2次元配列(画像表示用)にリシェイプ
    z = z[::-1]                                      # imshow()で上下逆になるので予め上下反転
    return z

# 水平方向h(実部Re)と垂直方向v(虚部Im)の範囲を決める
h1 = -1.7
h2 = 1.7
v1 = -1.7
v2 = 1.7

# 分解能を設定
resolution = 500

# 実部と虚部の軸データ配列、最大イタレーション数を設定
z_real = np.linspace(h1, h2, resolution)
z_imag = np.linspace(v1, v2, resolution)
n_max = 50


fig = plt.figure(plt.figure(figsize=[10,10]))
def plot(k):
    a = -0.8
    theta = 2*np.pi*k/360
    plt.cla()
    z = julia(z_real, z_imag, n_max, complex(a,b),theta)
    plt.imshow(z, cmap='gist_gray',
          norm=Normalize(vmin=0, vmax=n_max),
          extent=[h1, h2, v1, v2])
    
    
anim = FuncAnimation(fig, plot, frames=200,interval=50)
anim.save('julia8.gif', writer='pillow', dpi=100)
fig.show()
