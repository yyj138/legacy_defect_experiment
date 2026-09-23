import numpy as np

# 全局参数设置
DEFAULT_PARAMS = {
    'Fi': np.pi / 2,  # 缺陷或粒子的初始相位
    'K': 1,  # 缺陷的类型
    'LClength': 1.1,  # 粒子长度
    'LCinr': 0.2,  # 粒子半径
    'rangex': 8,  # 单个缺陷的x半径范围
    'rangey': 5,  # 单个缺陷的y半径范围
    'd': 0.005,  # 偏移值，避免Arctan函数定义域错误
}

class LiquidCrystalDefect:
    # 向列相液晶拓扑缺陷类
    
    def __init__(self, params=None):
        # 初始化缺陷参数
        self.params = params or DEFAULT_PARAMS
        self.Fi = self.params['Fi']
        self.K = self.params['K']
        self.LClength = self.params['LClength']
        self.LCinr = self.params['LCinr']
        self.rangex = self.params['rangex']
        self.rangey = self.params['rangey']
        self.d = self.params['d']
    
    def create_cylinder(self, x, y, z, length, radius, angle):
        # 创建一个旋转的圆柱体
        # 生成圆柱体的点
        theta = np.linspace(0, 2*np.pi, 10)
        z_cyl = np.linspace(-length/2, length/2, 5)
        theta, z_cyl = np.meshgrid(theta, z_cyl)
        
        # 圆柱体表面点
        x_cyl = radius * np.cos(theta)
        y_cyl = radius * np.sin(theta)
        
        # 旋转圆柱体
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        x_rot = x_cyl * cos_a - y_cyl * sin_a
        y_rot = x_cyl * sin_a + y_cyl * cos_a
        
        # 平移到指定位置
        x_final = x_rot + x
        y_final = y_rot + y
        z_final = z_cyl + z
        
        return x_final, y_final, z_final
    
    def bend(self, k, x1, x2, y1, y2, theta0):
        # 创建弯曲的液晶分子排列
        cylinders = []
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                angle = k * y * (1/6) * np.pi + 0.5 * np.pi + theta0
                x_cyl, y_cyl, z_cyl = self.create_cylinder(
                    x, y, 0, self.LClength, self.LCinr, angle
                )
                cylinders.append((x_cyl, y_cyl, z_cyl))
        return cylinders
    
    def bend1(self, k, x1, x2, y1, y2, theta0):
        # 创建另一种弯曲的液晶分子排列
        cylinders = []
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                angle = k * x * (1/6) * np.pi + np.pi + theta0
                x_cyl, y_cyl, z_cyl = self.create_cylinder(
                    x, y, 0, self.LClength, self.LCinr, angle
                )
                cylinders.append((x_cyl, y_cyl, z_cyl))
        return cylinders
    
    def part_of_r(self, k, x0, y0, theta1, theta2, R, theta0):
        # 创建圆形区域的液晶分子排列
        cylinders = []
        x_min = int(x0 - R - 3)
        x_max = int(x0 + R + 3)
        y_min = int(y0 - R - 3)
        y_max = int(y0 + R + 3)
        
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                # 检查是否在圆环区域内
                dist_sq = (x - x0)**2 + (y - y0)**2
                if (R - 3)**2 <= dist_sq <= (R + 4)**2:
                    # 检查角度范围
                    angle = np.arctan2(y - y0, x - x0 - self.d)
                    if theta1 <= angle <= theta2:
                        # 计算旋转角度
                        dist = np.sqrt(dist_sq)
                        angle_rot = k * (dist - R) * (1/6) * np.pi + theta0
                        x_cyl, y_cyl, z_cyl = self.create_cylinder(
                            x, y, 0, self.LClength, self.LCinr, angle_rot
                        )
                        cylinders.append((x_cyl, y_cyl, z_cyl))
        return cylinders
    
    def create_skyrmion(self):
        # 创建分数斯格明子
        # 上半部分
        cylinders1 = self.part_of_r(-1, 0, 0, np.pi/4, np.pi, 10, 0)
        # 下半部分
        cylinders2 = self.part_of_r(-1, 0, 0, -np.pi, -np.pi/4, 10, 0)
        
        return cylinders1 + cylinders2
    
    def create_bipolaron(self):
        # 创建双极子
        # 左侧部分
        cylinders1 = self.bend(1, -5, 5, -5, 5, 0)
        # 右侧部分
        cylinders2 = self.bend(-1, -5, 5, -5, 5, 0)
        
        return cylinders1 + cylinders2
