# legacy_defect_experiment — roleB 分支

本分支（`roleB`）包含论文 *Nature Communications 2025, 16:1148* 复现中与**斯格明子形态模拟**相关的代码与结果，主要由 Mathematica（`.nb` / `.m`）脚本构成，配合示例图。

## 目录结构

```
.
├── README.md                  # 项目说明（本文件）
├── czc_exp/                   # Mathematica 斯格明子形态模拟
│   ├── 复现/                  # Mathematica 模块与主程序
│   │   ├── 主程序.nb / 主程序.m
│   │   ├── 加载模块.m
│   │   ├── 可视化模块包.m
│   │   ├── 拓扑缺陷模块包.m
│   │   ├── 数据分析模块包.m
│   │   ├── 液晶排列模式模块包.m
│   │   └── skyrmion.png
│   ├── 四种典型斯格明子形态模拟.nb
│   ├── 不同半径斯格明子的自由能比较.nb
│   ├── 取向角的时间演化.nb
│   ├── 四种斯格明子3d矢量图.png
│   └── 四种液晶斯格明子指向矢排列模拟图/
│       ├── Néel_Skyrmion.png
│       ├── Anti_Skyrmion.png
│       ├── Bimeron.png
│       └── Bimeron_Reverse.png
└── examples/                  # 缺陷可视化示例
    ├── 分数斯格明子.png
    ├── 双极子.png
    ├── C_pattern.png
    ├── R_pattern.png
    ├── Uniform_pattern.png
    └── keyframes/             # 视频关键帧
```

## 内容说明

- **czc_exp/复现/**: Mathematica 主程序与模块包，实现液晶斯格明子形态的数值模拟（Néel 斯格明子、反斯格明子 Anti-Skyrmion、双半子 Bimeron 等）。
- **czc_exp/四种典型斯格明子形态模拟.nb**: 四种典型斯格明子形态的建模与可视化。
- **czc_exp/不同半径斯格明子的自由能比较.nb**: 不同 toron 半径下自由能对比。
- **examples/**: 缺陷结构（分数斯格明子、双极子）与排列模式（C/R/Uniform）的可视化结果图，以及视频关键帧。

## 运行方式

Mathematica 脚本（`.nb` / `.m`）需使用 **Wolfram Mathematica** 打开并运行：

```mathematica
Get["复现/加载模块.m"]   (* 加载模块 *)
Get["复现/主程序.m"]      (* 运行主程序 *)
```

> 注意：本分支为 roleB（成员 B 负责的斯格明子形态模拟部分）；roleA 分支为向列相液晶拓扑缺陷的 Python 仿真主程序。

## License / 说明

本项目仅用于大创课题复现与学术交流，代码基于论文公开信息自行实现，非原作者源码。
