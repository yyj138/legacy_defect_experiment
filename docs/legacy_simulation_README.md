# 向列相液晶拓扑缺陷实验复现

本项目用于复现论文 *Nature Communications, 2025, 16:1148* 中的向列相液晶拓扑缺陷实验。

## 项目结构

```
.
├── README.md                     # 项目说明（仓库根目录）
├── main.py                       # 主脚本（交互式操作，15项功能菜单）
├── src/                          # 源代码目录
│   ├── core/                     # 核心模块
│   │   ├── defects.py            # 缺陷生成（分数斯格明子、双极子）
│   │   └── patterns.py           # 液晶排列模式（R/C/Uniform）
│   ├── simulation/               # 模拟模块
│   │   ├── continuous_simulation.py           # 连续介质模拟
│   │   ├── skyrmion_complete_simulation.py    # 完整斯格明子模拟
│   │   ├── skyrmion_morphologies.py           # 四种斯格明子形貌对比
│   │   └── topological_magnetic_structures.py # 拓扑磁性结构
│   ├── analysis/                 # 数据分析模块
│   │   ├── data_analysis.py      # 缺陷结构分析
│   │   └── video_analysis.py     # 视频分析
│   ├── visualization/            # 可视化模块
│   │   ├── visualization.py      # 缺陷可视化
│   │   └── skyrmion_visualization.py  # 斯格明子可视化
│   └── liquid_crystal/           # 液晶主模块（工具/CLI）
├── examples/                     # 输出示例和结果
│   ├── *.png                     # 各种缺陷可视化结果
│   ├── continuous_simulation/    # 连续介质模拟结果（Fig1-Fig10）
│   └── keyframes/                # 视频关键帧（video_1/ ... video_11/）
├── videos/                       # 实验视频（视频1.mp4 - 视频11.mp4）
└── docs/                         # 文档目录
    ├── legacy_simulation_README.md  # 本文件
    └── debug.log                 # 调试日志
```

## 环境要求

- Python 3.8+
- NumPy
- Matplotlib
- SciPy
- OpenCV (用于视频分析)

## 安装依赖

```bash
pip install numpy matplotlib scipy opencv-python
```

## 功能说明

运行 `main.py` 后可选择以下15项功能：

| 序号 | 功能 | 说明 |
|------|------|------|
| 1 | 生成分数斯格明子 | 生成并可视化分数斯格明子结构 |
| 2 | 生成双极子 | 生成并可视化双极子结构 |
| 3 | 生成R pattern | 生成径向排列模式 |
| 4 | 生成C pattern | 生成圆周排列模式 |
| 5 | 生成Uniform pattern | 生成均匀排列模式 |
| 6 | 生成R pattern 2D网格 | R pattern的二维网格可视化 |
| 7 | 生成C pattern 2D网格 | C pattern的二维网格可视化 |
| 8 | 生成Uniform pattern 2D网格 | Uniform pattern的二维网格可视化 |
| 9 | 连续介质模拟 | 莫尔条纹和斯格明子形成模拟 |
| 10 | 完整斯格明子模拟 | 生成所有10张实验图（Fig1-Fig10） |
| 11 | 四种斯格明子形貌对比 | HAS/HNS/HNB+/HNB- 对比 |
| 12 | 调整参数 | 调整模拟参数 |
| 13 | 分析缺陷结构 | 拓扑分析、能量计算 |
| 14 | 视频分析 | 提取关键帧和运动特征 |
| 15 | 退出 | 退出程序 |

## 运行方式

### 主脚本（推荐）

```bash
python main.py
```

启动交互式界面后，输入数字选择功能即可。

### 输出文件位置

所有生成的图片保存在 `examples/` 目录下：
- 基础可视化：`examples/*.png`
- 连续介质模拟：`examples/continuous_simulation/`
- 视频关键帧：`examples/keyframes/video_N/`

## 核心模块说明

### src/core/
- **defects.py**: 生成拓扑缺陷（分数斯格明子、双极子）
- **patterns.py**: 实现R/C/Uniform三种排列模式

### src/simulation/
- **continuous_simulation.py**: 莫尔条纹和斯格明子模拟
- **skyrmion_complete_simulation.py**: 完整的10张斯格明子相关图表生成
- **skyrmion_morphologies.py**: 四种斯格明子形貌对比可视化
- **topological_magnetic_structures.py**: 拓扑磁性结构模拟

### src/analysis/
- **data_analysis.py**: 拓扑分析、能量计算、结构特征提取
- **video_analysis.py**: 视频关键帧提取、运动特征分析

### src/visualization/
- **visualization.py**: 缺陷结构可视化与保存
- **skyrmion_visualization.py**: 斯格明子专用可视化

## 实验复现步骤

1. 运行 `python main.py`
2. 选择功能1-5生成基础缺陷结构
3. 选择功能9-11运行完整模拟
4. 使用功能12调整参数观察变化
5. 使用功能13分析缺陷性质
6. 使用功能14分析实验视频
7. 结果保存在 `examples/` 目录

## 参考资料

- **论文**: Nature Communications, 2025, 16:1148
- **视频数据**: `videos/` 目录（视频1.mp4 - 视频11.mp4）

## 生成的图表

| 图表 | 文件名 | 说明 |
|------|--------|------|
| Fig1 | Fig1_2d_director_fields.png | 2D指向矢场示意图 |
| Fig2 | Fig2_3d_director_fields.png | 3D指向矢场 |
| Fig3 | Fig3_HAS_cross_sections.png | HAS三切面图 |
| Fig4 | Fig4_HNS_cross_sections.png | HNS三切面图 |
| Fig5 | Fig5_HNB+_cross_sections.png | HNB+三切面图 |
| Fig6 | Fig6_HNB-_cross_sections.png | HNB-三切面图 |
| Fig7 | Fig7_interaction_potential.png | 相互作用势曲线 |
| Fig8 | Fig8_colloid_dynamics.png | 胶体动力学轨迹 |
| Fig9 | Fig9_energy_transition.png | 自由能景观与拓扑转变 |
| Fig10 | Fig10_parameters_table.png | 参数汇总表 |
