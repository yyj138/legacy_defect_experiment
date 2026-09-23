import numpy as np

class DataAnalysis:
    #数据分析模块
    
    @staticmethod
    def analyze_topology(cylinders):
        #分析缺陷的拓扑性质
        # 计算缺陷的拓扑电荷
        topology_charge = 0
        
        # 统计圆柱体数量作为复杂度指标
        complexity = len(cylinders)
        
        return {
            'topology_charge': topology_charge,
            'complexity': complexity
        }
    
    @staticmethod
    def calculate_energy(cylinders, k1=1, k2=1, k3=1):
        # 计算缺陷的能量
        # k1, k2, k3 是弹性常数
        
        # 计算总能量
        total_energy = 0
        
        # 遍历所有圆柱体，计算能量贡献
        for i, (x1, y1, z1) in enumerate(cylinders):
            # 计算与其他圆柱体的相互作用能量
            for j, (x2, y2, z2) in enumerate(cylinders):
                if i != j:
                    # 计算距离
                    dist = np.sqrt(
                        (x1.mean() - x2.mean())**2 + 
                        (y1.mean() - y2.mean())**2 + 
                        (z1.mean() - z2.mean())**2
                    )
                    # 简单的相互作用能量模型
                    if dist > 0:
                        total_energy += 1 / dist
        
        # 添加弯曲能量
        bend_energy = len(cylinders) * 0.1
        total_energy += bend_energy
        
        return {
            'total_energy': total_energy,
            'bend_energy': bend_energy
        }
    
    @staticmethod
    def analyze_defect_structure(cylinders):
        # 分析缺陷的结构特征
        # 计算缺陷的中心位置
        x_coords = [cyl[0].mean() for cyl in cylinders]
        y_coords = [cyl[1].mean() for cyl in cylinders]
        z_coords = [cyl[2].mean() for cyl in cylinders]
        
        center = {
            'x': np.mean(x_coords),
            'y': np.mean(y_coords),
            'z': np.mean(z_coords)
        }
        
        # 计算缺陷的大小
        size = {
            'x_range': max(x_coords) - min(x_coords),
            'y_range': max(y_coords) - min(y_coords),
            'z_range': max(z_coords) - min(z_coords)
        }
        
        return {
            'center': center,
            'size': size,
            'num_molecules': len(cylinders)
        }
