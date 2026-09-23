import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class Visualization:
    # 可视化模块

    @staticmethod
    def visualize_defect(cylinders, title="液晶分子排列"):
        # 可视化缺陷结构
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        for (x, y, z) in cylinders:
            ax.plot_surface(x, y, z, color='b', alpha=0.6)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(title)
        ax.set_aspect('equal')

        return fig, ax

    @staticmethod
    def visualize_2d_grid(pattern_type, x_range=None, y_range=None, z=3):
        # 可视化2D网格点图
        from core.patterns import Patterns

        patterns = Patterns()

        if x_range is None:
            x_range = range(-patterns.rangexOy, patterns.rangexOy + 1)
        if y_range is None:
            y_range = range(-patterns.rangexOy, patterns.rangexOy + 1)

        y_components = []
        positions = []

        for x in x_range:
            for y in y_range:
                if pattern_type == 'r':
                    angle_x, angle_y, angle_z = patterns.r_pattern(x, y, z)
                elif pattern_type == 'c':
                    angle_x, angle_y, angle_z = patterns.c_pattern(x, y, z)
                elif pattern_type == 'uniform':
                    angle_x, angle_y, angle_z = patterns.uniform_pattern(x, y, z)
                else:
                    raise ValueError(f"Unknown pattern type: {pattern_type}")

                y_comp = np.sin(angle_y) * np.cos(angle_x)
                y_components.append(y_comp)
                positions.append((x, y))

        positions = np.array(positions)
        y_components = np.array(y_components)

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111)

        scatter = ax.scatter(positions[:, 0], positions[:, 1], c=y_components, cmap='RdBu', s=100)
        cbar = fig.colorbar(scatter, ax=ax)
        cbar.set_label('Director y-component')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(f'{pattern_type.upper()} Pattern - 2D Director Field')
        ax.set_aspect('equal')

        return fig, ax

    @staticmethod
    def save_visualization(cylinders, filename, directory="./examples"):
        # 保存可视化结果
        os.makedirs(directory, exist_ok=True)
        fig, ax = Visualization.visualize_defect(cylinders, filename)
        filepath = os.path.join(directory, f"{filename}.png")
        plt.savefig(filepath)
        plt.close()
        print(f"已保存 {filepath}")
        return filepath

    @staticmethod
    def save_2d_grid_visualization(pattern_type, filename, directory="./examples"):
        # 保存2D网格可视化结果
        os.makedirs(directory, exist_ok=True)
        fig, ax = Visualization.visualize_2d_grid(pattern_type)
        filepath = os.path.join(directory, f"{filename}.png")
        plt.savefig(filepath)
        plt.close()
        print(f"已保存 {filepath}")
        return filepath

    @staticmethod
    def show_visualization(cylinders, title="液晶分子排列"):
        # 显示可视化结果
        fig, ax = Visualization.visualize_defect(cylinders, title)
        plt.show()

    @staticmethod
    def show_2d_grid_visualization(pattern_type):
        # 显示2D网格可视化结果
        fig, ax = Visualization.visualize_2d_grid(pattern_type)
        plt.show()
