# 高級用法範例

本文檔提供 PSI Runtime SDK 的高級用法範例，幫助您充分利用系統的進階功能。

## 多模態處理

結合文本與圖像進行綜合分析：

```python
from psi_runtime_sdk.multimodal import MultimodalProcessor
from PIL import Image

# 初始化多模態處理器
processor = MultimodalProcessor()

# 載入圖像
image = Image.open("medical_scan.jpg")

# 處理文本與圖像
result = processor.multimodal_analysis(
    text="患者肺部CT掃描顯示可疑結節，需進一步評估",
    image=image
)

# 輸出分析結果
print("多模態分析結果:")
print(f"文本-圖像一致性: {result['text_image_coherence']}")
print(f"診斷建議: {result['diagnostic_suggestion']}")
```

## 領域特定適配

使用醫療領域適配器進行專業醫療文本分析：

```python
from psi_runtime_sdk.domain_adapters import MedicalDomainAdapter

# 初始化醫療領域適配器
adapter = MedicalDomainAdapter(
    medical_knowledge_base_path="medical_kb.db"
)

# 分析醫療文本
medical_text = """
患者，45歲男性，主訴胸痛2天。症狀為間歇性壓榨感，伴有輕微氣促。
既往有高血壓和2型糖尿病病史，目前服用降壓藥和二甲雙胍控制。
家族史顯示父親曾在55歲時患心肌梗塞。
"""

analysis = adapter.analyze_medical_text(medical_text)

# 輸出分析結果
print("醫療文本分析結果:")
print(f"檢測到的症狀: {analysis['symptoms']}")
print(f"可能的診斷: {analysis['possible_diagnoses']}")
print(f"建議的檢查: {analysis['recommended_tests']}")
print(f"風險評估: {analysis['risk_assessment']}")
```

## 分散式處理

使用分散式引擎處理大量文本：

```python
from psi_runtime_sdk.distributed import DistributedPsiEngine

# 初始化分散式引擎
engine = DistributedPsiEngine(num_workers=4)

# 準備批量處理的文本
texts = [
    "探討人工智能在醫療診斷中的應用",
    "量子計算對密碼學的影響",
    "深度學習在自然語言處理中的最新進展",
    "區塊鏈技術如何改變金融行業",
    # ... 更多文本
]

# 批量分析
results = engine.batch_analyze(texts)

# 處理結果
for i, result in enumerate(results):
    print(f"文本 {i+1} 分析結果:")
    print(f"主題: {result['main_topic']}")
    print(f"分析分數: {result['score']}")
    print("---")

# 關閉分散式引擎
engine.shutdown()
```

## 自定義插件開發與使用

創建和使用自定義插件擴展系統功能：

```python
from psi_runtime_sdk.plugin_system import PluginManager, BasePlugin

# 定義自定義插件
class SentimentAnalysisPlugin(BasePlugin):
    def __init__(self):
        super().__init__(name="sentiment_analyzer", version="1.0.0")
        # 初始化情感分析模型
        self.model = self._load_model()
    
    def _load_model(self):
        # 在實際應用中，這裡可以載入預訓練的情感分析模型
        return {"positive": 0.8, "negative": 0.2}  # 簡化示例
    
    def analyze(self, text):
        # 簡單的情感分析邏輯 (實際應用中應使用真實模型)
        positive_words = ["好", "優秀", "喜歡", "贊同", "滿意"]
        negative_words = ["壞", "糟糕", "討厭", "反對", "不滿"]
        
        positive_count = sum(word in text for word in positive_words)
        negative_count = sum(word in text for word in negative_words)
        
        total = positive_count + negative_count
        if total == 0:
            return {"sentiment": "neutral", "confidence": 0.5}
        
        positive_ratio = positive_count / total
        if positive_ratio > 0.6:
            return {"sentiment": "positive", "confidence": positive_ratio}
        elif positive_ratio < 0.4:
            return {"sentiment": "negative", "confidence": 1 - positive_ratio}
        else:
            return {"sentiment": "neutral", "confidence": 0.5}

# 註冊插件
plugin_manager = PluginManager()
plugin_manager.register_plugin("sentiment", SentimentAnalysisPlugin())

# 使用插件
plugin = plugin_manager.get_plugin("sentiment")
sentiment_result = plugin.analyze("我非常喜歡這個產品，使用體驗很優秀")

print("情感分析結果:")
print(f"情感傾向: {sentiment_result['sentiment']}")
print(f"置信度: {sentiment_result['confidence']}")
```

## 高級配置與性能調優

調整系統參數以優化性能：

