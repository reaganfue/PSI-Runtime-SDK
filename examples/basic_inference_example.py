#!/usr/bin/env python
# coding: utf-8
"""
基本推理示例 - 展示BasicResponseLogic的基本用法
"""

import sys
import os
import time

# 將项目根目錄添加到路徑中，方便導入模組
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_core import BasicResponseLogic, Config, ReportGenerator

def main():
    print("="*60)
    print("BasicResponseLogic 基本推理示例")
    print("="*60)
    
    # 初始化配置
    config = Config(timestamp="2025-03-12T00:00:00", debug_mode=True)
    
    # 初始化推理引擎
    engine = BasicResponseLogic()
    
    # 測試輸入
    test_inputs = [
        "請分析未來市場趨勢並給出建議",
        "我需要了解最新的技術發展方向",
        "如何優化現有產品的用戶體驗"
    ]
    
    for input_text in test_inputs:
        print(f"\n{'='*60}\n處理輸入: {input_text}\n{'='*60}")
        
        # 執行推理
        result = engine.run(input_text, config)
        
        # 生成報告
        report = ReportGenerator(result).generate_report(format="text")
        
        # 顯示結果
        print(report)
        
        # 暫停一下，避免輸出太快
        time.sleep(1)

if __name__ == "__main__":
    main()
