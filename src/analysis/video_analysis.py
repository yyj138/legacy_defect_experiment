import os
import cv2
import numpy as np

class VideoAnalysis:
    # 视频分析模块

    def __init__(self, video_dir=None):
        # 初始化视频分析器
        if video_dir is None:
            current_file_dir = os.path.dirname(os.path.abspath(__file__))
            self.video_dir = os.path.abspath(os.path.join(current_file_dir, 'videos'))
        else:
            self.video_dir = os.path.abspath(video_dir)
        print(f"视频目录: {self.video_dir}")
        self.video_files = self._find_video_files()

    def _find_video_files(self):
        # 查找视频文件
        video_files = []
        if os.path.exists(self.video_dir):
            for file in os.listdir(self.video_dir):
                if file.endswith(('.mp4', '.avi', '.mov')):
                    video_files.append(os.path.join(self.video_dir, file))
        return sorted(video_files)

    def list_videos(self):
        # 列出所有视频文件
        print("找到的视频文件:")
        for i, video_file in enumerate(self.video_files, 1):
            print(f"{i}. {os.path.basename(video_file)}")
        return self.video_files

    def analyze_video(self, video_path, output_dir='./examples'):
        # 分析视频文件
        if not os.path.exists(video_path):
            print(f"视频文件不存在: {video_path}")
            return None

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"无法打开视频文件: {video_path}")
            return None

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = frame_count / fps if fps > 0 else 0

        print(f"\n视频信息:")
        print(f"文件名: {os.path.basename(video_path)}")
        print(f"分辨率: {width}x{height}")
        print(f"帧率: {fps:.2f} fps")
        print(f"总帧数: {frame_count}")
        print(f"时长: {duration:.2f} 秒")

        key_frames = []
        frame_interval = max(1, frame_count // 10)

        print(f"提取关键帧，间隔: {frame_interval}")

        for i in range(0, frame_count, frame_interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if ret:
                key_frames.append(frame)
                print(f"成功读取帧 {i}")
            else:
                print(f"读取帧 {i} 失败")

        print(f"共提取 {len(key_frames)} 个关键帧")

        os.makedirs(output_dir, exist_ok=True)

        video_index = self.video_files.index(video_path) + 1
        video_output_dir = os.path.join(output_dir, f"video_{video_index}")
        os.makedirs(video_output_dir, exist_ok=True)

        print(f"创建输出目录: {video_output_dir}")

        print(f"开始保存关键帧到: {video_output_dir}")

        for i, frame in enumerate(key_frames):
            frame_path = os.path.join(video_output_dir, f"frame_{i:02d}.png")
            try:
                success = cv2.imwrite(frame_path, frame)
                if success:
                    print(f"成功保存关键帧: {frame_path}")
                else:
                    print(f"保存关键帧失败: {frame_path}")
            except Exception as e:
                print(f"保存关键帧时出错: {e}")

        cap.release()

        return {
            'fps': fps,
            'frame_count': frame_count,
            'width': width,
            'height': height,
            'duration': duration,
            'key_frames': len(key_frames)
        }

    def analyze_all_videos(self, output_dir='./examples'):
        """分析所有视频文件"""
        results = {}

        for video_file in self.video_files:
            print(f"\n{'='*60}")
            result = self.analyze_video(video_file, output_dir)
            if result:
                results[os.path.basename(video_file)] = result

        return results

    def extract_motion_features(self, video_path):
        # 提取运动特征
        if not os.path.exists(video_path):
            return None

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            return None

        ret, prev_frame = cap.read()
        if not ret:
            cap.release()
            return None

        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

        motion_magnitudes = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            flow = cv2.calcOpticalFlowFarneback(
                prev_gray, gray, None,
                0.5, 3, 15, 3, 5, 1.2, 0
            )

            magnitude = np.sqrt(flow[..., 0]**2 + flow[..., 1]**2)
            motion_magnitudes.append(np.mean(magnitude))

            prev_gray = gray

        cap.release()

        return {
            'mean_motion': np.mean(motion_magnitudes),
            'max_motion': np.max(motion_magnitudes),
            'motion_variance': np.var(motion_magnitudes)
        }
