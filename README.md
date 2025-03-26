# PSI Runtime SDK

## 概述

PSI Runtime SDK 是一個尖端實驗性框架，結合量子啟發式推理與語義場分析技術，為高級人機協同推理應用提供強大支持。本 SDK 實現了多層次的認知模型，包括基礎響應邏輯、語義場分析與量子分析引擎，為下一代智能系統提供創新思路與實現基礎。

## 專案結構

```
PsiRuntimeSDK/
├── README.md                  # 專案說明文件
├── pyproject.toml             # 構建系統配置
├── requirements.txt           # 依賴項清單
├── setup.py                   # 安裝腳本
├── pytest.ini                 # 測試配置文件
│
├── psi_runtime_sdk/           # 主要套件目錄
│   ├── __init__.py            # 套件初始化文件 (包含頂層導入)
│   │
│   ├── logic_core/            # 基礎推理邏輯層
│   │   ├── __init__.py        # 邏輯層導出類
│   │   └── basic_response_logic.py  # 基礎回應邏輯實現
│   │
│   ├── psi_field/             # 語義場處理層
│   │   ├── __init__.py        # 語義場層導出類
│   │   └── transient_judgment_of_semantic_field.py  # 語義場實現
│   │
│   └── quantum_engine/        # 量子啟發式分析層
│       ├── __init__.py        # 量子引擎層導出類
│       └── quantum_analyzer_engine.py  # 量子分析器實現
│
├── examples/                  # 範例代碼
│   ├── basic_inference_example.py       # 基本推理示例
│   ├── semantic_field_example.py        # 語義場分析示例
│   ├── quantum_analyzer_example.py      # 量子分析示例
│   └── integrated_analysis_example.py   # 綜合分析示例
│
└── tests/                     # 測試目錄
    ├── __init__.py            # 測試包初始化
    ├── conftest.py            # 測試配置和共用 fixtures
    │
    ├── test_logic_core/       # 邏輯層測試
    │   ├── __init__.py
    │   └── test_basic_response_logic.py
    │
    ├── test_psi_field/        # 語義場層測試
    │   ├── __init__.py
    │   └── test_transient_judgment.py
    │
    ├── test_quantum_engine/   # 量子引擎層測試
    │   ├── __init__.py
    │   └── test_quantum_analyzer.py
    │
    └── test_integration/      # 整合測試
        ├── __init__.py
        └── test_full_pipeline.py
```

## 核心功能

### 基礎推理邏輯層 (Logic Core)
- 實現完整的 AI 邏輯流程系統，從輸入解析→意圖對齊→量子態演化→自適應學習→因果推理→遞歸修正→全局整合
- 支援可擴展的配置管理與報告生成
- 提供完整的日誌追蹤與錯誤處理機制

### 語義場處理層 (PSI Field)
- 實現語境場的動態解鎖、知識錨定與語義張力分析
- 監控語義場演化與語境穩定相位
- 管理知識解鎖與激活程度，實現「語境穩定相位」(Context Stability Phase, CSP)

### 量子啟發式分析層 (Quantum Engine)
- 模擬量子啟發式推理與人機語意融合邏輯
- 提供多模式分析：純量子分析、基礎邏輯分析和綜合分析
- 整合量子與傳統方法，實現更高階的推理能力

## 安裝

```bash
# 從 PyPI 安裝
pip install psi-runtime-sdk

# 安裝開發版本
git clone https://github.com/example/psi-runtime-sdk.git
cd psi-runtime-sdk
pip install -e .

# 安裝可選依賴
pip install psi-runtime-sdk[api]  # 安裝 API 服務依賴
pip install psi-runtime-sdk[cli]  # 安裝 CLI 工具依賴
pip install psi-runtime-sdk[dev]  # 安裝開發工具依賴
```

## 快速開始

### 基本用法

```python
# 導入基本模組
from psi_runtime_sdk import BasicResponseLogic, SemanticFieldEngine, QuantumAnalyzer

# 使用基礎回應邏輯
from psi_runtime_sdk.logic_core import Config as BRLConfig
config = BRLConfig(debug_mode=True)
engine = BasicResponseLogic()
result = engine.run("請分析未來市場趨勢", config)
print(f"結果分數: {result.get('final_result', 0)}")

# 使用語義場引擎
from psi_runtime_sdk.psi_field import FieldConfig, DataParser
field_config = FieldConfig(enable_detailed_logging=True)
field_engine = SemanticFieldEngine(field_config)
semantic_input = DataParser.parse("探索語言模型的新應用")
unlocked_keys = field_engine.psi_engine.unlock_knowledge(semantic_input)
print(f"解鎖知識點: {unlocked_keys}")

# 使用量子分析器
from psi_runtime_sdk.quantum_engine import Config as QAConfig
qa_config = QAConfig(log_level=10)
qa_engine = QuantumAnalyzer(qa_config)
comprehensive_result = qa_engine.comprehensive_analysis("分析技術發展趨勢")
print(f"綜合分析結果: {comprehensive_result.get('integrated_score', 0)}")
```

