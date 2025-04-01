#!/usr/bin/env python
# coding: utf-8

# =======================================================
# Segment 1: 模組說明 (Module Docstring)
# =======================================================
"""
基本推理示例 - 展示 BasicResponseLogic 的基本用法

本示例展示如何初始化配置、建立推理引擎 BasicResponseLogic，
並對多個輸入文本執行推理，最後生成並輸出文本報告。
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

# 將项目根目錄添加到系統路徑中，方便導入內部模組
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_core import BasicResponseLogic, Config, ReportGenerator

# =======================================================
# Segment 3: 主函數定義 (Main Function)
# =======================================================
def main():
    print("=" * 60)
    print("BasicResponseLogic 基本推理示例")
    print("=" * 60)
    
    # 初始化配置，包含時間戳與調試模式設定
    config = Config(timestamp="2025-03-12T00:00:00", debug_mode=True)
    
    # 初始化推理引擎
    engine = BasicResponseLogic()
    
    # 測試輸入列表
    test_inputs = [
        "請分析未來市場趨勢並給出建議",
        "我需要了解最新的技術發展方向",
        "如何優化現有產品的用戶體驗"
    ]
    
    # 遍歷每個輸入，執行推理並生成報告
    for input_text in test_inputs:
        print(f"\n{'=' * 60}\n處理輸入: {input_text}\n{'=' * 60}")
        
        try:
            # 執行完整推理流程
            result = engine.run(input_text, config)
            
            # 生成文本格式報告
            report = ReportGenerator(result).generate_report(format="text")
            
            # 輸出報告內容
            print(report)
        except Exception as e:
            print(f"推理過程發生錯誤: {str(e)}")
        
        # 暫停一秒，避免輸出過快
        time.sleep(1)

# =======================================================
# Segment 4: 主程式入口 (Main Entry)
# =======================================================
if __name__ == "__main__":
    main()
