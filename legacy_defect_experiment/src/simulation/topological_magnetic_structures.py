# 拓扑磁结构模拟代码

import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.gridspec import GridSpec
import matplotlib.patches as patches

# 设置matplotlib参数以获得科研级别的可视化效果
plt.rcParams['font.family'] = 'serif'  # 使用衬线字体
plt.rcParams['font.size'] = 10  # 设置基础字体大小
plt.rcParams['axes.linewidth'] = 1.5  # 坐标轴线条宽度
plt.rcParams['xtick.major.width'] = 1.5  # x轴主刻度线宽度
plt.rcParams['ytick.major.width'] = 1.5  # y轴主刻度线宽度
plt.rcParams['xtick.minor.width'] = 1.0  # x轴次刻度线宽度
plt.rcParams['ytick.minor.width'] = 1.0  # y轴次刻度线宽度
plt.rcParams['legend.frameon'] = False  # 图例无边框
plt.rcParams['figure.dpi'] = 300  # 图像分辨率

class TopologicalMagneticStructures:
    # 拓扑磁结构模拟类
    
    def __init__(self, grid_size=100, box_length=200):
        # 初始化模拟参数
        self.grid_size = grid_size
        self.box_length = box_length
        self.x = np.linspace(-box_length/2, box_length/2, grid_size)
        self.y = np.linspace(-box_length/2, box_length/2, grid_size)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        self.r = np.sqrt(self.X**2 + self.Y**2)
        self.theta = np.arctan2(self.Y, self.X)
    
    def generate_anti_skyrmion(self):
        # 生成反斯格明子 (Nsk=1, vorticity=-1, helicity=0)
        # 计算自旋分量
        r0 = 50  # 核心半径
        
        # 反斯格明子的特征：四极对称，中心自旋与外围反向
        n_x = np.cos(2 * self.theta) * (1 - np.exp(-self.r**2 / (2 * r0**2)))
        n_y = -np.sin(2 * self.theta) * (1 - np.exp(-self.r**2 / (2 * r0**2)))
        n_z = np.exp(-self.r**2 / (2 * r0**2)) - 0.5
        
        # 归一化
        norm = np.sqrt(n_x**2 + n_y**2 + n_z**2)
        mask = norm > 1e-10
        n_x[mask] /= norm[mask]
        n_y[mask] /= norm[mask]
        n_z[mask] /= norm[mask]
        
        return n_x, n_y, n_z
    
    def generate_neel_skyrmion(self):
        # 生成奈尔型斯格明子 (Nsk=1, vorticity=1, helicity=0)
        # 计算自旋分量
        r0 = 50  # 核心半径
        
        # 奈尔型斯格明子的特征：径向对称，中心自旋垂直于膜面
        n_x = np.cos(self.theta) * np.sin(np.pi * np.exp(-self.r**2 / (2 * r0**2)))
        n_y = np.sin(self.theta) * np.sin(np.pi * np.exp(-self.r**2 / (2 * r0**2)))
        n_z = np.cos(np.pi * np.exp(-self.r**2 / (2 * r0**2)))
        
        return n_x, n_y, n_z
    
    def generate_neel_bimeron_1(self):
        # 生成奈尔型双半子 (Nsk=1, vorticity=0, helicity=0)
        # 计算自旋分量
        r0 = 50  # 核心半径
        
        # 奈尔型双半子的特征：面内涡旋，无垂直分量
        n_x = np.cos(self.theta) * (1 - np.exp(-self.r**2 / (2 * r0**2)))
        n_y = np.sin(self.theta) * (1 - np.exp(-self.r**2 / (2 * r0**2)))
        n_z = np.zeros_like(self.X)
        
        # 归一化
        norm = np.sqrt(n_x**2 + n_y**2 + n_z**2)
        mask = norm > 1e-10
        n_x[mask] /= norm[mask]
        n_y[mask] /= norm[mask]
        
        return n_x, n_y, n_z
    
    def generate_neel_bimeron_2(self):
        # 生成另一构型的奈尔型双半子 (Nsk=1, vorticity=0, helicity=0，不同手性)
        # 计算自旋分量
        r0 = 50  # 核心半径
        
        # 另一构型的奈尔型双半子：面内涡旋，不同手性
        n_x = -np.cos(self.theta) * (1 - np.exp(-self.r**2 / (2 * r0**2)))
        n_y = -np.sin(self.theta) * (1 - np.exp(-self.r**2 / (2 * r0**2)))
        n_z = np.zeros_like(self.X)
        
        # 归一化
        norm = np.sqrt(n_x**2 + n_y**2 + n_z**2)
        mask = norm > 1e-10
        n_x[mask] /= norm[mask]
        n_y[mask] /= norm[mask]
        
        return n_x, n_y, n_z
    
    def plot_real_space(self, ax, n_x, n_y, n_z, title):
        # 绘制实空间自旋分布
        # 绘制矢量场
        step = 5  # 步长，减少矢量数量
        ax.quiver(self.X[::step, ::step], self.Y[::step, ::step], 
                 n_x[::step, ::step], n_y[::step, ::step], 
                 color='black', alpha=0.6, linewidth=0.5)
        
        # 绘制颜色填充（基于z分量）
        im = ax.imshow(n_z, cmap='RdBu_r', origin='lower', 
                      extent=[-self.box_length/2, self.box_length/2, 
                              -self.box_length/2, self.box_length/2],
                      vmin=-1, vmax=1)
        
        # 设置标题和标签
        ax.set_title(title)
        ax.set_xlabel('x (μm)')
        ax.set_ylabel('y (μm)')
        ax.set_aspect('equal')
        
        return im
    
    def plot_unit_sphere(self, ax, n_x, n_y, n_z, title, highlight_half=False):
        # 绘制单位球面包裹
        # 绘制球体
        circle = patches.Circle((0, 0), 1, fill=False, color='black', linewidth=1.5)
        ax.add_patch(circle)
        
        # 绘制坐标轴
        ax.arrow(0, 0, 1.2, 0, head_width=0.1, head_length=0.1, color='black')
        ax.arrow(0, 0, 0, 1.2, head_width=0.1, head_length=0.1, color='black')
        ax.text(1.3, 0, 'x')
        ax.text(0, 1.3, 'y')
        
        # 绘制几个关键方向的箭头
        # 顶部视图
        for angle in np.linspace(0, 2*np.pi, 8):
            r = 0.8
            x = r * np.cos(angle)
            y = r * np.sin(angle)
            
            # 根据不同结构计算箭头方向
            if 'Anti-skyrmion' in title:
                nx = np.cos(2 * angle)
                ny = -np.sin(2 * angle)
            elif 'Néel-skyrmion' in title:
                nx = np.cos(angle)
                ny = np.sin(angle)
            elif 'bimeron' in title.lower():
                if '1' in title:
                    nx = np.cos(angle)
                    ny = np.sin(angle)
                else:
                    nx = -np.cos(angle)
                    ny = -np.sin(angle)
            else:
                nx = np.cos(angle)
                ny = np.sin(angle)
            
            ax.arrow(x, y, 0.2*nx, 0.2*ny, head_width=0.05, head_length=0.05, color='red')
        
        # 高亮半结构（如果需要）
        if highlight_half:
            # 绘制红框高亮半结构
            rect = patches.Rectangle((-1, -1), 2, 1, linewidth=1, edgecolor='red', facecolor='none', linestyle='--')
            ax.add_patch(rect)
        
        # 设置标题和标签
        ax.set_title(title)
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')
    
    def visualize_all_structures(self, save_path=None):
        # 可视化所有四种拓扑磁结构
        # 创建网格布局
        fig = plt.figure(figsize=(16, 12))
        gs = GridSpec(4, 2, figure=fig)
        
        # 生成四种结构
        structures = [
            (self.generate_anti_skyrmion, "Anti-skyrmion", "(Nsk=1, vorticity=-1, helicity=0)"),
            (self.generate_neel_skyrmion, "Néel-skyrmion", "(Nsk=1, vorticity=1, helicity=0)"),
            (self.generate_neel_bimeron_1, "Néel-bimeron", "(Nsk=1, vorticity=0, helicity=0)"),
            (self.generate_neel_bimeron_2, "Néel-bimeron (another configuration)", "(Nsk=1, vorticity=0, helicity=0)"),
        ]
        
        # 绘制每种结构
        for i, (generator, name, params) in enumerate(structures):
            n_x, n_y, n_z = generator()
            
            # 绘制实空间分布
            ax_real = fig.add_subplot(gs[i, 0])
            im = self.plot_real_space(ax_real, n_x, n_y, n_z, f"{name}\n{params}")
            
            # 绘制单位球面包裹
            ax_sphere = fig.add_subplot(gs[i, 1])
            self.plot_unit_sphere(ax_sphere, n_x, n_y, n_z, "Wrapping to unit sphere", highlight_half=True)
        
        # 添加颜色条
        cbar_ax = fig.add_axes([0.92, 0.1, 0.02, 0.8])
        cbar = fig.colorbar(im, cax=cbar_ax)
        cbar.set_label('n_z (out-of-plane component)')
        
        # 调整布局
        plt.tight_layout(rect=[0, 0, 0.9, 1])
        
        # 保存图像
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"图像已保存到: {save_path}")
        
        # 显示图像
        plt.show()

if __name__ == "__main__":
    """主函数"""
    # 创建模拟实例
    simulator = TopologicalMagneticStructures()
    
    # 可视化所有结构
    save_path = "topological_magnetic_structures.png"
    simulator.visualize_all_structures(save_path)