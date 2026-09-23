from .core import *
from .simulation import *
from .visualization import *
from .analysis import *
from .utils import *
from .cli import main as cli_main

__version__ = "1.0.0"
__author__ = "Research Team"
__description__ = "液晶斯格明子模拟与分析项目"

# 导出核心类和函数
__all__ = [
    # 核心模块
    'LiquidCrystalDefect',
    'DEFAULT_PARAMS',
    'Patterns',
    
    # 模拟模块
    'SkyrmionMorphologies',
    'TopologicalMagneticStructures',
    'ContinuousSimulation',
    
    # 可视化模块
    'Visualization',
    'SkyrmionVisualizer',
    
    # 分析模块
    'DataAnalysis',
    'VideoAnalysis',
    
    # 工具模块
    'CONFIG',
    'get_config',
    'update_params',
    'get_param',
    'PHYSICAL_CONSTANTS',
    'ProjectConfig',
    
    # CLI
    'cli_main',
]

def main():
    # 运行CLI命令行接口
    cli_main()
