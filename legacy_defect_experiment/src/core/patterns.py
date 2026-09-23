import numpy as np

class Patterns:
    # 液晶排列模式类
    
    def __init__(self, params=None):
        # 初始化参数
        self.params = params or {
            'LClength': 1.5,
            'LCinr': 0.05,
            'rangexOy': 10,
            'rangez': 4,
            'period': 5,
            'A': 5  # 抵抗Uniform排列因子
        }
        self.LClength = self.params['LClength']
        self.LCinr = self.params['LCinr']
        self.rangexOy = self.params['rangexOy']
        self.rangez = self.params['rangez']
        self.period = self.params['period']
        self.A = self.params['A']
        
        # 计算旋转参数
        self.K = 0.5 * np.pi / self.rangez
        self.K2 = np.pi / self.period
        self.K3 = 1 / self.period
        self.Kz = 0.5 / self.rangez
    
    @staticmethod
    def sawtooth(x):
        # 标准斜锯齿函数，含正负
        return x - 2 * np.floor(0.5 * (x + 1))
    
    @staticmethod
    def sawtooth_plus(x):
        # 标准斜锯齿函数，全部正
        return x - np.floor(x)
    
    def create_cylinder(self, x, y, z, length, radius, angle_x, angle_y, angle_z):
        # 创建旋转的圆柱体
        theta = np.linspace(0, 2*np.pi, 10)
        z_cyl = np.linspace(-length/2, length/2, 5)
        theta, z_cyl = np.meshgrid(theta, z_cyl)
        
        x_cyl = radius * np.cos(theta)
        y_cyl = radius * np.sin(theta)
        
        # 绕z轴旋转
        cos_az = np.cos(angle_z)
        sin_az = np.sin(angle_z)
        x_rot = x_cyl * cos_az - y_cyl * sin_az
        y_rot = x_cyl * sin_az + y_cyl * cos_az
        z_rot = z_cyl
        
        # 绕y轴旋转
        cos_ay = np.cos(angle_y)
        sin_ay = np.sin(angle_y)
        x_rot2 = x_rot * cos_ay + z_rot * sin_ay
        y_rot2 = y_rot
        z_rot2 = -x_rot * sin_ay + z_rot * cos_ay
        
        # 绕x轴旋转
        cos_ax = np.cos(angle_x)
        sin_ax = np.sin(angle_x)
        x_final = x_rot2
        y_final = y_rot2 * cos_ax - z_rot2 * sin_ax
        z_final = y_rot2 * sin_ax + z_rot2 * cos_ax
        
        # 平移
        x_final += x
        y_final += y
        z_final += z
        
        return x_final, y_final, z_final
    
    def r_pattern(self, x, y, z):
        """R pattern - 径向模式"""
        r = np.sqrt(x**2 + y**2)
        
        # xOz平面绕y轴旋转
        angle_y = self.K * z * self.sawtooth(self.K3 * r)
        
        # yOz平面绕x轴旋转
        angle_x = self.K2 * z * self.sawtooth(self.K3 * r)
        
        # z轴旋转
        angle_z = np.arctan2(y, x)
        
        return angle_x, angle_y, angle_z
    
    def c_pattern(self, x, y, z):
        # C pattern - 圆周模式
        r = np.sqrt(x**2 + y**2)
        
        # xOz平面绕y轴旋转
        angle_y = self.K * z * self.sawtooth_plus(self.K3 * r)
        
        # yOz平面绕x轴旋转
        angle_x = self.K2 * z * self.sawtooth_plus(self.K3 * r)
        
        # z轴旋转
        angle_z = np.arctan2(y, x) + np.pi/2
        
        return angle_x, angle_y, angle_z
    
    def uniform_pattern(self, x, y, z):
        # Uniform pattern - 均匀排列
        # 均匀排列，所有分子朝同一方向
        angle_x = 0
        angle_y = 0
        angle_z = 0
        
        return angle_x, angle_y, angle_z
    
    def generate_pattern(self, pattern_type='r', x_range=None, y_range=None, z_range=None):
        # 生成指定的pattern
        if x_range is None:
            x_range = range(-self.rangexOy, self.rangexOy + 1)
        if y_range is None:
            y_range = range(-self.rangexOy, self.rangexOy + 1)
        if z_range is None:
            z_range = range(-self.rangez, self.rangez + 1)
        
        cylinders = []
        
        for x in x_range:
            for y in y_range:
                for z in z_range:
                    if pattern_type == 'r':
                        angle_x, angle_y, angle_z = self.r_pattern(x, y, z)
                    elif pattern_type == 'c':
                        angle_x, angle_y, angle_z = self.c_pattern(x, y, z)
                    elif pattern_type == 'uniform':
                        angle_x, angle_y, angle_z = self.uniform_pattern(x, y, z)
                    else:
                        raise ValueError(f"Unknown pattern type: {pattern_type}")
                    
                    # 添加抵抗Uniform排列的影响
                    if pattern_type != 'uniform':
                        uniform_x, uniform_y, uniform_z = self.uniform_pattern(x, y, z)
                        angle_x = (angle_x + self.A * uniform_x) / (1 + self.A)
                        angle_y = (angle_y + self.A * uniform_y) / (1 + self.A)
                        angle_z = (angle_z + self.A * uniform_z) / (1 + self.A)
                    
                    x_cyl, y_cyl, z_cyl = self.create_cylinder(
                        x, y, z, self.LClength, self.LCinr, 
                        angle_x, angle_y, angle_z
                    )
                    cylinders.append((x_cyl, y_cyl, z_cyl))
        
        return cylinders
