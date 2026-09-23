# 主入口文件 - 向列相液晶拓扑缺陷实验复现
# 基于论文 Nature Communications, 2025, 16:1148

import sys
import os
import subprocess

# 添加src目录到Python路径
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

# 设置输出目录
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'examples')
os.makedirs(OUTPUT_DIR, exist_ok=True)

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

from core.defects import LiquidCrystalDefect, DEFAULT_PARAMS
from core.patterns import Patterns
from visualization.visualization import Visualization
from analysis.data_analysis import DataAnalysis

try:
    from analysis.video_analysis import VideoAnalysis
    VIDEO_ANALYSIS_AVAILABLE = True
except ImportError:
    VIDEO_ANALYSIS_AVAILABLE = False
    print("警告: 视频分析模块不可用，请安装opencv-python")

class Main:
    # 主脚本类

    @staticmethod
    def display_menu():
        # 显示菜单
        print("=" * 70)
        print("向列相液晶拓扑缺陷实验复现")
        print("=" * 70)
        print("1. 生成分数斯格明子")
        print("2. 生成双极子")
        print("3. 生成R pattern")
        print("4. 生成C pattern")
        print("5. 生成Uniform pattern")
        print("6. 生成R pattern 2D网格")
        print("7. 生成C pattern 2D网格")
        print("8. 生成Uniform pattern 2D网格")
        print("9. 连续介质模拟（莫尔条纹和斯格明子）")
        print("10. 完整斯格明子模拟（生成所有图）")
        print("11. 四种斯格明子形貌对比")
        print("12. 调整参数")
        print("13. 分析缺陷结构")
        print("14. 视频分析")
        print("15. 退出")
        print("=" * 70)

    @staticmethod
    def adjust_parameters():
        # 调整参数
        print("当前参数:")
        for key, value in DEFAULT_PARAMS.items():
            print(f"  {key}: {value}")

        print("\n输入要修改的参数，或按Enter保持默认:")

        new_params = DEFAULT_PARAMS.copy()

        for key in DEFAULT_PARAMS:
            user_input = input(f"{key} [{DEFAULT_PARAMS[key]}]: ")
            if user_input:
                try:
                    if isinstance(DEFAULT_PARAMS[key], float):
                        new_params[key] = float(user_input)
                    elif isinstance(DEFAULT_PARAMS[key], int):
                        new_params[key] = int(user_input)
                except ValueError:
                    print(f"无效输入，保持默认值 {DEFAULT_PARAMS[key]}")

        return new_params

    @staticmethod
    def run():
        # 运行主程序
        params = DEFAULT_PARAMS

        try:
            while True:
                Main.display_menu()
                choice = input("请选择操作 (1-15): ").strip()
                choice = ''.join([c for c in choice if c.isdigit()])
                if not choice:
                    print("无效输入，请输入 1-15 之间的数字")
                    continue

                if choice == "1":
                    while True:
                        print("生成分数斯格明子...")
                        lc_defect = LiquidCrystalDefect(params)
                        skyrmion = lc_defect.create_skyrmion()
                        Visualization.save_visualization(skyrmion, "分数斯格明子", OUTPUT_DIR)

                        analysis = DataAnalysis.analyze_defect_structure(skyrmion)
                        print("\n缺陷结构分析:")
                        print(f"中心位置: ({analysis['center']['x']:.2f}, {analysis['center']['y']:.2f}, {analysis['center']['z']:.2f})")
                        print(f"大小范围: X={analysis['size']['x_range']:.2f}, Y={analysis['size']['y_range']:.2f}, Z={analysis['size']['z_range']:.2f}")
                        print(f"分子数量: {analysis['num_molecules']}")

                        next_action = input("\n1. 再次生成分数斯格明子\n2. 返回主菜单\n请选择: ")
                        if next_action != "1":
                            break

                elif choice == "2":
                    while True:
                        print("生成双极子...")
                        lc_defect = LiquidCrystalDefect(params)
                        bipolaron = lc_defect.create_bipolaron()
                        Visualization.save_visualization(bipolaron, "双极子", OUTPUT_DIR)

                        analysis = DataAnalysis.analyze_defect_structure(bipolaron)
                        print("\n缺陷结构分析:")
                        print(f"中心位置: ({analysis['center']['x']:.2f}, {analysis['center']['y']:.2f}, {analysis['center']['z']:.2f})")
                        print(f"大小范围: X={analysis['size']['x_range']:.2f}, Y={analysis['size']['y_range']:.2f}, Z={analysis['size']['z_range']:.2f}")
                        print(f"分子数量: {analysis['num_molecules']}")

                        next_action = input("\n1. 再次生成双极子\n2. 返回主菜单\n请选择: ")
                        if next_action != "1":
                            break

                elif choice == "3":
                    while True:
                        print("生成R pattern...")
                        patterns = Patterns()
                        r_pattern = patterns.generate_pattern('r')
                        Visualization.save_visualization(r_pattern, "R_pattern", OUTPUT_DIR)

                        analysis = DataAnalysis.analyze_defect_structure(r_pattern)
                        print("\nR pattern结构分析:")
                        print(f"中心位置: ({analysis['center']['x']:.2f}, {analysis['center']['y']:.2f}, {analysis['center']['z']:.2f})")
                        print(f"大小范围: X={analysis['size']['x_range']:.2f}, Y={analysis['size']['y_range']:.2f}, Z={analysis['size']['z_range']:.2f}")
                        print(f"分子数量: {analysis['num_molecules']}")

                        next_action = input("\n1. 再次生成R pattern\n2. 返回主菜单\n请选择: ")
                        if next_action != "1":
                            break

                elif choice == "4":
                    while True:
                        print("生成C pattern...")
                        patterns = Patterns()
                        c_pattern = patterns.generate_pattern('c')
                        Visualization.save_visualization(c_pattern, "C_pattern", OUTPUT_DIR)

                        analysis = DataAnalysis.analyze_defect_structure(c_pattern)
                        print("\nC pattern结构分析:")
                        print(f"中心位置: ({analysis['center']['x']:.2f}, {analysis['center']['y']:.2f}, {analysis['center']['z']:.2f})")
                        print(f"大小范围: X={analysis['size']['x_range']:.2f}, Y={analysis['size']['y_range']:.2f}, Z={analysis['size']['z_range']:.2f}")
                        print(f"分子数量: {analysis['num_molecules']}")

                        next_action = input("\n1. 再次生成C pattern\n2. 返回主菜单\n请选择: ")
                        if next_action != "1":
                            break

                elif choice == "5":
                    while True:
                        print("生成Uniform pattern...")
                        patterns = Patterns()
                        uniform_pattern = patterns.generate_pattern('uniform')
                        Visualization.save_visualization(uniform_pattern, "Uniform_pattern", OUTPUT_DIR)

                        analysis = DataAnalysis.analyze_defect_structure(uniform_pattern)
                        print("\nUniform pattern结构分析:")
                        print(f"中心位置: ({analysis['center']['x']:.2f}, {analysis['center']['y']:.2f}, {analysis['center']['z']:.2f})")
                        print(f"大小范围: X={analysis['size']['x_range']:.2f}, Y={analysis['size']['y_range']:.2f}, Z={analysis['size']['z_range']:.2f}")
                        print(f"分子数量: {analysis['num_molecules']}")

                        next_action = input("\n1. 再次生成Uniform pattern\n2. 返回主菜单\n请选择: ")
                        if next_action != "1":
                            break

                elif choice == "6":
                    while True:
                        print("生成R pattern 2D网格...")
                        Visualization.save_2d_grid_visualization('r', "R_pattern_2D", OUTPUT_DIR)
                        print("R pattern 2D网格已保存")

                        next_action = input("\n1. 再次生成R pattern 2D网格\n2. 返回主菜单\n请选择: ")
                        if next_action != "1":
                            break

                elif choice == "7":
                    while True:
                        print("生成C pattern 2D网格...")
                        Visualization.save_2d_grid_visualization('c', "C_pattern_2D", OUTPUT_DIR)
                        print("C pattern 2D网格已保存")

                        next_action = input("\n1. 再次生成C pattern 2D网格\n2. 返回主菜单\n请选择: ")
                        if next_action != "1":
                            break

                elif choice == "8":
                    while True:
                        print("生成Uniform pattern 2D网格...")
                        Visualization.save_2d_grid_visualization('uniform', "Uniform_pattern_2D", OUTPUT_DIR)
                        print("Uniform pattern 2D网格已保存")

                        next_action = input("\n1. 再次生成Uniform pattern 2D网格\n2. 返回主菜单\n请选择: ")
                        if next_action != "1":
                            break

                elif choice == "9":
                    from simulation.continuous_simulation import ContinuousSimulation
                    while True:
                        print("运行连续介质模拟...")
                        thicknesses = [10, 30, 60]
                        ContinuousSimulation.simulate_moiré_patterns(thicknesses)
                        print("连续介质模拟完成！")

                        next_action = input("\n1. 再次运行连续介质模拟\n2. 返回主菜单\n请选择: ")
                        if next_action != "1":
                            break

                elif choice == "10":
                    while True:
                        print("运行完整斯格明子模拟...")
                        sim_path = os.path.join(src_path, 'simulation', 'skyrmion_complete_simulation.py')
                        subprocess.run([sys.executable, sim_path], cwd=os.path.dirname(__file__))
                        print("完整斯格明子模拟完成！")

                        next_action = input("\n1. 再次运行完整斯格明子模拟\n2. 返回主菜单\n请选择: ")
                        if next_action != "1":
                            break

                elif choice == "11":
                    from simulation.skyrmion_morphologies import SkyrmionMorphologies
                    while True:
                        print("四种斯格明子形貌对比...")
                        sim = SkyrmionMorphologies()
                        sim.visualize_all_morphologies()
                        print("四种斯格明子形貌对比完成！")

                        next_action = input("\n1. 再次生成四种斯格明子形貌对比\n2. 返回主菜单\n请选择: ")
                        if next_action != "1":
                            break

                elif choice == "12":
                    while True:
                        params = Main.adjust_parameters()
                        print("参数已更新")

                        next_action = input("\n1. 再次调整参数\n2. 返回主菜单\n请选择: ")
                        if next_action != "1":
                            break

                elif choice == "13":
                    while True:
                        print("选择要分析的缺陷类型:")
                        print("1. 分数斯格明子")
                        print("2. 双极子")
                        print("3. R pattern")
                        print("4. C pattern")
                        print("5. Uniform pattern")
                        defect_choice = input("请选择 (1-5): ")

                        if defect_choice == "1":
                            lc_defect = LiquidCrystalDefect(params)
                            defect = lc_defect.create_skyrmion()
                            defect_name = "分数斯格明子"
                        elif defect_choice == "2":
                            lc_defect = LiquidCrystalDefect(params)
                            defect = lc_defect.create_bipolaron()
                            defect_name = "双极子"
                        elif defect_choice == "3":
                            patterns = Patterns()
                            defect = patterns.generate_pattern('r')
                            defect_name = "R pattern"
                        elif defect_choice == "4":
                            patterns = Patterns()
                            defect = patterns.generate_pattern('c')
                            defect_name = "C pattern"
                        elif defect_choice == "5":
                            patterns = Patterns()
                            defect = patterns.generate_pattern('uniform')
                            defect_name = "Uniform pattern"
                        else:
                            print("无效选择")
                            continue

                        topology = DataAnalysis.analyze_topology(defect)
                        print(f"\n{defect_name}拓扑分析:")
                        print(f"拓扑电荷: {topology['topology_charge']}")
                        print(f"复杂度: {topology['complexity']}")

                        energy = DataAnalysis.calculate_energy(defect)
                        print(f"\n能量分析:")
                        print(f"总能量: {energy['total_energy']:.2f}")
                        print(f"弯曲能量: {energy['bend_energy']:.2f}")

                        structure = DataAnalysis.analyze_defect_structure(defect)
                        print(f"\n结构特征:")
                        print(f"中心位置: ({structure['center']['x']:.2f}, {structure['center']['y']:.2f}, {structure['center']['z']:.2f})")
                        print(f"大小范围: X={structure['size']['x_range']:.2f}, Y={structure['size']['y_range']:.2f}, Z={structure['size']['z_range']:.2f}")
                        print(f"分子数量: {structure['num_molecules']}")

                        next_action = input("\n1. 分析其他缺陷类型\n2. 返回主菜单\n请选择: ")
                        if next_action != "1":
                            break

                elif choice == "14":
                    while True:
                        if not VIDEO_ANALYSIS_AVAILABLE:
                            print("视频分析模块不可用，请安装opencv-python")
                            break

                        print("视频分析...")
                        video_dir = os.path.join(os.path.dirname(__file__), 'videos')
                        video_analyzer = VideoAnalysis(video_dir=video_dir)

                        video_files = video_analyzer.list_videos()

                        if not video_files:
                            print("未找到视频文件")
                            break

                        print("\n选择要分析的视频:")
                        print("0. 分析所有视频")
                        for i, video_file in enumerate(video_files, 1):
                            print(f"{i}. {os.path.basename(video_file)}")

                        video_choice = input(f"请选择 (0-{len(video_files)}): ")

                        try:
                            video_choice = int(video_choice)
                            keyframes_dir = os.path.join(os.path.dirname(__file__), 'examples', 'keyframes')
                            if video_choice == 0:
                                video_analyzer.analyze_all_videos(output_dir=keyframes_dir)
                            elif 1 <= video_choice <= len(video_files):
                                video_analyzer.analyze_video(video_files[video_choice - 1], output_dir=keyframes_dir)
                            else:
                                print("无效选择")
                        except ValueError:
                            print("无效输入")

                        next_action = input("\n1. 分析其他视频\n2. 返回主菜单\n请选择: ")
                        if next_action != "1":
                            break

                elif choice == "15":
                    print("退出程序...")
                    break

                else:
                    print("无效选择，请重新输入")

        except KeyboardInterrupt:
            print("\n\n程序已被用户中断，安全退出~")
            sys.exit(0)

if __name__ == "__main__":
    Main.run()
