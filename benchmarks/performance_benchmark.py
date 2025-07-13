#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =======================================================
# Segment 1: 模組說明 (Module Docstring)
# =======================================================
"""
PSI Runtime SDK 性能基準測試框架

本模組提供一個可擴展、可配置的框架，用於測量 PSI Runtime SDK
及其他相關組件的性能指標。

核心功能：
- **性能測試**: 測量給定目標在不同負載下的處理時間與記憶體增量。
- **結果報告**: 將測試結果自動保存為結構化的 JSON 檔案。
- **視覺化分析**: 自動生成處理時間與記憶體使用的性能趨勢圖。
- **模型比較**: 在統一的環境下對多個模型或組件進行橫向比較。

設計理念：
- **抽象化測試目標**: 使用 `BenchmarkTarget` 抽象類別，將任何可測試的
  單元（模型、函數）標準化，消除程式碼重複。
- **職責分離 (SoC)**: 將測試執行器 (Runner)、性能測量器 (Measurer)
  和報告生成器 (Reporter) 拆分為獨立組件。
- **配置驅動**: 所有測試參數（如輸入大小、重複次數）均由一個
  `BenchmarkConfig` 資料類別集中管理。
- **結構化資料模型**: 使用 `@dataclass` 定義測試結果，確保資料的
  一致性與可追溯性。

版本：2.0.0
作者：Reagan Fu 開發團隊 (Refactored by AI Assistant)
更新日期：2025-07-14
"""

# =======================================================
# Segment 2: 模組匯入與基礎設置 (Imports & Setup)
# =======================================================
# --- 標準庫 ---
import gc
import json
import logging
import os
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Tuple

# --- 第三方庫 ---
import matplotlib.pyplot as plt
import numpy as np
import psutil

# --- 待測 SDK 模組 ---
# 假設專案已正確安裝或路徑已配置
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic_core.basic_response_logic import BasicResponseLogic, Config as BRLConfig
# 替換為重構後的 QuantumFusionEngine
from quantum_engine import QuantumFusionEngine, EngineConfig
# PsiFieldModel 假設存在
# from psi_field import PsiFieldModel

