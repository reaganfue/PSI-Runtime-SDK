#!/usr/bin/env python
# coding: utf-8

# =======================================================
# Segment 1: 模組說明 (Module Docstring)
# =======================================================
"""
語義場分析示例 - 展示 SemanticFieldEngine 的基本用法

本示例展示如何初始化語義場引擎並對多個輸入文本進行解析與知識解鎖，
以獲取文本中的關鍵知識點。適用於自然語言處理中的語義理解與知識提取任務。
版本：1.0.0
作者：Reagan Fu 開發團隊
更新日期：2025-03-12
"""

# =======================================================
# Segment 2: 模組匯入與路徑設置 (Imports & Path Setup)
# =======================================================
import sys
import os
import time

# 將項目根目錄添加到系統路徑中，方便導入內部模組
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from psi_field import SemanticFieldEngine, FieldConfig, DataParser

# =======================================================
# Segment 3: 主程式入口與引擎初始化 (Main Entry & Engine Initialization)
# =======================================================
def main():
    print("=" * 60)
    print("SemanticFieldEngine 語義場分析示例")
    print("=" * 60)
    
    # 初始化配置，啟用詳細日誌（便於調試與追蹤）
    config = FieldConfig(enable_detailed_logging=True)
    
    # 初始化語義場引擎
    engine = SemanticFieldEngine(config)
    
    # 測試輸入列表
    test_inputs = [
        "人工智能如何改變未來的工作方式？",
        "語義理解在自然語言處理中的重要性是什麼？",
        "量子計算對密碼學的影響"
    ]
    
    # =======================================================
    # Segment 4: 輸入解析與知識解鎖 (Input Parsing & Knowledge Unlocking)
    # =======================================================
    for input_text in test_inputs:
        print(f"\n{'=' * 60}\n處理輸入: {input_text}\n{'=' * 60}")
        
        try:
            # 解析輸入文本生成語義輸入結構
            semantic_input = DataParser.parse(input_text)
            print(f"解析輸入: {semantic_input.text}")
            
            # 提取知識關鍵字（示例：利用 DataParser 提供的靜態方法）
            knowledge_keys = DataParser.extract_knowledge_keys(input_text)
            print(f"提取知識關鍵字: {knowledge_keys}")
            
            # 使用語義場引擎進行知識解鎖
            unlocked_keys = engine.psi_engine.unlock_knowledge(semantic_input)
            print(f"解鎖知識點: {unlocked_keys}")
        except Exception as e:
            print(f"處理過程發生錯誤: {str(e)}")
        
        # 暫停一秒，避免輸出過快
        time.sleep(1)

# =======================================================
# Segment 5: 主程式入口 (Main Entry Point)
# =======================================================
if __name__ == "__main__":
    main()
