#!/usr/bin/env python
# coding: utf-8

# =======================================================
# Segment 1: 模組說明 (Module Docstring)
# =======================================================
"""
量子分析器示例 - 展示 QuantumAnalyzer 的基本用法

本示例展示如何初始化量子分析器並對多個輸入文本執行不同模式的推理：
1. 量子分析模式 (不使用基礎邏輯)
2. 基礎邏輯模式 (使用基本邏輯進行分析)
3. 綜合分析 (綜合多種分析結果生成整體評分)

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

# 移除 psi_runtime_sdk 前綴，直接導入量子引擎模組
from quantum_engine import QuantumAnalyzer, Config

# =======================================================
# Segment 3: 主程式入口與量子分析器初始化 (Main Entry & Engine Initialization)
# =======================================================
def main():
    print("=" * 60)
    print("QuantumAnalyzer 量子分析示例")
    print("=" * 60)
    
    # 初始化配置，設定 DEBUG 級別
    config = Config(log_level=10)
    
    # 初始化量子分析器
    engine = QuantumAnalyzer(config)
    
    # 測試輸入列表
    test_inputs = [
        "探索人工智能與量子計算的結合點",
        "分析長期技術趨勢的方法論",
        "未來十年的技術發展方向預測"
    ]
    
    # =======================================================
    # Segment 4: 輸入處理與模式調用 (Input Processing & Mode Invocation)
    # =======================================================
    for input_text in test_inputs:
        print(f"\n{'=' * 60}\n處理輸入: {input_text}\n{'=' * 60}")
        
        try:
            # 模式一: 量子分析 (不使用基礎邏輯)
            quantum_result = engine.run_inference(input_text, use_basic_logic=False)
            print(f"量子分析結果: {quantum_result}")
        except Exception as e:
            print(f"量子分析錯誤: {str(e)}")
        
        try:
            # 模式二: 基礎邏輯分析 (使用基本邏輯處理)
            basic_result = engine.run_inference(input_text, use_basic_logic=True)
            basic_final = basic_result.get('final_result', 'N/A')
            print(f"基礎邏輯分析結果: {basic_final}")
        except Exception as e:
            print(f"基礎邏輯分析錯誤: {str(e)}")
        
        try:
            # 模式三: 綜合分析
            comprehensive_result = engine.comprehensive_analysis(input_text)
            comp_score = comprehensive_result.get('integrated_score', 'N/A')
            print(f"綜合分析結果: {comp_score}")
        except Exception as e:
            print(f"綜合分析錯誤: {str(e)}")
        
        # 暫停一秒，避免輸出過快
        time.sleep(1)

# =======================================================
# Segment 5: 主程式入口 (Main Entry Point)
# =======================================================
if __name__ == "__main__":
    main()
