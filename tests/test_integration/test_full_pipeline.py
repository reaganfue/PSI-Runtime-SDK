"""
PSI Runtime SDK 整合測試
"""
import pytest
from logic_core import BasicResponseLogic, Config as BRLConfig
from psi_field import SemanticFieldEngine, FieldConfig, DataParser as PsiDataParser
from quantum_engine import QuantumAnalyzer, Config as QAConfig

class TestIntegration:
    @pytest.fixture
    def all_engines(self):
        """初始化所有引擎"""
        brl_config = BRLConfig(debug_mode=False)
        field_config = FieldConfig(enable_detailed_logging=False)
        qa_config = QAConfig(log_level=30)
        
        return {
            "brl": BasicResponseLogic(),
            "field": SemanticFieldEngine(field_config),
            "qa": QuantumAnalyzer(qa_config),
            "brl_config": brl_config,
            "field_config": field_config,
            "qa_config": qa_config
        }
    
    def test_basic_to_quantum_flow(self, all_engines):
        """測試從基礎邏輯到量子分析的流程"""
        # 1. 使用 BRL 進行初步分析
        input_text = "分析人工智能對未來五年的影響"
        brl_result = all_engines["brl"].run(input_text, all_engines["brl_config"])
        
        # 驗證 BRL 結果
        assert isinstance(brl_result, dict)
        assert "final_result" in brl_result
        
        # 2. 將結果傳遞給量子分析器
        qa_result = all_engines["qa"].run_inference(input_text, use_basic_logic=False)
        
        # 驗證量子分析結果
        assert isinstance(qa_result, float)
        
        # 3. 測試流程的連貫性（這裡僅作示意）
        assert 0 <= brl_result["final_result"] <= 1.0
        assert 0 <= qa_result <= 1.0
    
    def test_field_to_quantum_flow(self, all_engines):
        """測試從語義場到量子分析的流程"""
        # 1. 使用語義場引擎解鎖知識
        input_text = "量子計算和神經網絡的融合應用"
        semantic_input = PsiDataParser.parse(input_text)
        unlocked_keys = all_engines["field"].psi_engine.unlock_knowledge(semantic_input)
        
        # 驗證解鎖結果
        assert isinstance(unlocked_keys, list)
        assert len(unlocked_keys) > 0
        
        # 2. 將結果提供給量子分析器
        # 在實際應用中，這裡可能需要將知識點集成到量子分析中
        # 這裡僅作示意
        qa_result = all_engines["qa"].run_inference(input_text, use_basic_logic=False)
        
        # 驗證量子分析結果
        assert isinstance(qa_result, float)
    
    def test_full_pipeline(self, all_engines):
        """測試完整的分析流水線"""
        input_text = "分析量子計算對密碼學的影響"
        
        # 1. 語義場處理
        semantic_input = PsiDataParser.parse(input_text)
        unlocked_keys = all_engines["field"].psi_engine.unlock_knowledge(semantic_input)
        
        # 2. 量子分析
        qa_result = all_engines["qa"].comprehensive_analysis(input_text)
        
        # 3. 基礎邏輯分析
        brl_result = all_engines["brl"].run(input_text, all_engines["brl_config"])
        
        # 4. 整合結果
        integrated_result = {
            "query": input_text,
            "unlocked_knowledge": unlocked_keys,
            "quantum_analysis": qa_result,
            "logical_analysis": brl_result,
            "confidence": (qa_result.get("integrated_score", 0.5) + 
                          brl_result.get("final_result", 0.5)) / 2
        }
        
        # 驗證整合結果
        assert isinstance(integrated_result, dict)
        assert "confidence" in integrated_result
        assert 0 <= integrated_result["confidence"] <= 1.0
        assert "unlocked_knowledge" in integrated_result
        assert "quantum_analysis" in integrated_result
        assert "logical_analysis" in integrated_result 