### 綜合分析

```python
# 整合三個引擎的能力
def integrated_analysis(query):
    # 初始化所有引擎
    brl_engine = BasicResponseLogic()
    field_engine = SemanticFieldEngine(FieldConfig())
    qa_engine = QuantumAnalyzer(QAConfig())
    
    # 1. 使用語義場解鎖知識
    semantic_input = DataParser.parse(query)
    knowledge_keys = field_engine.psi_engine.unlock_knowledge(semantic_input)
    
    # 2. 使用量子分析器進行分析
    qa_result = qa_engine.comprehensive_analysis(query)
    
    # 3. 使用基礎邏輯引擎生成詳細分析
    brl_result = brl_engine.run(query, BRLConfig())
    
    # 4. 整合結果
    confidence = (qa_result.get("integrated_score", 0.5) + 
                 brl_result.get("final_result", 0.5)) / 2
    
    return {
        "query": query,
        "confidence": confidence,
        "knowledge_keys": knowledge_keys,
        "suggestions": brl_result.get("suggestions", {})
    }

# 使用整合分析
result = integrated_analysis("人工智能對未來工作的影響")
print(f"整合分析結果: {result}")
```

## 架構詳解

SDK 的三層架構實現了從基礎推理到高階語義分析的完整能力：

1. **邏輯核心層** (`logic_core`) 
   - 處理基本推理流程與決策生成
   - 提供配置管理、數據解析與報告生成
   - 實現量子態模擬與演化計算

2. **語義場層** (`psi_field`)
   - 動態解鎖與管理知識點
   - 追蹤語義場演化與穩定性
   - 分析語義張力與關聯度

3. **量子引擎層** (`quantum_engine`)
   - 綜合量子與傳統分析方法
   - 跨越自然語言與數學模型的鴻溝
   - 提供更高維度的語義理解

這三層可以獨立使用，也可以組合使用以實現更複雜的分析任務。

## 範例說明

`examples` 目錄提供了多個範例，展示了不同模組的使用方法：

- `basic_inference_example.py` - 展示 BasicResponseLogic 的基本用法
- `semantic_field_example.py` - 展示 SemanticFieldEngine 的語義場分析
- `quantum_analyzer_example.py` - 展示 QuantumAnalyzer 的多種分析模式
- `integrated_analysis_example.py` - 展示如何整合三個引擎進行綜合分析

執行範例：
```bash
python -m examples.basic_inference_example
python -m examples.integrated_analysis_example
```

## 進階應用

### API 服務
SDK 支援通過 FastAPI 快速搭建 API 服務：
```python
from fastapi import FastAPI
from psi_runtime_sdk import QuantumAnalyzer

app = FastAPI()
engine = QuantumAnalyzer()

@app.post("/analyze")
async def analyze(query: str):
    return engine.comprehensive_analysis(query)
```

### 自定義配置
所有引擎都支援深度自定義配置：
```python
from psi_runtime_sdk.psi_field import FieldConfig

# 自定義語義場配置
config = FieldConfig(
    field_dimension=128,          # 增加維度
    stability_threshold=0.85,     # 提高穩定性閾值
    enable_philosophical_analysis=True,
    enable_detailed_logging=True
)
```

### 運行測試

```bash
# 安裝測試依賴
pip install -e ".[test]"

# 運行所有測試
pytest

# 運行特定模組的測試
pytest tests/test_logic_core

# 運行單元測試，排除集成測試
pytest -m "unit and not integration"

# 生成測試覆蓋率報告
pytest --cov=psi_runtime_sdk
```


## 貢獻指南

我們歡迎對本項目做出貢獻！無論是修復錯誤、改進文檔還是提出新功能，您的參與都將使 PSI Runtime SDK 更加完善

## 許可協議

本項目採用 MIT 許可協議。詳情請參閱 `LICENSE` 文件。

## 聯繫我們

有任何問題或建議，請通過以下方式聯繫我們：
- 電子郵件：reagan.fue@gmail.com
- 項目主頁：https://github.com/example/psi-runtime-sdk

---

*PSI Runtime SDK - 將認知推理提升到一個新的維度*

