# legacy_defect_experiment — roleB 分支

本分支（`roleB`）包含论文 *Nature Communications 2025, 16:1148* 复现中与**斯格明子形态模拟**相关的代码与结果，主要由 Mathematica（`.nb` / `.m`）脚本构成，配合结果图与缺陷可视化示例。

## 目录结构

```
.
├── README.md                  # 项目说明（本文件）
├── src/                       # Mathematica 脚本代码
│   ├── skyrmion_simulation/   # 斯格明子主程序与模块包（内部保持同目录相对引用）
│   │   ├── 主程序.nb / 主程序.m
│   │   ├── 加载模块.m
│   │   ├── 拓扑缺陷模块包.m
│   │   ├── 液晶排列模式模块包.m
│   │   ├── 可视化模块包.m
│   │   ├── 数据分析模块包.m
│   │   └── skyrmion.png
│   ├── 四种典型斯格明子形态模拟.nb
│   ├── 不同半斯格明子的自由能比较.nb
│   └── 胶体取向角的时间近似演化.nb
├── figures/                   # 斯格明子形态结果图
│   ├── 四种液晶斯格明子指向矢排列模拟图/
│   │   ├── Néel_Skyrmion.png
│   │   ├── Anti_Skyrmion.png
│   │   ├── Bimeron.png
│   │   └── Bimeron_Reverse.png
│   └── 四种斯格明子3d矢量图.png
└── examples/                  # 缺陷可视化示例
    ├── 分数斯格明子.png
    ├── 双极子.png
    ├── C_pattern.png
    ├── R_pattern.png
    ├── Uniform_pattern.png
    └── keyframes/             # 视频关键帧
```

## 内容说明

- **src/skyrmion_simulation/**: Mathematica 主程序与模块包，实现液晶斯格明子形态的数值模拟（Néel 斯格明子、反斯格明子 Anti-Skyrmion、双半子 Bimeron 等）。六个 `.m` 模块包位于同一目录，`加载模块.m` 通过 `Get[...]` 相对引用同目录模块。
- **src/四种典型斯格明子形态模拟.nb**: 四种典型斯格明子形态的建模与可视化。
- **src/不同半斯格明子的自由能比较.nb**: 不同半径下斯格明子自由能对比。
- **src/胶体取向角的时间近似演化.nb**: 胶体取向角随时间演化的近似模拟。
- **figures/**: 斯格明子形态结果图（Néel / Anti-Skyrmion / Bimeron / Bimeron_Reverse 指向矢排列模拟图及 3D 矢量图）。
- **examples/**: 缺陷结构（分数斯格明子、双极子）与排列模式（C/R/Uniform）的可视化结果图，以及视频关键帧。

## 运行方式

Mathematica 脚本（`.nb` / `.m`）需使用 **Wolfram Mathematica** 打开并运行：

```mathematica
(* 打开 src/skyrmion_simulation/主程序.nb，或在工作目录内加载模块 *)
Get["skyrmion_simulation/加载模块.m"]   (* 加载模块（需在 src/ 目录下） *)
Get["skyrmion_simulation/主程序.m"]      (* 运行主程序 *)
```

> 注意：`.m` 模块包间的 `Get[...]` 引用为同目录相对引用，请在 `src/` 目录下运行，保持 `src/skyrmion_simulation/` 内部结构不变。

## 分支说明

- `roleB`：斯格明子形态模拟（Mathematica）与可视化示例（本分支）
- `roleA`：向列相液晶拓扑缺陷的 Python 仿真主程序（main.py / src / examples / videos / docs）

## License / 说明

本项目仅用于大创课题复现与学术交流，代码基于论文公开信息自行实现，非原作者源码。
