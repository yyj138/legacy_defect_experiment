import numpy as np
import matplotlib.pyplot as plt
import os
from mpl_toolkits.mplot3d import Axes3D

# 设置matplotlib中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class ContinuousSimulation:
    # 连续介质模拟模块

    @staticmethod
    def simulate_moiré_patterns(thicknesses, L=100, nx=100, ny=100, directory="./examples"):
        # 模拟不同厚度下的莫尔条纹和斯格明子
        results = []

        for d in thicknesses:
            x = np.linspace(0, L, nx)
            y = np.linspace(0, L, ny)
            X, Y = np.meshgrid(x, y)

            z = d / 2
            alpha = np.pi * z / L

            y_component = np.zeros_like(X)

            period_bottom = L / 5

            for i in range(nx):
                for j in range(ny):
                    phase_bottom = 2 * np.pi * Y[i, j] / period_bottom
                    phase_top = np.pi / 2
                    phase_diff = alpha
                    y_component[i, j] = np.sin(phase_bottom - phase_top + phase_diff)

            if 20 < d < 50:
                center_x, center_y = L/2, L/2
                r = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
                mask = r < 15
                for i in range(nx):
                    for j in range(ny):
                        if mask[i, j]:
                            r_val = r[i, j]
                            theta = np.arctan2(Y[i, j] - center_y, X[i, j] - center_x)
                            y_component[i, j] = np.sin(alpha + np.pi * r_val / 15 + theta)

            elif d >= 50:
                skyrmion_positions = [(L/2, L/3), (L/2, L/2), (L/2, 2*L/3)]
                for (center_x, center_y) in skyrmion_positions:
                    r = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
                    mask = r < 12
                    for i in range(nx):
                        for j in range(ny):
                            if mask[i, j]:
                                r_val = r[i, j]
                                theta = np.arctan2(Y[i, j] - center_y, X[i, j] - center_x)
                                y_component[i, j] = np.sin(alpha + np.pi * r_val / 12 + theta)

            results.append({
                'thickness': d,
                'x': X,
                'y': Y,
                'y_component': y_component
            })

        return results
