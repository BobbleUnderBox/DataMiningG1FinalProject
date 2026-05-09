"""
BNPL 信用风险分类项目 - 主包
"""

__version__ = "1.0.0"
__author__ = "Data Science Team"

from .data_loader import ConfigLoader, DataDownloader, DataLoader, load_data

__all__ = [
    'ConfigLoader',
    'DataDownloader', 
    'DataLoader',
    'load_data',
]
