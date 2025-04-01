# 快速入門指南

本指南將幫助您快速上手 PSI Runtime SDK，了解其基本功能與用法。

## 安裝

首先，使用 pip 安裝 PSI Runtime SDK：

```bash
pip install psi-runtime-sdk
```

若需要完整功能（包括 API、命令行工具與可視化功能），可安裝完整版：

```bash
pip install "psi-runtime-sdk[full]"
```

## 基本使用

### 語義場分析

以下是使用 `PsiFieldModel` 進行語義場分析的基本示例：

```python
from psi_field import PsiFieldModel

# 初始化語義場模型
model = PsiFieldModel()

# 分析文本
result = model.process("探索人工智能與量子計算的結合點，以及在自然語言處理中的應用前景。")

# 輸出分析結果
print("語義場張力:", result["semantic_field"]["tension"])
print("穩定性分數:", result["semantic_field"]["stability_score"])
print("場類型:", result["semantic_field"]["field_type"])
print("\n關鍵詞:", result["keywords"])
print("\n洞察:")
for insight in result["insights"]:
    print(f"- {insight}")
```

### 量子分析

使用 `QuantumAnalyzer` 進行量子分析：

```python
from quantum_engine import QuantumAnalyzer

# 初始化量子分析器
analyzer = QuantumAnalyzer()

# 執行綜合分析
result = analyzer.comprehensive_analysis("量子計算在密碼學中的應用，以及對現有加密系統的潛在威脅。")

# 輸出分析結果
print("整合分析分數:", result["integrated_score"])
print("\n洞察:")
for insight in result["insights"]:
    print(f"- {insight}")
```

### 基礎邏輯推理

使用 `BasicResponseLogic` 進行邏輯推理：

```python
from logic_core import BasicResponseLogic, Config

# 創建配置
config = Config(timestamp="2025-03-12T00:00:00")

# 初始化推理引擎
engine = BasicResponseLogic()

# 執行推理
result = engine.run("分析未來十年人工智能發展方向及可能的突破點", config)

# 輸出推理結果
print("生成回應:", result["generated_response"])
print("回應置信度:", result["confidence"])
```

## 參數配置

各模組可通過配置對象進行自定義設置：

```python
from psi_field import PsiFieldModel
from quantum_engine import QuantumAnalyzer, Config as QAConfig
from logic_core import BasicResponseLogic, Config as BRLConfig

# 語義場模型配置
psi_model = PsiFieldModel(config={
    "use_advanced": True,
    "field_dimension": 128,
    "stability_threshold": 0.85
})

# 量子分析器配置
qa_config = QAConfig(log_level=10, mode="advanced")
qa_analyzer = QuantumAnalyzer(qa_config)

# 基礎邏輯推理配置
brl_config = BRLConfig(debug_mode=True, output_format="detailed")
brl_engine = BasicResponseLogic()
```

## 組合使用

PSI Runtime SDK 的真正威力在於組合使用各個模組：

```python
from psi_field import PsiFieldModel
from quantum_engine import QuantumAnalyzer
from logic_core import BasicResponseLogic, Config

# 初始化各組件
psi_model = PsiFieldModel(config={"use_advanced": True})
qa_analyzer = QuantumAnalyzer()
logic_engine = BasicResponseLogic()
logic_config = Config()

# 輸入文本
text = "探討量子計算與人工智能結合的可能性，以及對未來科技發展的影響"

# 步驟1: 使用語義場模型解析文本
semantic_result = psi_model.process(text)
keywords = semantic_result["keywords"]
field_type = semantic_result["semantic_field"]["field_type"]

# 步驟2: 使用量子分析器深入分析
quantum_result = qa_analyzer.comprehensive_analysis(text)
integrated_score = quantum_result["integrated_score"]
insights = quantum_result.get("insights", [])

# 步驟3: 使用基礎邏輯引擎生成回應
logic_result = logic_engine.run(text, logic_config)
response = logic_result["generated_response"]

# 步驟4: 綜合所有結果
print(f"輸入文本: {text}")
print(f"\n關鍵詞: {', '.join(keywords)}")
print(f"語義場類型: {field_type}")
print(f"整合分析分數: {integrated_score}")
print("\n關鍵洞察:")
for insight in insights:
    print(f"- {insight}")
print(f"\n生成回應: {response}")
```

## 下一步

現在您已經了解了 PSI Runtime SDK 的基本用法，可以進一步探索：

- [高級用法範例](advanced_usage.md) - 了解更多高級功能
- [API 參考](../api/psi_field.md) - 詳細的 API 參考文檔
- [架構概述](../architecture.md) - 了解系統架構設計
- [核心概念](../concepts.md) - 深入理解語義場理論與量子分析 