# --- 日誌配置 ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s] %(message)s",
    handlers=[
        logging.FileHandler("benchmark.log", mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# =======================================================
# Segment 3: 基準測試配置 (Benchmark Configuration)
# =======================================================
@dataclass
class BenchmarkConfig:
    """集中管理所有基準測試的參數。"""
    text_sizes: List[int] = field(default_factory=lambda: [100, 500, 1000, 5000, 10000])
    repeat_count: int = 5
    output_dir: str = "benchmark_results"
    generate_plots: bool = True
    
    def __post_init__(self):
        """配置初始化後，建立輸出目錄。"""
        Path(self.output_dir).mkdir(exist_ok=True)
        if self.generate_plots:
            Path(self.output_dir, "plots").mkdir(exist_ok=True)
        logger.info(f"Benchmark configured. Results will be saved to '{self.output_dir}'.")

# =======================================================
# Segment 4: 資料結構模型 (Data Models)
# =======================================================
@dataclass
class PerformanceMetrics:
    """單次執行的性能指標。"""
    elapsed_time_s: float
    memory_increase_mb: float

@dataclass
class SizeBenchmarkResult:
    """單一輸入大小的所有重複測試結果。"""
    size: int
    avg_time_s: float
    avg_memory_mb: float
    all_runs: List[PerformanceMetrics]

@dataclass
class TargetBenchmarkResult:
    """單一測試目標的完整基準測試結果。"""
    target_name: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    results_by_size: List[SizeBenchmarkResult] = field(default_factory=list)

@dataclass
class SuiteBenchmarkResult:
    """整個測試套件的結果，包含多個目標的比較。"""
    suite_name: str
    config: BenchmarkConfig
    all_target_results: List[TargetBenchmarkResult]

# =======================================================
# Segment 5: 測試目標抽象化 (Test Target Abstraction)
# =======================================================
class BenchmarkTarget(ABC):
    """
    測試目標的抽象基礎類別 (策略模式)。
    - 將任何需要測試的物件或函數封裝成一個標準化、可執行的目標。
    """
    @property
    @abstractmethod
    def name(self) -> str:
        """返回測試目標的唯一名稱。"""
        pass

    @abstractmethod
    def setup(self) -> Callable[[str], Any]:
        """
        準備測試環境並返回一個可呼叫的測試函數。
        該函數應接受一個字串（測試文本）作為輸入。
        """
        pass

# --- 具體測試目標實現 ---

class QuantumFusionEngineTarget(BenchmarkTarget):
    """測試 QuantumFusionEngine 的目標。"""
    @property
    def name(self) -> str:
        return "QuantumFusionEngine"

    def setup(self) -> Callable[[str], Any]:
        config = EngineConfig()
        engine = QuantumFusionEngine(config)
        return engine.analyze

class BasicResponseLogicTarget(BenchmarkTarget):
    """測試 BasicResponseLogic 的目標。"""
    @property
    def name(self) -> str:
        return "BasicResponseLogic"

    def setup(self) -> Callable[[str], Any]:
        engine = BasicResponseLogic()
        config = BRLConfig(debug_mode=False)
        # 使用 lambda 將多參數函數轉換為單參數函數
        return lambda text: engine.run(text, config)

# class PsiFieldModelTarget(BenchmarkTarget):
#     """測試 PsiFieldModel 的目標 (範例)。"""
#     @property
#     def name(self) -> str:
#         return "PsiFieldModel"
#
#     def setup(self) -> Callable[[str], Any]:
#         model = PsiFieldModel(config={"use_advanced": False})
#         return model.process

# =======================================================
# Segment 6: 核心服務組件 (Core Service Components)
# =======================================================
class DataGenerator:
    """負責生成測試資料。"""
    @staticmethod
    def generate_test_text(size: int) -> str:
        words = ["人工智能", "語義場", "量子分析", "語境穩定相位", "知識解鎖", "動態演化"]
        text = ""
        # 使用確定性種子，確保每次測試的文本內容相同
        rng = np.random.default_rng(seed=size)
        while len(text) < size:
            text += rng.choice(words) + " "
        return text[:size]

class PerformanceMeasurer:
    """負責精確測量單次函數執行的性能。"""
    @staticmethod
    def measure(func: Callable, *args, **kwargs) -> Tuple[PerformanceMetrics, Any]:
        gc.collect()
        process = psutil.Process(os.getpid())
        mem_before_mb = process.memory_info().rss / (1024 * 1024)
        
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_time_s = time.perf_counter() - start_time
        
        mem_after_mb = process.memory_info().rss / (1024 * 1024)
        memory_increase_mb = max(0, mem_after_mb - mem_before_mb)
        
        metrics = PerformanceMetrics(
            elapsed_time_s=elapsed_time_s,
            memory_increase_mb=memory_increase_mb
        )
        return metrics, result

class ReportGenerator:
    """負責生成 JSON 報告和視覺化圖表。"""
    def __init__(self, output_dir: str, generate_plots: bool):
        self.output_dir = Path(output_dir)
        self.plots_dir = self.output_dir / "plots"
        self.generate_plots = generate_plots

    def generate(self, suite_result: SuiteBenchmarkResult):
        """生成所有報告和圖表。"""
        self._save_json_report(suite_result)
        if self.generate_plots:
            self._plot_comparison_charts(suite_result)

    def _save_json_report(self, suite_result: SuiteBenchmarkResult):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"{suite_result.suite_name}_{timestamp}.json"
        with filename.open('w', encoding='utf-8') as f:
            json.dump(asdict(suite_result), f, indent=2, ensure_ascii=False)
        logger.info(f"Benchmark suite results saved to: {filename}")

    def _plot_comparison_charts(self, suite_result: SuiteBenchmarkResult):
        text_sizes = suite_result.config.text_sizes
        
        fig_time, ax_time = plt.subplots(figsize=(12, 8))
        fig_mem, ax_mem = plt.subplots(figsize=(12, 8))
        
        markers = ['o', 's', '^', 'D', 'v', '<', '>']

        for i, target_result in enumerate(suite_result.all_target_results):
            marker = markers[i % len(markers)]
            times = [r.avg_time_s for r in target_result.results_by_size]
            memory = [r.avg_memory_mb for r in target_result.results_by_size]
            
            ax_time.plot(text_sizes, times, marker=marker, label=target_result.target_name)
            ax_mem.plot(text_sizes, memory, marker=marker, label=target_result.target_name)
            
        self._finalize_plot(ax_time, "Model Processing Time Comparison", "Input Size (characters)", "Avg. Time (s)")
        self._finalize_plot(ax_mem, "Model Memory Usage Comparison", "Input Size (characters)", "Avg. Memory Increase (MB)")
        
        fig_time.savefig(self.plots_dir / "comparison_time.png")
        fig_mem.savefig(self.plots_dir / "comparison_memory.png")
        
        plt.close(fig_time)
        plt.close(fig_mem)
        logger.info(f"Comparison plots saved to: {self.plots_dir}")

    def _finalize_plot(self, ax, title: str, xlabel: str, ylabel: str):
        ax.set_title(title, fontsize=16)
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.legend()
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)

# =======================================================
# Segment 7: 基準測試執行器 (Benchmark Runner)
# =======================================================
class BenchmarkRunner:
    """
    協調整個基準測試流程的執行器。
    """
    def __init__(self, config: BenchmarkConfig):
        self.config = config
        self.reporter = ReportGenerator(config.output_dir, config.generate_plots)

    def run_suite(self, targets: List[BenchmarkTarget], suite_name: str = "ModelComparison"):
        """
        對一組測試目標執行完整的基準測試套件。
        """
        logger.info(f"--- Starting Benchmark Suite: {suite_name} ---")
        suite_result = SuiteBenchmarkResult(suite_name=suite_name, config=self.config, all_target_results=[])

        for target in targets:
            target_result = self._run_for_target(target)
            suite_result.all_target_results.append(target_result)
        
        self.reporter.generate(suite_result)
        logger.info(f"--- Benchmark Suite: {suite_name} Finished ---")

    def _run_for_target(self, target: BenchmarkTarget) -> TargetBenchmarkResult:
        logger.info(f"--- Benchmarking Target: {target.name} ---")
        test_function = target.setup()
        target_result = TargetBenchmarkResult(target_name=target.name)

        for size in self.config.text_sizes:
            logger.info(f"Testing with input size: {size} characters")
            test_text = DataGenerator.generate_test_text(size)
            
            runs_metrics: List[PerformanceMetrics] = []
            for i in range(self.config.repeat_count):
                metrics, _ = PerformanceMeasurer.measure(test_function, test_text)
                runs_metrics.append(metrics)
                logger.debug(f"  Run {i+1}/{self.config.repeat_count}: "
                             f"Time={metrics.elapsed_time_s:.4f}s, "
                             f"Memory={metrics.memory_increase_mb:.2f}MB")
            
            avg_time = np.mean([m.elapsed_time_s for m in runs_metrics])
            avg_memory = np.mean([m.memory_increase_mb for m in runs_metrics])
            
            size_result = SizeBenchmarkResult(
                size=size,
                avg_time_s=avg_time,
                avg_memory_mb=avg_memory,
                all_runs=runs_metrics
            )
            target_result.results_by_size.append(size_result)
            logger.info(f"  Average for size {size}: Time={avg_time:.4f}s, Memory={avg_memory:.2f}MB")
        
        logger.info(f"--- Finished Benchmarking Target: {target.name} ---")
        return target_result

# =======================================================
# Segment 8: 主程式入口 (Main Entry)
# =======================================================
def main():
    """主執行函數。"""
    logger.info("Initializing PSI Runtime SDK Benchmark Framework.")
    
    try:
        # 1. 建立測試配置
        config = BenchmarkConfig()
        
        # 2. 定義所有要測試的目標
        #    擴展：若要測試新模型，只需在此處新增一個 Target 實例。
        targets_to_test = [
            QuantumFusionEngineTarget(),
            BasicResponseLogicTarget(),
            # PsiFieldModelTarget(), # 如需測試，取消此行註解
        ]
        
        # 3. 建立並運行基準測試執行器
        runner = BenchmarkRunner(config)
        runner.run_suite(targets_to_test)
        
        logger.info("All benchmark tests completed successfully.")
        logger.info(f"Check the '{config.output_dir}' directory for detailed results.")

    except Exception as e:
        logger.critical(f"A critical error occurred during the benchmark process: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
