# plot

import matplotlib.pyplot as plt

def run(repo):
    x = [100, 200, 300, 400, 500, 600]
    y = [10, 20, 30, 50, 80, 130]

    plt.plot(x, y, label="test") # プロット
    plt.legend() # 凡例の表示
    plt.show() # プロット表示(設定の反映)
