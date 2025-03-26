#!/usr/bin/env python
# coding: utf-8
"""
語義場分析示例 - 展示SemanticFieldEngine的基本用法
"""

import sys
import os
import time

# 將项目根目錄添加到路徑中，方便導入模組
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from psi_field import SemanticFieldEngine, FieldConfig, DataParser

def main():
    print("="*60)
    print("SemanticFieldEngine 語義場分析示例")
    print("="*60)
    
    # 初始化配置
    config = FieldConfig(enable_detailed_logging=True)
    
    # 初始化語義場引擎
    engine = SemanticFieldEngine(config)
    
    # 測試輸入
    test_inputs = [
        "人工智能如何改變未來的工作方式？",
        "語義理解在自然語言處理中的重要性是什麼？",
        "量子計算對密碼學的影響"
    ]
    
    for input_text in test_inputs:
        print(f"\n{'='*60}\n處理輸入: {input_text}\n{'='*60}")
        
        # 解析輸入
        semantic_input = DataParser.parse(input_text)
        
        # 處理輸入 (假設 SemanticFieldEngine 有 process_input 方法)
        # 注意：由於原始代碼中沒有完整的 process_input 實現，這裡僅作示例
        print(f"解析輸入: {semantic_input.text}")
        print(f"提取知識關鍵字: {DataParser.extract_knowledge_keys(input_text)}")
        
        # 模擬解鎖知識
        unlocked_keys = engine.psi_engine.unlock_knowledge(semantic_input)
        print(f"解鎖知識點: {unlocked_keys}")
        
        # 暫停一下，避免輸出太快
        time.sleep(1)

if __name__ == "__main__":
    main()
