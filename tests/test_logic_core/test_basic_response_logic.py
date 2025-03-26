"""
BasicResponseLogic 單元測試
"""
import pytest
import numpy as np
from psi_runtime_sdk.logic_core import BasicResponseLogic, Config, DataParser

class TestBasicResponseLogic:
    @pytest.fixture
    def brl_engine(self):
        """創建測試用的 BRL 引擎"""
        return BasicResponseLogic()
    
    @pytest.fixture
    def default_config(self):
        """創建默認配置"""
        return Config(timestamp="2025-03-12T00:00:00", debug_mode=True)
    
    def test_init(self, brl_engine):
        """測試初始化"""
        assert brl_engine is not None
        assert brl_engine.memory_states == []
        assert brl_engine.iteration_counter == 0
    
    def test_parse_and_embed(self, brl_engine):
        """測試輸入解析與向量化"""
        input_text = "測試輸入文本"
        h_t, intent, H_p_c = brl_engine._parse_and_embed(input_text)
        
        # 檢查基本屬性
        assert isinstance(h_t, np.ndarray)
        assert isinstance(intent, int)
        assert isinstance(H_p_c, float)
        assert 0 <= intent < 10  # 假設意圖數量為10
        assert 0 <= H_p_c <= 1.0  # 熵應該在0到1之間
    
    def test_simulate_quantum_attention(self, brl_engine):
        """測試量子態演化與注意力機制"""
        state_0 = np.random.rand(10)
        evolved_state, H_evolved = brl_engine._simulate_quantum_attention(state_0)
        
        assert isinstance(evolved_state, np.ndarray)
        assert isinstance(H_evolved, float)
        assert evolved_state.shape == state_0.shape
        assert 0 <= H_evolved <= np.log2(10) + 0.1  # 10維向量的最大熵加一點誤差空間
    
    def test_run_inference(self, brl_engine, default_config):
        """測試完整推理流程"""
        input_text = "請分析未來市場趨勢"
        result = brl_engine.run(input_text, default_config)
        
        # 檢查結果結構
        assert isinstance(result, dict)
        assert "final_result" in result
        assert 0 <= result["final_result"] <= 1.0
        assert "suggestions" in result
        assert "context" in result
        
    def test_reset(self, brl_engine):
        """測試重置功能"""
        # 先執行一些操作，填充記憶
        brl_engine.memory_states = [np.random.rand(10) for _ in range(3)]
        brl_engine.iteration_counter = 5
        
        # 執行重置
        brl_engine.reset()
        
        # 檢查重置後的狀態
        assert brl_engine.memory_states == []
        assert brl_engine.iteration_counter == 0 
