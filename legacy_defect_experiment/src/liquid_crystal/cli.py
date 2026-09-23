# 命令行接口 - 液晶斯格明子模拟与分析项目

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        prog='liquid-crystal',
        description='液晶斯格明子模拟与分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  liquid-crystal simulate --type skyrmion
  liquid-crystal visualize --input data.npy --output result.png
  liquid-crystal analyze --video video.mp4
  liquid-crystal complete-simulation
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # simulate命令
    simulate_parser = subparsers.add_parser('simulate', help='运行模拟')
    simulate_parser.add_argument(
        '--type', '-t', 
        choices=['skyrmion', 'moire', 'defect'],
        required=True,
        help='模拟类型'
    )
    simulate_parser.add_argument(
        '--output', '-o',
        default='output',
        help='输出目录'
    )
    
    # visualize命令
    visualize_parser = subparsers.add_parser('visualize', help='可视化数据')
    visualize_parser.add_argument(
        '--input', '-i',
        required=True,
        help='输入文件路径'
    )
    visualize_parser.add_argument(
        '--output', '-o',
        required=True,
        help='输出图像路径'
    )
    visualize_parser.add_argument(
        '--dpi', '-d',
        type=int,
        default=300,
        help='图像分辨率'
    )
    
    # analyze命令
    analyze_parser = subparsers.add_parser('analyze', help='分析数据')
    analyze_parser.add_argument(
        '--video', '-v',
        help='视频文件路径'
    )
    analyze_parser.add_argument(
        '--defect', '-d',
        help='缺陷数据文件路径'
    )
    
    # complete-simulation命令
    complete_parser = subparsers.add_parser('complete-simulation', help='运行完整斯格明子模拟')
    complete_parser.add_argument(
        '--output-dir', '-o',
        default=None,
        help='输出目录'
    )
    
    # 参数命令
    params_parser = subparsers.add_parser('params', help='查看或修改参数')
    params_parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='列出所有参数'
    )
    params_parser.add_argument(
        '--set', '-s',
        nargs='+',
        help='设置参数，格式为 key=value'
    )
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    
    if args.command == 'simulate':
        print(f"运行{args.type}模拟...")
        if args.type == 'skyrmion':
            from liquid_crystal.simulation import SkyrmionMorphologies
            skyrmion = SkyrmionMorphologies()
            print("斯格明子形貌生成器已创建")
        elif args.type == 'moire':
            from liquid_crystal.simulation import ContinuousSimulation
            ContinuousSimulation.simulate_moiré_patterns([10, 30, 60])
        elif args.type == 'defect':
            from liquid_crystal.core import LiquidCrystalDefect
            defect = LiquidCrystalDefect()
            print("缺陷生成器已创建")
    
    elif args.command == 'visualize':
        print(f"可视化 {args.input} -> {args.output}")
        # 简化的可视化逻辑
        print("可视化功能即将实现...")
    
    elif args.command == 'analyze':
        if args.video:
            print(f"分析视频: {args.video}")
            try:
                from liquid_crystal.analysis import VideoAnalysis
                va = VideoAnalysis()
                va.analyze_video(args.video)
            except ImportError:
                print("视频分析模块不可用，请安装opencv-python")
        elif args.defect:
            print(f"分析缺陷: {args.defect}")
            from liquid_crystal.analysis import DataAnalysis
            print("缺陷分析功能即将实现...")
    
    elif args.command == 'complete-simulation':
        print("运行完整斯格明子模拟...")
        from liquid_crystal.simulation.skyrmion_complete_simulation import main
        main()
    
    elif args.command == 'params':
        from liquid_crystal import DEFAULT_PARAMS, update_params
        if args.list:
            print("当前参数:")
            for key, value in DEFAULT_PARAMS.items():
                print(f"  {key}: {value}")
        elif args.set:
            new_params = {}
            for param in args.set:
                key, value = param.split('=')
                try:
                    new_params[key] = float(value)
                except ValueError:
                    new_params[key] = value
            update_params(new_params)
            print("参数已更新")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
