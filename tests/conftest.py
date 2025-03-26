"""
測試配置文件

包含全局 fixtures 和測試設置
"""
import pytest
import os
import sys

# 確保可以導入 SDK 模組
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session")
def test_data_dir():
    """返回測試數據目錄"""
    return os.path.join(os.path.dirname(__file__), "test_data")

@pytest.fixture(autouse=True)
def setup_logging(caplog):
    """設置測試期間的日誌配置"""
    import logging
    caplog.set_level(logging.INFO) 
