import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.animation import FuncAnimation
import math
from numba import jit
@jit

def julia(width, height, N, t):
    Re, Im = np.meshgrid(width, height)             # ReとImの組み合わせを計算
    n_grid = len(Re.ravel())                         # 組み合わせの総数
    z = np.zeros(n_grid)                             # ジュリア集合のデータ格納用空配列
    # zにジュリア集合に属するか否かのデータを格納していくループ
    for i in range(n_grid):                        
        # イタレーション回数nと複素数z0を初期化
        n = 0
        z0 = complex(Re.ravel()[i], Im.ravel()[i])
        while np.abs(z0) < 2 and not n == N:
            # z0 = z0 ** 2 + (2*np.cos(t)-np.cos(t*2)+1j*2*np.sin(t)-1j*np.sin(t*2))/4
            # z0 = z0 ** 5 + z0 -0.4 + t*0.01
            # z0 = (z0 ** 5 + z0)/(np.sin(0.01*t)+1j*np.cos(0.01*t))
            z0 = z0 ** 6 + z0*(-0.5 + t*0.001)
            n += 1                                 
        #色
        if n == N:
            z[i] = N
        else:
            z[i] = n
    z = np.reshape(z, Re.shape)                      # 2次元配列(画像表示用)にリシェイプ
    z = z[::-1]                                      # imshow()で上下逆になるので予め上下反転
    return z

width = [-1.4,1.4]
height = [-1.4,1.4]
resolution = 1000
N = 100

# 実部と虚部の軸データ配列、最大イタレーション数を設定
z_real = np.linspace(width[0], width[1], resolution)
z_imag = np.linspace(height[0], height[1], resolution)

fig = plt.figure(figsize=[10,10])
def plot(k):
    t = 2*np.pi*k/300
    plt.cla()
    z = julia(z_real, z_imag, N, k)
    plt.imshow(z, cmap='YlGnBu_r',
          norm=Normalize(vmin=0, vmax=N),
          extent=[width[0], width[1], height[0], height[1]])
def anim():
    anim = FuncAnimation(fig, plot, frames=10,interval=50)
    anim.save('julia409.gif', writer='pillow', dpi=resolution/10)

# anim()
def img():
    k = 0
    z = julia(z_real, z_imag, N, k)
    plt.imshow(z, cmap='YlGnBu_r',
            norm=Normalize(vmin=0, vmax=N),
            extent=[width[0], width[1], height[0], height[1]])
    plt.savefig("400.png",dpi=resolution/10)
img()
fig.show()
