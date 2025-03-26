"""
QuantumAnalyzer 單元測試
"""
import pytest
import numpy as np
from quantum_engine import QuantumAnalyzer, Config, DataParser

class TestQuantumAnalyzer:
    @pytest.fixture
    def qa_engine(self):
        """創建測試用的量子分析器"""
        config = Config(log_level=30)  # 設置為WARNING級別，減少測試輸出
        return QuantumAnalyzer(config)
    
    def test_init(self, qa_engine):
        """測試初始化"""
        assert qa_engine is not None
        assert qa_engine.config is not None
        assert hasattr(qa_engine, "brl")  # 確認有 BasicResponseLogic 實例
    
    def test_parse_input(self, qa_engine):
        """測試輸入解析"""
        text = "測試量子分析功能"
        parsed = qa_engine.parse_input(text)
        
        assert isinstance(parsed, dict)
        assert "text" in parsed
        assert parsed["text"] == text
    
    def test_run_inference_quantum(self, qa_engine):
        """測試純量子分析模式"""
        input_text = "分析未來技術發展趨勢"
        result = qa_engine.run_inference(input_text, use_basic_logic=False)
        
        assert isinstance(result, float)
        assert 0 <= result <= 1.0
    
    def test_run_inference_basic(self, qa_engine):
        """測試基礎邏輯分析模式"""
        input_text = "分析未來技術發展趨勢"
        result = qa_engine.run_inference(input_text, use_basic_logic=True)
        
        assert isinstance(result, dict)
        assert "final_result" in result
        assert isinstance(result["final_result"], float)
        assert 0 <= result["final_result"] <= 1.0
    
    def test_comprehensive_analysis(self, qa_engine):
        """測試綜合分析功能"""
        input_text = "分析未來技術發展趨勢"
        result = qa_engine.comprehensive_analysis(input_text)
        
        assert isinstance(result, dict)
        assert "integrated_score" in result
        assert "quantum_result" in result
        assert "basic_result" in result
        assert isinstance(result["integrated_score"], float)
        assert 0 <= result["integrated_score"] <= 1.0
    
    def test_integrate_results(self, qa_engine):
        """測試結果整合功能"""
        quantum_result = 0.75
        basic_result = {"final_result": 0.65, "context": {"timestamp": "2025-01-01"}}
        
        integrated = qa_engine.integrate_results(quantum_result, basic_result)
        
        assert isinstance(integrated, dict)
        assert "integrated_score" in integrated
        assert integrated["integrated_score"] == 0.75 * 0.5 + 0.65 * 0.5
        assert "suggestions" in integrated
        assert "quantum_insight" in integrated["suggestions"] 
