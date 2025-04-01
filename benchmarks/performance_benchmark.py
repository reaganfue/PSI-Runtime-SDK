#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =======================================================
# Segment 1: 模組說明 (Module Docstring)
# =======================================================
"""
PSI Runtime SDK 性能基準測試模組

本模組負責測量 PSI Runtime SDK 各核心組件的性能，包括：
1. 處理速度測試：測量不同大小輸入的處理時間
2. 記憶體使用測試：測量處理過程中的記憶體峰值
3. 準確性測試：測量分析結果的準確性與一致性
4. 擴展性測試：測量在多核心環境下的性能擴展

版本：1.0.0
作者：Reagan Fu 開發團隊
更新日期：2025-03-12
"""

# =======================================================
# Segment 2: 模組匯入與基礎設置 (Imports & Setup)
# =======================================================
import os
import sys
import time
import json
import logging
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Any, Tuple
from datetime import datetime
import psutil
import gc

# 添加專案根目錄到系統路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 從 SDK 匯入需要測試的模組
from psi_field import PsiFieldModel
from quantum_engine import QuantumAnalyzer
from logic_core import BasicResponseLogic

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("benchmark.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# =======================================================
# Segment 3: 測試配置定義 (Test Configuration)
# =======================================================
# 測試輸入大小配置
TEXT_SIZES = [100, 500, 1000, 5000, 10000]  # 字符數
# 每個測試重複次數
REPEAT_COUNT = 5
# 測試結果輸出目錄
OUTPUT_DIR = "benchmark_results"
# 生成測試結果圖形
GENERATE_PLOTS = True

# =======================================================
# Segment 4: 輔助函數 (Helper Functions)
# =======================================================
def generate_test_text(size: int) -> str:
    """
    生成指定大小的測試文本
    
    Args:
        size (int): 文本大小（字符數）
    
    Returns:
        str: 生成的測試文本
    """
    words = [
        "人工智能", "語義場", "量子分析", "語境穩定相位", "知識解鎖",
        "動態演化", "上下文理解", "語義張力", "推理能力", "認知模型"
    ]
    text = ""
    while len(text) < size:
        text += np.random.choice(words) + " "
    return text[:size]

def measure_memory_usage() -> float:
    """
    測量當前進程的記憶體使用量（MB）
    
    Returns:
        float: 記憶體使用量（MB）
    """
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # 轉換為 MB

def run_timed_test(func, *args, **kwargs) -> Tuple[float, float, Any]:
    """
    運行計時測試並返回執行時間、記憶體使用量和結果
    
    Args:
        func: 要測試的函數
        *args, **kwargs: 函數參數
    
    Returns:
        Tuple[float, float, Any]: (執行時間, 記憶體使用量, 函數返回結果)
    """
    # 清理記憶體
    gc.collect()
    # 記錄初始記憶體
    mem_before = measure_memory_usage()
    # 記錄開始時間
    start_time = time.time()
    # 執行函數
    result = func(*args, **kwargs)
    # 計算耗時
    elapsed_time = time.time() - start_time
    # 測量記憶體使用量
    mem_after = measure_memory_usage()
    # 計算記憶體增量
    mem_used = mem_after - mem_before
    
    return elapsed_time, mem_used, result

def save_benchmark_results(results: Dict[str, Any], name: str):
    """
    保存基準測試結果
    
    Args:
        results (Dict[str, Any]): 測試結果數據
        name (str): 測試名稱
    """
    # 創建輸出目錄
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 檔案名添加時間戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUT_DIR}/{name}_benchmark_{timestamp}.json"
    
    # 保存測試結果
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    logger.info(f"測試結果已保存到: {filename}")

def plot_benchmark_results(results: Dict[str, Any], name: str):
    """
    繪製性能測試結果圖表
    
    Args:
        results (Dict[str, Any]): 測試結果數據
        name (str): 測試名稱
    """
    if not GENERATE_PLOTS:
        return
    
    # 創建輸出目錄
    os.makedirs(f"{OUTPUT_DIR}/plots", exist_ok=True)
    
    # 獲取文本大小和時間數據
    sizes = results["text_sizes"]
    times = results["avg_times"]
    memory = results["avg_memory"]
    
    # 繪製處理時間圖
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times, marker='o', linestyle='-', linewidth=2)
    plt.title(f"{name} - 處理時間與輸入大小關係")
    plt.xlabel("輸入大小 (字符數)")
    plt.ylabel("處理時間 (秒)")
    plt.grid(True)
    plt.savefig(f"{OUTPUT_DIR}/plots/{name}_time_plot.png")
    
    # 繪製記憶體使用圖
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, memory, marker='s', linestyle='-', linewidth=2)
    plt.title(f"{name} - 記憶體使用與輸入大小關係")
    plt.xlabel("輸入大小 (字符數)")
    plt.ylabel("記憶體使用增量 (MB)")
    plt.grid(True)
    plt.savefig(f"{OUTPUT_DIR}/plots/{name}_memory_plot.png")
    
    logger.info(f"測試結果圖表已保存到: {OUTPUT_DIR}/plots/")

