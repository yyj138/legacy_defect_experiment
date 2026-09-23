# 文件工具模块 - 提供文件操作相关功能

import os
import json
import numpy as np
from typing import Any, Dict, List, Optional

def ensure_dir(path: str) -> None:
    # 确保目录存在，如果不存在则创建
    os.makedirs(path, exist_ok=True)

def save_json(data: Dict[str, Any], filepath: str, indent: int = 4) -> None:
    # 保存数据为JSON文件
    ensure_dir(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)

def load_json(filepath: str) -> Dict[str, Any]:
    # 从JSON文件加载数据
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_npy(data: np.ndarray, filepath: str) -> None:
    # 保存NumPy数组为.npy文件
    ensure_dir(os.path.dirname(filepath))
    np.save(filepath, data)

def load_npy(filepath: str) -> np.ndarray:
    # 从.npy文件加载NumPy数组
    return np.load(filepath)

def get_files_in_dir(directory: str, extensions: Optional[List[str]] = None) -> List[str]:
    # 获取目录中指定扩展名的文件列表
    files = []
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isfile(full_path):
            if extensions is None:
                files.append(full_path)
            else:
                _, ext = os.path.splitext(entry)
                if ext.lower() in extensions:
                    files.append(full_path)
    return sorted(files)

def get_subdirectories(directory: str) -> List[str]:
    # 获取目录下的所有子目录
    dirs = []
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isdir(full_path):
            dirs.append(full_path)
    return sorted(dirs)

def generate_unique_filename(directory: str, prefix: str, extension: str) -> str:
    # 生成唯一的文件名
    ensure_dir(directory)
    counter = 1
    while True:
        filename = f"{prefix}_{counter:03d}.{extension}"
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            return filepath
        counter += 1

def copy_file(source: str, destination: str) -> None:
    # 复制文件
    ensure_dir(os.path.dirname(destination))
    import shutil
    shutil.copy2(source, destination)

def delete_file(filepath: str) -> bool:
    # 删除文件
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False

def file_exists(filepath: str) -> bool:
    # 检查文件是否存在
    return os.path.exists(filepath)

def get_file_size(filepath: str) -> int:
    # 获取文件大小（字节）
    if os.path.exists(filepath):
        return os.path.getsize(filepath)
    return 0

def get_file_modification_time(filepath: str) -> float:
    # 获取文件修改时间
    if os.path.exists(filepath):
        return os.path.getmtime(filepath)
    return 0.0