```python
from psi_field import PsiFieldModel
from quantum_engine import QuantumAnalyzer, Config as QAConfig

# 高級 PsiFieldModel 配置
psi_model = PsiFieldModel(config={
    "use_advanced": True,
    "field_dimension": 256,       # 增加維度以提高表達能力
    "stability_threshold": 0.9,   # 提高穩定性閾值
    "enable_detailed_logging": True,
    "cache_size": 1024,           # 增加緩存大小
    "max_active_knowledge": 50,   # 增加最大激活知識點數量
    "tensor_parallelism": True,   # 啟用張量並行
    "use_gpu": True               # 啟用 GPU 加速
})

# 高級 QuantumAnalyzer 配置
qa_config = QAConfig(
    log_level=10,
    mode="experimental",          # 使用實驗性模式
    tensor_precision="float16",   # 降低精度以提高性能
    max_dimension=128,            # 設置量子態最大維度
    use_approximate=True,         # 使用近似計算
    parallel_threads=8            # 並行線程數
)
qa_analyzer = QuantumAnalyzer(qa_config)

# 長文本處理
long_text = """
人工智能(AI)與量子計算的結合正在開創新的計算範式。量子機器學習算法可以處理傳統算法難以應對的複雜問題，
特別是在大規模數據集上的模式識別與優化問題。量子神經網絡可能比經典神經網絡具有指數級的表達能力，
但面臨量子退相干、量子誤差校正等挑戰。目前研究重點包括量子變分電路、量子核方法及混合量子-經典算法。
未來可能出現的量子AI系統將解鎖現有系統無法觸及的應用領域，如複雜分子模擬、加密分析和金融模型優化。
然而，這一領域仍處於早期階段，需要更多理論突破與實驗驗證。
"""

# 使用優化配置處理長文本
psi_result = psi_model.process(long_text)
qa_result = qa_analyzer.comprehensive_analysis(long_text)

print("高級配置處理結果:")
print(f"語義場維度: {psi_result['semantic_field']['dimensions']}")
print(f"激活知識點數量: {psi_result['semantic_field']['active_knowledge_count']}")
print(f"量子分析整合分數: {qa_result['integrated_score']}")
```

## 深度整合範例

將 PSI Runtime SDK 與現有 AI 模型和系統深度整合：

```python
import json
from psi_field import PsiFieldModel
from quantum_engine import QuantumAnalyzer
from logic_core import BasicResponseLogic, Config

# 假設這是外部 AI 系統的模擬接口
class ExternalAISystem:
    def generate_response(self, prompt):
        return f"這是對'{prompt}'的模擬回應。"

# 初始化
psi_model = PsiFieldModel(config={"use_advanced": True})
quantum_analyzer = QuantumAnalyzer()
logic_engine = BasicResponseLogic()
external_ai = ExternalAISystem()

def enhanced_ai_system(user_input, conversation_history=None):
    """
    增強型 AI 系統，整合 PSI Runtime SDK 與外部 AI
    """
    conversation_history = conversation_history or []
    
    # 步驟 1: 語義場分析
    semantic_result = psi_model.process(user_input)
    field_type = semantic_result["semantic_field"]["field_type"]
    field_tension = semantic_result["semantic_field"]["tension"]
    
    # 步驟 2: 量子分析
    quantum_result = quantum_analyzer.comprehensive_analysis(user_input)
    coherence = quantum_result.get("coherence", 0.5)
    
    # 步驟 3: 構建增強提示
    context = "\n".join(conversation_history[-5:])  # 最近5條對話
    insights = ", ".join(semantic_result["insights"])
    
    enhanced_prompt = f"""
    用戶輸入: {user_input}
    
    上下文: {context}
    
    語義分析:
    - 場類型: {field_type}
    - 張力: {field_tension}
    - 一致性: {coherence}
    - 洞察: {insights}
    
    請基於以上信息提供回應:
    """
    
    # 步驟 4: 調用外部 AI 系統
    ai_response = external_ai.generate_response(enhanced_prompt)
    
    # 步驟 5: 評估回應質量
    evaluation = logic_engine.evaluate_response(ai_response, {"query": user_input})
    
    # 步驟 6: 返回結果與元信息
    return {
        "response": ai_response,
        "metadata": {
            "field_type": field_type,
            "field_tension": field_tension,
            "coherence": coherence,
            "evaluation": evaluation,
            "insights": semantic_result["insights"]
        }
    }

# 使用示例
conversation = [
    "你好，我想了解量子計算。",
    "量子計算使用量子位而非傳統位元，可進行疊加和糾纏，處理複雜計算。"
]

user_query = "量子計算在金融領域有什麼應用前景？"
result = enhanced_ai_system(user_query, conversation)

print(json.dumps(result, indent=2, ensure_ascii=False))
```

## 性能基準測試

進行系統性能基準測試：

```python
from psi_runtime_sdk.benchmarks import performance_benchmark

# 配置基準測試
config = {
    "text_sizes": [100, 500, 1000, 5000, 10000],  # 文本大小（字符數）
    "repeat_count": 5,                            # 每個測試重複次數
    "generate_plots": True,                       # 生成圖表
    "output_dir": "benchmark_results"             # 結果輸出目錄
}

# 運行基準測試
results = performance_benchmark.run_benchmarks(config)

# 輸出摘要
print("性能基準測試結果摘要:")
for model_name, model_results in results["models"].items():
    print(f"\n{model_name}:")
    print(f"  平均處理時間: {model_results['avg_time']:.4f} 秒")
    print(f"  平均記憶體使用: {model_results['avg_memory']:.2f} MB")
    print(f"  最大文本大小處理時間: {model_results['max_time']:.4f} 秒")
```

這些高級範例展示了 PSI Runtime SDK 的強大功能和靈活性。通過這些範例，您可以深入了解系統的進階用法，並根據您的特定需求進行定制和優化。 
