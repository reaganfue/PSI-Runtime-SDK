#!/usr/bin/env python
# coding: utf-8
"""
綜合分析示例 - 展示三個主要引擎的組合使用
"""

import sys
import os
import time
import json

# 將项目根目錄添加到路徑中，方便導入模組
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 修正: 移除 psi_runtime_sdk 前綴
from logic_core import BasicResponseLogic, Config as BRLConfig
from psi_field import SemanticFieldEngine, FieldConfig
from quantum_engine import QuantumAnalyzer, Config as QAConfig

def main():
    print("="*60)
    print("PsiRuntimeSDK 綜合分析示例")
    print("="*60)
    
    # 初始化各模組配置
    brl_config = BRLConfig(timestamp="2025-03-12T00:00:00", debug_mode=True)
    field_config = FieldConfig(enable_detailed_logging=True)
    qa_config = QAConfig(log_level=10)  # DEBUG 級別
    
    # 初始化各模組引擎
    brl_engine = BasicResponseLogic()
    field_engine = SemanticFieldEngine(field_config)
    qa_engine = QuantumAnalyzer(qa_config)
    
    # 測試輸入
    test_input = "分析未來五年的技術發展趨勢，特別關注AI與量子計算領域的突破"
    
    print(f"\n{'='*60}\n處理輸入: {test_input}\n{'='*60}")
    
    # 1. 使用語義場引擎進行知識解鎖
    semantic_input = SemanticFieldEngine.DataParser.parse(test_input)
    unlocked_keys = field_engine.psi_engine.unlock_knowledge(semantic_input)
    print(f"解鎖知識點: {unlocked_keys}")
    
    # 2. 使用量子分析器進行綜合分析
    comprehensive_result = qa_engine.comprehensive_analysis(test_input)
    print(f"量子綜合分析分數: {comprehensive_result.get('integrated_score', 'N/A')}")
    
    # 3. 使用基礎邏輯引擎生成詳細報告
    brl_result = brl_engine.run(test_input, brl_config)
    
    # 4. 整合所有結果
    integrated_result = {
        "input": test_input,
        "unlocked_knowledge": unlocked_keys,
        "quantum_analysis": comprehensive_result,
        "logical_analysis": brl_result,
        "conclusion": {
            "confidence": (comprehensive_result.get("integrated_score", 0.5) + 
                          brl_result.get("final_result", 0.5)) / 2,
            "recommended_action": "探索並投入資源於" + ", ".join(unlocked_keys)
        }
    }
    
    # 顯示最終整合結果
    print("\n最終整合結果:")
    print(json.dumps(integrated_result.get("conclusion", {}), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
