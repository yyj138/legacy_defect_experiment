# 液晶斯格明子弦的3D可视化代码

import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D 
from mpl_toolkits.mplot3d.art3d import Poly3DCollection 
from matplotlib.colors import LinearSegmentedColormap 

# 设置matplotlib参数以获得科研级别的可视化效果
plt.rcParams['font.family'] = 'serif'  # 使用衬线字体
plt.rcParams['font.size'] = 12  # 设置基础字体大小
plt.rcParams['axes.linewidth'] = 1.5  # 坐标轴线条宽度
plt.rcParams['xtick.major.width'] = 1.5  # x轴主刻度线宽度
plt.rcParams['ytick.major.width'] = 1.5  # y轴主刻度线宽度
plt.rcParams['xtick.minor.width'] = 1.0  # x轴次刻度线宽度
plt.rcParams['ytick.minor.width'] = 1.0  # y轴次刻度线宽度
plt.rcParams['legend.frameon'] = False  # 图例无边框
plt.rcParams['figure.dpi'] = 300  # 图像分辨率

class SkyrmionVisualizer:

    
    def __init__(self, period_length=2.0, box_length=8.0, box_width=3.0, box_thickness=2.5):
        self.period_length = period_length
        self.box_length = box_length
        self.box_width = box_width
        self.box_thickness = box_thickness
        
        # 斯格明子核心位置（基于反向平行机制：x = 1.5L 和 3.5L）
        self.skyrmion_positions = [1.5 * period_length, 3.5 * period_length]
        
        # 初始化图形
        self.fig = plt.figure(figsize=(16, 9))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # 设置图形样式
        self._setup_figure_style()
    
    def _setup_figure_style(self):
        # 移除网格和背景面板
        self.ax.grid(False)
        self.ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        
        # 设置坐标轴范围
        self.ax.set_xlim(0, self.box_length)
        self.ax.set_ylim(-self.box_width / 2, self.box_width / 2)
        self.ax.set_zlim(0, self.box_thickness)
        
        # 设置坐标轴比例
        self.ax.set_box_aspect([self.box_length, self.box_width, self.box_thickness])
        
        # 设置坐标轴标签
        self.ax.set_xlabel('x (μm)', fontsize=14, labelpad=15, fontweight='bold')
        self.ax.set_ylabel('y (μm)', fontsize=14, labelpad=15, fontweight='bold')
        self.ax.set_zlabel('z (μm)', fontsize=14, labelpad=15, fontweight='bold')
        
        # 设置标题
        self.ax.set_title('Liquid Crystal Skyrmion Strings', 
                         pad=30, fontsize=18, fontweight='bold', color='darkblue')
        
        # 设置视角
        self.ax.view_init(elev=22, azim=-65)
    
    def _draw_substrates(self):
        # 底部基板
        verts_b = [[(0, -self.box_width / 2, 0), 
                   (self.box_length, -self.box_width / 2, 0), 
                   (self.box_length, self.box_width / 2, 0), 
                   (0, self.box_width / 2, 0)]]
        self.ax.add_collection3d(Poly3DCollection(verts_b, 
                                                 alpha=0.05, 
                                                 color='gray', 
                                                 edgecolor='k', 
                                                 linewidth=0.3))
        
        # 顶部基板
        verts_t = [[(0, -self.box_width / 2, self.box_thickness), 
                   (self.box_length, -self.box_width / 2, self.box_thickness), 
                   (self.box_length, self.box_width / 2, self.box_thickness), 
                   (0, self.box_width / 2, self.box_thickness)]]
        self.ax.add_collection3d(Poly3DCollection(verts_t, 
                                                 alpha=0.05, 
                                                 color='gray', 
                                                 edgecolor='k', 
                                                 linewidth=0.3))
    
    def _draw_bottom_directors(self):
        # 生成高密度网格
        x_dense = np.linspace(0, self.box_length, 130)
        y_dense = np.linspace(-self.box_width / 2, self.box_width / 2, 10)
        X_d, Y_d = np.meshgrid(x_dense, y_dense)
        
        # 计算指向矢方向（基于周期性排列）
        alpha_d = np.pi * X_d / self.period_length
        U_d, V_d = np.cos(alpha_d), np.sin(alpha_d)
        W_d = np.zeros_like(X_d)
        
        # 绘制指向矢
        self.ax.quiver(X_d[:, ::2], Y_d[:, ::2], W_d[:, ::2], 
                       U_d[:, ::2], V_d[:, ::2], W_d[:, ::2], 
                       length=0.15, color='black', alpha=0.4, linewidth=0.5)
    
    def _draw_top_directors(self):
        # 生成网格
        x_top = np.linspace(0.1, self.box_length - 0.1, 40)
        y_top = np.linspace(-self.box_width / 2 + 0.2, self.box_width / 2 - 0.2, 8)
        X_t, Y_t = np.meshgrid(x_top, y_top)
        
        # 绘制沿y轴的指向矢
        self.ax.quiver(X_t, Y_t, self.box_thickness, 
                       np.zeros_like(X_t), np.ones_like(X_t), np.zeros_like(X_t), 
                       length=0.18, color='red', alpha=0.3, linewidth=0.6)
    
    def _draw_skyrmion_strings(self):
        for i, px in enumerate(self.skyrmion_positions):
            # 绘制核心立方体
            self._draw_skyrmion_core(px, i)
            
            # 绘制弦
            self._draw_skyrmion_string(px)
    
    def _draw_skyrmion_core(self, px, index):
        w = 0.6  # 核心立方体宽度
        x_r, y_r, z_r = [px - w / 2, px + w / 2], \
                        [-self.box_width / 2, self.box_width / 2], \
                        [0, self.box_thickness]
        
        # 定义立方体的六个面
        faces = [
            [(x_r[0], y_r[0], z_r[0]), (x_r[1], y_r[0], z_r[0]), 
             (x_r[1], y_r[1], z_r[0]), (x_r[0], y_r[1], z_r[0])],
            [(x_r[0], y_r[0], z_r[1]), (x_r[1], y_r[0], z_r[1]), 
             (x_r[1], y_r[1], z_r[1]), (x_r[0], y_r[1], z_r[1])],
            [(x_r[0], y_r[0], z_r[0]), (x_r[1], y_r[0], z_r[0]), 
             (x_r[1], y_r[0], z_r[1]), (x_r[0], y_r[0], z_r[1])],
            [(x_r[1], y_r[0], z_r[0]), (x_r[1], y_r[1], z_r[0]), 
             (x_r[1], y_r[1], z_r[1]), (x_r[1], y_r[0], z_r[1])],
            [(x_r[1], y_r[1], z_r[0]), (x_r[0], y_r[1], z_r[0]), 
             (x_r[0], y_r[1], z_r[1]), (x_r[1], y_r[1], z_r[1])],
            [(x_r[0], y_r[1], z_r[0]), (x_r[0], y_r[0], z_r[0]), 
             (x_r[0], y_r[0], z_r[1]), (x_r[0], y_r[1], z_r[1])]
        ]
        
        # 使用不同颜色区分不同斯格明子
        core_colors = ['purple', 'cyan']
        color = core_colors[index % len(core_colors)]
        
        # 添加立方体
        self.ax.add_collection3d(Poly3DCollection(faces, 
                                                 alpha=0.15, 
                                                 color=color, 
                                                 edgecolor='none'))
    
    def _draw_skyrmion_string(self, px):
        # 生成弦的路径
        z_path = np.linspace(0, self.box_thickness, 60)
        
        # 绘制弦
        self.ax.plot([px] * 60, [0] * 60, z_path, 
                    color='blue', linewidth=3.5, alpha=0.8)
        
        # 添加弦的中间标记
        self.ax.scatter([px], [0], [self.box_thickness / 2], 
                       color='blue', s=100, edgecolors='white', zorder=10)
        
        # 添加x坐标标注
        self.ax.text(px, 0, self.box_thickness / 2 + 0.2, 
                    f'x={px:.1f}', ha='center', 
                    color='blue', weight='bold', fontsize=12)
    
    def visualize(self, save_path=None):
        # 绘制各组件
        self._draw_substrates()
        self._draw_bottom_directors()
        self._draw_top_directors()
        self._draw_skyrmion_strings()
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图像（如果指定了路径）
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"图像已保存到: {save_path}")
        
        # 显示图像
        plt.show()

if __name__ == "__main__":
    # 创建可视化实例
    visualizer = SkyrmionVisualizer()
    
    # 生成可视化并保存图像
    save_path = "skyrmion_visualization.png"
    visualizer.visualize(save_path)