# =======================================================
# Segment 5: 具體測試實現 (Test Implementations)
# =======================================================
def benchmark_psi_field_model():
    """
    測試 PsiFieldModel 的性能
    """
    logger.info("開始 PsiFieldModel 性能測試")
    
    # 初始化模型
    model = PsiFieldModel(config={"use_advanced": False})
    
    results = {
        "model": "PsiFieldModel",
        "timestamp": datetime.now().isoformat(),
        "text_sizes": TEXT_SIZES,
        "repeat_count": REPEAT_COUNT,
        "times": [],
        "memory": [],
        "avg_times": [],
        "avg_memory": [],
        "test_details": []
    }
    
    # 針對不同大小的輸入進行測試
    for size in TEXT_SIZES:
        logger.info(f"測試輸入大小: {size} 字符")
        test_text = generate_test_text(size)
        
        size_times = []
        size_memory = []
        
        # 重複測試多次取平均
        for i in range(REPEAT_COUNT):
            elapsed_time, mem_used, result = run_timed_test(model.process, test_text)
            size_times.append(elapsed_time)
            size_memory.append(mem_used)
            
            logger.debug(f"  重複 {i+1}/{REPEAT_COUNT}: 時間={elapsed_time:.4f}秒, 記憶體={mem_used:.2f}MB")
        
        # 計算平均值
        avg_time = np.mean(size_times)
        avg_memory = np.mean(size_memory)
        
        # 記錄結果
        results["times"].append(size_times)
        results["memory"].append(size_memory)
        results["avg_times"].append(avg_time)
        results["avg_memory"].append(avg_memory)
        results["test_details"].append({
            "size": size,
            "times": size_times,
            "memory": size_memory,
            "avg_time": avg_time,
            "avg_memory": avg_memory
        })
        
        logger.info(f"  平均處理時間: {avg_time:.4f}秒, 平均記憶體增量: {avg_memory:.2f}MB")
    
    # 保存結果
    save_benchmark_results(results, "psi_field_model")
    # 繪製圖表
    plot_benchmark_results(results, "PsiFieldModel")
    
    logger.info("PsiFieldModel 性能測試完成")
    return results

def benchmark_quantum_analyzer():
    """
    測試 QuantumAnalyzer 的性能
    """
    logger.info("開始 QuantumAnalyzer 性能測試")
    
    # 初始化分析器
    analyzer = QuantumAnalyzer()
    
    results = {
        "model": "QuantumAnalyzer",
        "timestamp": datetime.now().isoformat(),
        "text_sizes": TEXT_SIZES,
        "repeat_count": REPEAT_COUNT,
        "times": [],
        "memory": [],
        "avg_times": [],
        "avg_memory": [],
        "test_details": []
    }
    
    # 針對不同大小的輸入進行測試
    for size in TEXT_SIZES:
        logger.info(f"測試輸入大小: {size} 字符")
        test_text = generate_test_text(size)
        
        size_times = []
        size_memory = []
        
        # 重複測試多次取平均
        for i in range(REPEAT_COUNT):
            elapsed_time, mem_used, result = run_timed_test(analyzer.comprehensive_analysis, test_text)
            size_times.append(elapsed_time)
            size_memory.append(mem_used)
            
            logger.debug(f"  重複 {i+1}/{REPEAT_COUNT}: 時間={elapsed_time:.4f}秒, 記憶體={mem_used:.2f}MB")
        
        # 計算平均值
        avg_time = np.mean(size_times)
        avg_memory = np.mean(size_memory)
        
        # 記錄結果
        results["times"].append(size_times)
        results["memory"].append(size_memory)
        results["avg_times"].append(avg_time)
        results["avg_memory"].append(avg_memory)
        results["test_details"].append({
            "size": size,
            "times": size_times,
            "memory": size_memory,
            "avg_time": avg_time,
            "avg_memory": avg_memory
        })
        
        logger.info(f"  平均處理時間: {avg_time:.4f}秒, 平均記憶體增量: {avg_memory:.2f}MB")
    
    # 保存結果
    save_benchmark_results(results, "quantum_analyzer")
    # 繪製圖表
    plot_benchmark_results(results, "QuantumAnalyzer")
    
    logger.info("QuantumAnalyzer 性能測試完成")
    return results

