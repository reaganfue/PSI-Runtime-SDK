"""
========================================
Segment 1: 模組說明 (Module Docstring)
========================================
BasicResponseLogic 單元測試模組

本模組用於驗證 BasicResponseLogic 核心引擎的各項功能，包括：
    - 輸入解析與向量化處理
    - 量子態演化與注意力機制模擬
    - 完整推理流程運作
    - 重置功能檢查

版本: 1.0.0
作者: 測試團隊
許可證: Proprietary
"""

import pytest
import numpy as np
import logging

# ========================================
# Segment 2: 模組匯入與基礎設置 (Imports & Setup)
# ========================================
# 設置日誌配置與全域常數
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 修改導入路徑以匹配實際目錄結構
from logic_core import BasicResponseLogic, Config, DataParser

# ========================================
# Segment 3: 測試案例與測試環境設置 (Test Cases & Environment Setup)
# ========================================
class TestBasicResponseLogic:
    @pytest.fixture
    def brl_engine(self):
        """
        創建測試用的 BasicResponseLogic 引擎實例。

        返回:
            BasicResponseLogic: 基本邏輯推理引擎實例。
        """
        engine = BasicResponseLogic()
        logger.info("BasicResponseLogic 引擎已初始化")
        return engine

    @pytest.fixture
    def default_config(self):
        """
        創建默認配置。

        返回:
            Config: 配置對象，包含時間戳與調試模式設置。
        """
        config = Config(timestamp="2025-03-12T00:00:00", debug_mode=True)
        logger.info("默認配置已初始化: %s", config.__dict__)
        return config

    def test_init(self, brl_engine):
        """
        測試 BasicResponseLogic 的初始化狀態。

        驗證:
            - 引擎實例不為 None
            - memory_states 初始為空列表
            - iteration_counter 初始為 0
        """
        assert brl_engine is not None, "引擎實例不應為 None"
        assert brl_engine.memory_states == [], "memory_states 初始應為空列表"
        assert brl_engine.iteration_counter == 0, "iteration_counter 初始應為 0"
        logger.info("初始化測試通過")

    def test_parse_and_embed(self, brl_engine):
        """
        測試輸入解析與向量化處理功能。

        流程:
            1. 傳入測試文本
            2. 解析並嵌入文本以獲取向量 h_t、意圖標識 intent 及熵 H_p_c

        驗證:
            - h_t 為 numpy.ndarray 類型
            - intent 為 int 且在 0 至 9 之間（假設意圖數量為 10）
            - H_p_c 為 float 且在 0 至 1.0 之間
        """
        input_text = "測試輸入文本"
        h_t, intent, H_p_c = brl_engine._parse_and_embed(input_text)
        logger.info("解析與向量化結果: h_t=%s, intent=%s, H_p_c=%s", h_t, intent, H_p_c)

        assert isinstance(h_t, np.ndarray), "h_t 必須為 numpy.ndarray 類型"
        assert isinstance(intent, int), "intent 必須為 int 類型"
        assert isinstance(H_p_c, float), "H_p_c 必須為 float 類型"
        assert 0 <= intent < 10, "intent 超出預期範圍"
        assert 0 <= H_p_c <= 1.0, "H_p_c 超出有效範圍"

    def test_simulate_quantum_attention(self, brl_engine):
        """
        測試量子態演化與注意力機制模擬功能。

        流程:
            1. 傳入隨機初始狀態 state_0
            2. 模擬量子態演化，獲取演化後的狀態 evolved_state 及熵 H_evolved

        驗證:
            - evolved_state 為 numpy.ndarray 且形狀與 state_0 相同
            - H_evolved 為 float 且在 0 至 np.log2(10) + 誤差範圍內（10 維向量最大熵）
        """
        state_0 = np.random.rand(10)
        evolved_state, H_evolved = brl_engine._simulate_quantum_attention(state_0)
        logger.info("量子注意力模擬結果: evolved_state=%s, H_evolved=%s", evolved_state, H_evolved)

        assert isinstance(evolved_state, np.ndarray), "evolved_state 必須為 numpy.ndarray 類型"
        assert isinstance(H_evolved, float), "H_evolved 必須為 float 類型"
        assert evolved_state.shape == state_0.shape, "evolved_state 形狀應與 state_0 相同"
        max_entropy = np.log2(10)
        assert 0 <= H_evolved <= max_entropy + 0.1, "H_evolved 超出預期熵範圍"

    def test_run_inference(self, brl_engine, default_config):
        """
        測試完整推理流程。

        流程:
            1. 傳入測試輸入文本
            2. 執行 run 方法進行推理

        驗證:
            - 返回結果為字典
            - 結果包含 "final_result", "suggestions" 與 "context" 關鍵字
            - final_result 在 0 到 1.0 之間
        """
        input_text = "請分析未來市場趨勢"
        result = brl_engine.run(input_text, default_config)
        logger.info("推理結果: %s", result)

        assert isinstance(result, dict), "推理結果必須為字典"
        assert "final_result" in result, "結果缺少 'final_result' 關鍵字"
        assert 0 <= result["final_result"] <= 1.0, "final_result 超出有效範圍"
        assert "suggestions" in result, "結果缺少 'suggestions' 關鍵字"
        assert "context" in result, "結果缺少 'context' 關鍵字"

    def test_reset(self, brl_engine):
        """
        測試重置功能。

        流程:
            1. 模擬部分記憶狀態與迭代計數
            2. 調用 reset 方法重置引擎

        驗證:
            - memory_states 被重置為空列表
            - iteration_counter 被重置為 0
        """
        # 模擬填充記憶狀態與迭代計數
        brl_engine.memory_states = [np.random.rand(10) for _ in range(3)]
        brl_engine.iteration_counter = 5
        logger.info("重置前狀態: memory_states=%s, iteration_counter=%s", brl_engine.memory_states, brl_engine.iteration_counter)
        
        # 執行重置操作
        brl_engine.reset()
        logger.info("重置後狀態: memory_states=%s, iteration_counter=%s", brl_engine.memory_states, brl_engine.iteration_counter)
        
        assert brl_engine.memory_states == [], "重置後 memory_states 應為空列表"
        assert brl_engine.iteration_counter == 0, "重置後 iteration_counter 應為 0"
