"""
========================================
Segment 1: 模組說明 (Module Docstring)
========================================
conftest.py 測試配置文件

本文件包含全局 fixtures 和測試設置，確保測試環境的正確初始化。
主要功能包括：
    - 配置測試數據目錄
    - 設置全局日誌配置以便於測試過程中的日誌追蹤

版本: 1.0.0
作者: 測試團隊
許可證: Proprietary
"""

# ========================================
# Segment 2: 模組匯入與基礎設置 (Imports & Setup)
# ========================================
import pytest
import os
import sys

# 確保可以導入 SDK 模組，調整路徑以匹配項目結構
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ========================================
# Segment 3: 全局 Fixtures 與配置管理 (Global Fixtures & Configuration)
# ========================================
@pytest.fixture(scope="session")
def test_data_dir():
    """
    返回測試數據目錄。

    返回:
        str: 測試數據所在目錄的絕對路徑。
    """
    return os.path.join(os.path.dirname(__file__), "test_data")

@pytest.fixture(autouse=True)
def setup_logging(caplog):
    """
    設置測試期間的日誌配置。

    這個 fixture 會自動啟用，將測試日誌級別設置為 INFO，以便於追蹤測試過程中的日誌輸出。
    """
    import logging
    caplog.set_level(logging.INFO)
