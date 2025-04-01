#!/usr/bin/env python
# coding: utf-8

# =======================================================
# Segment 1: 模組說明 (Module Docstring)
# =======================================================
"""
綜合分析示例 - 展示三個主要引擎的組合使用

本示例展示如何同時利用語義場引擎、量子分析器與基礎邏輯推理引擎，
對輸入文本進行綜合分析，並整合各引擎輸出生成最終結論與建議。
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
import json

# 將項目根目錄添加到系統路徑中，方便導入內部模組
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 移除 psi_runtime_sdk 前綴，直接導入各引擎
from logic_core import BasicResponseLogic, Config as BRLConfig
from psi_field import SemanticFieldEngine, FieldConfig
from quantum_engine import QuantumAnalyzer, Config as QAConfig

# =======================================================
# Segment 3: 主程式入口與引擎初始化 (Main Entry & Engine Initialization)
# =======================================================
def main():
    print("=" * 60)
    print("PsiRuntimeSDK 綜合分析示例")
    print("=" * 60)
    
    # 初始化各模組配置
    brl_config = BRLConfig(timestamp="2025-03-12T00:00:00", debug_mode=True)
    field_config = FieldConfig(enable_detailed_logging=True)
    qa_config = QAConfig(log_level=10)  # DEBUG 級別
    
    # 初始化各模組引擎
    brl_engine = BasicResponseLogic()
    field_engine = SemanticFieldEngine(field_config)
    qa_engine = QuantumAnalyzer(qa_config)
    
    # 測試輸入文本
    test_input = "分析未來五年的技術發展趨勢，特別關注AI與量子計算領域的突破"
    print(f"\n{'=' * 60}\n處理輸入: {test_input}\n{'=' * 60}")
    
    # =======================================================
    # Segment 4: 語義場引擎處理 (Semantic Field Engine Processing)
    # =======================================================
    try:
        # 解析輸入並生成語義表示
        semantic_input = SemanticFieldEngine.DataParser.parse(test_input)
        # 使用語義場引擎進行知識解鎖
        unlocked_keys = field_engine.psi_engine.unlock_knowledge(semantic_input)
        print(f"解鎖知識點: {unlocked_keys}")
    except Exception as e:
        print(f"語義場處理錯誤: {str(e)}")
        unlocked_keys = []
    
    # =======================================================
    # Segment 5: 量子分析器處理 (Quantum Analyzer Processing)
    # =======================================================
    try:
        comprehensive_result = qa_engine.comprehensive_analysis(test_input)
        integrated_score = comprehensive_result.get("integrated_score", "N/A")
        print(f"量子綜合分析分數: {integrated_score}")
    except Exception as e:
        print(f"量子分析錯誤: {str(e)}")
        comprehensive_result = {}
    
    # =======================================================
    # Segment 6: 基礎邏輯推理處理 (Basic Logic Inference)
    # =======================================================
    try:
        brl_result = brl_engine.run(test_input, brl_config)
    except Exception as e:
        print(f"基礎邏輯推理錯誤: {str(e)}")
        brl_result = {}
    
    # =======================================================
    # Segment 7: 結果整合 (Result Integration)
    # =======================================================
    try:
        integrated_result = {
            "input": test_input,
            "unlocked_knowledge": unlocked_keys,
            "quantum_analysis": comprehensive_result,
            "logical_analysis": brl_result,
            "conclusion": {
                "confidence": (comprehensive_result.get("integrated_score", 0.5) +
                               brl_result.get("final_result", 0.5)) / 2,
                "recommended_action": "探索並投入資源於 " + ", ".join(unlocked_keys) if unlocked_keys else "待進一步分析"
            }
        }
        
        # =======================================================
        # Segment 8: 輸出最終結果 (Output Final Integrated Result)
        # =======================================================
        print("\n最終整合結果:")
        print(json.dumps(integrated_result.get("conclusion", {}), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"結果整合錯誤: {str(e)}")
    
    # 暫停一下，避免輸出過快
    time.sleep(1)

# =======================================================
# Segment 9: 主程式入口 (Main Entry Point)
# =======================================================
if __name__ == "__main__":
    main()
