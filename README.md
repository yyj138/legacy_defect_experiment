# legacy_defect_experiment

复现论文 *Nature Communications 2025, 16:1148* 向列相液晶拓扑缺陷（分数斯格明子、双极子）实验，含连续介质模拟、缺陷生成、可视化与视频关键帧，以及基于 Mathematica 的斯格明子形态模拟。

本项目为两套互补的复现方案：
- **Python 仿真**（`main.py` / `src/`）：连续介质模拟、缺陷生成、可视化与视频分析
- **Mathematica 模拟**（`src/skyrmion_simulation/`）：斯格明子形态的数值模拟与结果图

## 目录结构

```
.
├── README.md                  # 项目说明（本文件）
├── main.py                    # Python 主脚本（交互式操作，15项功能菜单）
├── src/                       # 源代码目录
│   ├── core/                  # 核心模块
│   │   ├── defects.py         # 缺陷生成（分数斯格明子、双极子）
│   │   └── patterns.py        # 液晶排列模式（R/C/Uniform）
│   ├── simulation/            # 模拟模块
│   │   ├── continuous_simulation.py           # 连续介质模拟
│   │   ├── skyrmion_complete_simulation.py    # 完整斯格明子模拟
│   │   ├── skyrmion_morphologies.py           # 四种斯格明子形貌对比
│   │   └── topological_magnetic_structures.py # 拓扑磁性结构
│   ├── analysis/              # 数据分析模块
│   │   ├── data_analysis.py   # 缺陷结构分析
│   │   └── video_analysis.py  # 视频分析
│   ├── visualization/         # 可视化模块
│   │   ├── visualization.py   # 缺陷可视化
│   │   └── skyrmion_visualization.py  # 斯格明子可视化
│   ├── liquid_crystal/        # 液晶主模块（工具/CLI）
│   └── skyrmion_simulation/   # Mathematica 斯格明子主程序与模块包
│       ├── 主程序.nb / 主程序.m
│       ├── 加载模块.m
│       ├── 拓扑缺陷模块包.m
│       ├── 液晶排列模式模块包.m
│       ├── 可视化模块包.m
│       ├── 数据分析模块包.m
│       └── skyrmion.png
│   ├── 四种典型斯格明子形态模拟.nb
│   ├── 不同半斯格明子的自由能比较.nb
│   └── 胶体取向角的时间近似演化.nb
├── figures/                   # 斯格明子形态结果图（Mathematica 输出）
│   ├── 四种液晶斯格明子指向矢排列模拟图/
│   │   ├── Néel_Skyrmion.png
│   │   ├── Anti_Skyrmion.png
│   │   ├── Bimeron.png
│   │   └── Bimeron_Reverse.png
│   └── 四种斯格明子3d矢量图.png
├── examples/                  # 输出示例和结果
│   ├── 分数斯格明子.png / 双极子.png
│   ├── C_pattern.png / R_pattern.png / Uniform_pattern.png
│   ├── *.png                  # 各种缺陷可视化结果
│   ├── continuous_simulation/ # 连续介质模拟结果（Fig1-Fig10）
│   └── keyframes/             # 视频关键帧（video_1/ ... video_11/）
├── videos/                    # 实验视频（视频1.mp4 - 视频11.mp4）
└── docs/                      # 文档
    ├── legacy_simulation_README.md  # 详细说明
    └── debug.log              # 调试日志
```

## Python 仿真（main.py）

### 环境要求

- Python 3.8+
- NumPy
- Matplotlib
- SciPy
- OpenCV (用于视频分析)

### 安装依赖

```bash
pip install numpy matplotlib scipy opencv-python
```

### 快速开始

```bash
# 启动交互式界面（在仓库根目录运行）
python main.py
```

> 注意：`main.py` 通过 `os.path.dirname(__file__)` 定位 `src/examples/videos`，请在仓库根目录运行。

### 功能说明

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

### 输出文件位置

所有生成的图片保存在 `examples/` 目录下：
- 基础可视化：`examples/*.png`
- 连续介质模拟：`examples/continuous_simulation/`
- 视频关键帧：`examples/keyframes/video_N/`

### 实验复现步骤

1. 运行 `python main.py`
2. 选择功能1-5生成基础缺陷结构
3. 选择功能9-11运行完整模拟
4. 使用功能12调整参数观察变化
5. 使用功能13分析缺陷性质
6. 使用功能14分析实验视频
7. 结果保存在 `examples/` 目录

## Mathematica 斯格明子模拟（src/skyrmion_simulation/）

实现液晶斯格明子形态的数值模拟（Néel 斯格明子、反斯格明子 Anti-Skyrmion、双半子 Bimeron 等），六个 `.m` 模块包位于同一目录，`加载模块.m` 通过 `Get[...]` 相对引用同目录模块。

### 运行方式

Mathematica 脚本（`.nb` / `.m`）需使用 **Wolfram Mathematica** 打开并运行：

```mathematica
(* 打开 src/skyrmion_simulation/主程序.nb，或在工作目录内加载模块 *)
Get["skyrmion_simulation/加载模块.m"]   (* 加载模块（需在 src/ 目录下） *)
Get["skyrmion_simulation/主程序.m"]      (* 运行主程序 *)
```

> 注意：`.m` 模块包间的 `Get[...]` 引用为同目录相对引用，请在 `src/` 目录下运行，保持 `src/skyrmion_simulation/` 内部结构不变。

### 内容说明

- **src/skyrmion_simulation/**: Mathematica 主程序与模块包，实现液晶斯格明子形态的数值模拟。
- **src/四种典型斯格明子形态模拟.nb**: 四种典型斯格明子形态的建模与可视化。
- **src/不同半斯格明子的自由能比较.nb**: 不同半径下斯格明子自由能对比。
- **src/胶体取向角的时间近似演化.nb**: 胶体取向角随时间演化的近似模拟。
- **figures/**: 斯格明子形态结果图（Néel / Anti-Skyrmion / Bimeron / Bimeron_Reverse 指向矢排列模拟图及 3D 矢量图）。

## 参考资料

- **论文**: Nature Communications, 2025, 16:1148
- **视频数据**: `videos/` 目录（视频1.mp4 - 视频11.mp4）
- 详细说明见 [docs/legacy_simulation_README.md](docs/legacy_simulation_README.md)

## 分支说明

- `roleA`：向列相液晶拓扑缺陷的 Python 仿真主程序（main.py / src / examples / videos / docs）
- `roleB`：斯格明子形态模拟（Mathematica）与可视化示例（src/skyrmion_simulation / figures）
- `main`：合并后的默认分支（包含 roleA + roleB 全部内容）

## License / 说明

本项目仅用于大创课题复现与学术交流，代码基于论文公开信息自行实现，非原作者源码。
