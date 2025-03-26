#!/usr/bin/env python
# coding: utf-8
"""
量子分析器示例 - 展示QuantumAnalyzer的基本用法
"""

import sys
import os
import time

# 將项目根目錄添加到路徑中，方便導入模組
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 修正: 移除 psi_runtime_sdk 前綴
from quantum_engine import QuantumAnalyzer, Config

def main():
    print("="*60)
    print("QuantumAnalyzer 量子分析示例")
    print("="*60)
    
    # 初始化配置
    config = Config(log_level=10)  # DEBUG 級別
    
    # 初始化量子分析器
    engine = QuantumAnalyzer(config)
    
    # 測試輸入
    test_inputs = [
        "探索人工智能與量子計算的結合點",
        "分析長期技術趨勢的方法論",
        "未來十年的技術發展方向預測"
    ]
    
    for input_text in test_inputs:
        print(f"\n{'='*60}\n處理輸入: {input_text}\n{'='*60}")
        
        # 執行量子分析
        quantum_result = engine.run_inference(input_text, use_basic_logic=False)
        print(f"量子分析結果: {quantum_result}")
        
        # 執行基礎邏輯分析
        basic_result = engine.run_inference(input_text, use_basic_logic=True)
        print(f"基礎邏輯分析結果: {basic_result.get('final_result', 'N/A')}")
        
        # 執行綜合分析
        comprehensive_result = engine.comprehensive_analysis(input_text)
        print(f"綜合分析結果: {comprehensive_result.get('integrated_score', 'N/A')}")
        
        # 暫停一下，避免輸出太快
        time.sleep(1)

if __name__ == "__main__":
    main()
