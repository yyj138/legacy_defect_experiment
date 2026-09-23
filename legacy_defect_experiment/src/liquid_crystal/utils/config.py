# 配置模块 - 管理项目全局配置参数

import os
from dataclasses import dataclass
from typing import Dict, Any

# 默认参数配置
DEFAULT_PARAMS = {
    'Fi': 1.5708,  # π/2, 缺陷或粒子的初始相位
    'K': 1,  # 缺陷的类型
    'LClength': 1.1,  # 粒子长度
    'LCinr': 0.2,  # 粒子半径
    'rangex': 8,  # 单个缺陷的x半径范围
    'rangey': 5,  # 单个缺陷的y半径范围
    'd': 0.005,  # 偏移值，避免Arctan函数定义域错误
}

# 物理常数配置
PHYSICAL_CONSTANTS = {
    'K1': 6.0,  # splay弹性常数 (pN)
    'K2': 3.9,  # twist弹性常数 (pN)
    'K3': 6.8,  # bend弹性常数 (pN)
    'L': 100,   # 展曲-弯曲图案周期 (μm)
    'H': 50,    # 液晶盒厚度 (μm)
    'r': 2.5,   # 胶体半径 (μm)
}

@dataclass
class ProjectConfig:
    # 项目配置类
    project_name: str = "liquid_crystal_experiment"
    version: str = "1.0.0"
    author: str = "Research Team"
    description: str = "液晶斯格明子模拟与分析项目"
    
    # 路径配置
    base_dir: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir: str = os.path.join(base_dir, "data")
    output_dir: str = os.path.join(base_dir, "outputs")
    figures_dir: str = os.path.join(output_dir, "figures")
    videos_dir: str = os.path.join(output_dir, "videos")
    examples_dir: str = os.path.join(base_dir, "examples")
    
    # 可视化配置
    dpi: int = 300
    font_family: str = "serif"
    font_size: int = 12
    axes_linewidth: float = 1.5
    
    def __post_init__(self):
        # 初始化后创建必要的目录
        for dir_path in [self.data_dir, self.output_dir, self.figures_dir, self.videos_dir]:
            os.makedirs(dir_path, exist_ok=True)
    
    def get_output_path(self, filename: str, subdir: str = "figures") -> str:
        # 获取输出文件路径
        if subdir == "figures":
            return os.path.join(self.figures_dir, filename)
        elif subdir == "videos":
            return os.path.join(self.videos_dir, filename)
        else:
            return os.path.join(self.output_dir, filename)

# 全局配置实例
CONFIG = ProjectConfig()

def get_config() -> ProjectConfig:
    # 获取全局配置
    return CONFIG

def update_params(new_params: Dict[str, Any]) -> None:
    # 更新默认参数
    DEFAULT_PARAMS.update(new_params)

def get_param(key: str, default=None):
    # 获取参数值
    return DEFAULT_PARAMS.get(key, default)