def benchmark_basic_response_logic():
    """
    測試 BasicResponseLogic 的性能
    """
    logger.info("開始 BasicResponseLogic 性能測試")
    
    # 初始化邏輯引擎
    from logic_core import Config
    config = Config(debug_mode=False)
    engine = BasicResponseLogic()
    
    results = {
        "model": "BasicResponseLogic",
        "timestamp": datetime.now().isoformat(),
        "text_sizes": TEXT_SIZES,
        "repeat_count": REPEAT_COUNT,
        "times": [],
        "memory": [],
        "avg_times": [],
        "avg_memory": [],
        "test_details": []
    }
    
    # 針對不同大小的輸入進行測試
    for size in TEXT_SIZES:
        logger.info(f"測試輸入大小: {size} 字符")
        test_text = generate_test_text(size)
        
        size_times = []
        size_memory = []
        
        # 重複測試多次取平均
        for i in range(REPEAT_COUNT):
            elapsed_time, mem_used, result = run_timed_test(engine.run, test_text, config)
            size_times.append(elapsed_time)
            size_memory.append(mem_used)
            
            logger.debug(f"  重複 {i+1}/{REPEAT_COUNT}: 時間={elapsed_time:.4f}秒, 記憶體={mem_used:.2f}MB")
        
        # 計算平均值
        avg_time = np.mean(size_times)
        avg_memory = np.mean(size_memory)
        
        # 記錄結果
        results["times"].append(size_times)
        results["memory"].append(size_memory)
        results["avg_times"].append(avg_time)
        results["avg_memory"].append(avg_memory)
        results["test_details"].append({
            "size": size,
            "times": size_times,
            "memory": size_memory,
            "avg_time": avg_time,
            "avg_memory": avg_memory
        })
        
        logger.info(f"  平均處理時間: {avg_time:.4f}秒, 平均記憶體增量: {avg_memory:.2f}MB")
    
    # 保存結果
    save_benchmark_results(results, "basic_response_logic")
    # 繪製圖表
    plot_benchmark_results(results, "BasicResponseLogic")
    
    logger.info("BasicResponseLogic 性能測試完成")
    return results

def compare_all_models():
    """
    比較所有模型的性能
    """
    logger.info("開始比較所有模型的性能")
    
    # 運行各模型的基準測試
    psi_results = benchmark_psi_field_model()
    qa_results = benchmark_quantum_analyzer()
    brl_results = benchmark_basic_response_logic()
    
    # 準備比較結果
    comparison = {
        "timestamp": datetime.now().isoformat(),
        "text_sizes": TEXT_SIZES,
        "models": ["PsiFieldModel", "QuantumAnalyzer", "BasicResponseLogic"],
        "times": {
            "PsiFieldModel": psi_results["avg_times"],
            "QuantumAnalyzer": qa_results["avg_times"],
            "BasicResponseLogic": brl_results["avg_times"],
        },
        "memory": {
            "PsiFieldModel": psi_results["avg_memory"],
            "QuantumAnalyzer": qa_results["avg_memory"],
            "BasicResponseLogic": brl_results["avg_memory"],
        }
    }
    
    # 保存比較結果
    save_benchmark_results(comparison, "model_comparison")
    
    # 繪製比較圖表
    if GENERATE_PLOTS:
        # 創建輸出目錄
        os.makedirs(f"{OUTPUT_DIR}/plots", exist_ok=True)
        
        # 繪製時間比較圖
        plt.figure(figsize=(12, 8))
        plt.plot(TEXT_SIZES, psi_results["avg_times"], marker='o', label="PsiFieldModel")
        plt.plot(TEXT_SIZES, qa_results["avg_times"], marker='s', label="QuantumAnalyzer")
        plt.plot(TEXT_SIZES, brl_results["avg_times"], marker='^', label="BasicResponseLogic")
        plt.title("模型處理時間比較")
        plt.xlabel("輸入大小 (字符數)")
        plt.ylabel("處理時間 (秒)")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{OUTPUT_DIR}/plots/model_time_comparison.png")
        
        # 繪製記憶體比較圖
        plt.figure(figsize=(12, 8))
        plt.plot(TEXT_SIZES, psi_results["avg_memory"], marker='o', label="PsiFieldModel")
        plt.plot(TEXT_SIZES, qa_results["avg_memory"], marker='s', label="QuantumAnalyzer")
        plt.plot(TEXT_SIZES, brl_results["avg_memory"], marker='^', label="BasicResponseLogic")
        plt.title("模型記憶體使用比較")
        plt.xlabel("輸入大小 (字符數)")
        plt.ylabel("記憶體使用增量 (MB)")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{OUTPUT_DIR}/plots/model_memory_comparison.png")
    
    logger.info("所有模型性能比較完成")
    return comparison

# =======================================================
# Segment 6: 主程式入口 (Main Entry)
# =======================================================
if __name__ == "__main__":
    logger.info("開始 PSI Runtime SDK 性能基準測試")
    
    try:
        # 比較所有模型的性能
        compare_all_models()
        
        logger.info("所有性能測試已完成")
        logger.info(f"測試結果保存在 {os.path.abspath(OUTPUT_DIR)} 目錄")
    
    except Exception as e:
        logger.error(f"測試過程中發生錯誤: {e}", exc_info=True)
        sys.exit(1) 
