# Things to Remember - Artificial intelligence is an extension of your morality and character
# 請記得 - 人工智慧是你的道德和性格的延伸

# PSI Runtime SDK

## Overview

PSI Runtime SDK is a cutting-edge experimental framework that combines quantum-inspired reasoning and semantic field analysis technology to provide powerful support for advanced human-computer collaborative reasoning applications. This SDK implements a multi-level cognitive model, including basic response logic, semantic field analysis, and quantum analysis engine, providing innovative ideas and implementation foundation for the next generation of intelligent systems.

## Project Structure

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

## Core Functionality

### Basic reasoning logic layer (Logic Core)
- Implement a complete AI logic process system, from input parsing → intention alignment → quantum state evolution → adaptive learning → causal reasoning → recursive correction → global integration
- Supports scalable configuration management and report generation
- Provide complete log tracking and error handling mechanism

### Semantic Field Processing Layer (PSI Field)
- Realize dynamic unlocking of context field, knowledge anchoring and semantic tension analysis
- Monitor the evolution of semantic fields and the phase of contextual stability
- Manage the degree of knowledge unlocking and activation to achieve the "Context Stability Phase" (CSP)

### Quantum-inspired analysis layer (Quantum Engine)
- Simulating quantum-inspired reasoning and human-computer semantic fusion logic
- Provide multi-mode analysis: pure quantum analysis, basic logic analysis and comprehensive analysis
- Integrate quantum and traditional methods to achieve higher-order reasoning capabilities

## Install

```bash
# Install from PyPI
pip install psi-runtime-sdk

# Install the development version
git clone https://github.com/example/psi-runtime-sdk.git
cd psi-runtime-sdk
pip install -e .

# Install optional dependencies
pip install psi-runtime-sdk[api] # Install API service dependencies
pip install psi-runtime-sdk[cli] # Install CLI tool dependencies
pip install psi-runtime-sdk[dev] # Install development tool dependencies
```

## Quick Start

### Basic usage

```Python
# Import basic modules
from psi_runtime_sdk import BasicResponseLogic, SemanticFieldEngine, QuantumAnalyzer

# Using basic response logic
from psi_runtime_sdk.logic_core import Config as BRLConfig
config = BRLConfig(debug_mode=True)
engine = BasicResponseLogic()
result = engine.run("Please analyze future market trends", config)
print(f"Result score: {result.get('final_result', 0)}")

# Using the Semantic Field Engine
from psi_runtime_sdk.psi_field import FieldConfig, DataParser
field_config = FieldConfig(enable_detailed_logging=True)
field_engine = SemanticFieldEngine(field_config)
semantic_input = DataParser.parse("Explore new applications of language models")
unlocked_keys = field_engine.psi_engine.unlock_knowledge(semantic_input)
print(f"Unlocked knowledge points: {unlocked_keys}")

# Using the quantum analyzer
from psi_runtime_sdk.quantum_engine import Config as QAConfig
qa_config = QAConfig(log_level=10)
qa_engine = QuantumAnalyzer(qa_config)
comprehensive_result = qa_engine.comprehensive_analysis("分析技術發展趨勢")
print(f"綜合分析結果: {comprehensive_result.get('integrated_score', 0)}")
```

### Comprehensive Analysis

```Python
# Integrate the capabilities of the three engines
def integrated_analysis(query):
# Initialize all engines
brl_engine = BasicResponseLogic()
field_engine = SemanticFieldEngine(FieldConfig())
qa_engine = QuantumAnalyzer(QAConfig())

# 1. Unlock knowledge using semantic fields
semantic_input = DataParser.parse(query)
knowledge_keys = field_engine.psi_engine.unlock_knowledge(semantic_input)

# 2. Analyze using quantum analyzer
qa_result = qa_engine.comprehensive_analysis(query)

# 3. Generate detailed analysis using the basic logic engine
brl_result = brl_engine.run(query, BRLConfig())

# 4. Integrate the results
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

## Architecture details

The three-layer architecture of the SDK enables complete capabilities from basic reasoning to high-level semantic analysis:


- 1. **Logical core layer** (`logic_core`)
- Handle basic reasoning processes and decision making
- Provide configuration management, data analysis and report generation
- Realize quantum state simulation and evolutionary computing

  
2. **Semantic Field Layer** (`psi_field`)
- Dynamic unlocking and management knowledge points
- Tracking the evolution and stability of semantic fields
- Analyze semantic tension and relevance


3. **Quantum Engine Layer** (`quantum_engine`)
- Integrated quantum and traditional analysis methods
- Bridging the gap between natural language and mathematical models
- Provide higher-dimensional semantic understanding


These three layers can be used independently or in combination to achieve more complex analysis tasks.

## Example Description

The `examples` directory provides several examples showing how to use different modules:

- `basic_inference_example.py` - demonstrates basic usage of BasicResponseLogic
- `semantic_field_example.py` - Demonstrates semantic field analysis using SemanticFieldEngine
- `quantum_analyzer_example.py` - demonstrates various analysis modes of QuantumAnalyzer
- `integrated_analysis_example.py` - shows how to integrate the three engines for integrated analysis

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

### Custom Configuration
All engines support deep custom configuration:

```Python


from psi_runtime_sdk.psi_field import FieldConfig

# Custom semantic field configuration
config = FieldConfig(
field_dimension=128, # add dimension
stability_threshold=0.85, # Increase the stability threshold
enable_philosophical_analysis=True,
enable_detailed_logging=True
)

```
### Running the tests
```
bash
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


## Contribution Guidelines

We welcome contributions to this project! Whether it's fixing bugs, improving documentation or proposing new features, your participation will make the PSI Runtime SDK better.

## License Agreement

This project uses the MIT license. See the `LICENSE` file for details.


Submission Package README

Title
AI Contextual Field Modeling: Semantic Unlocking and Dialogic Reasoning Framework

— A Foundational Architecture of Semantic Field Theory (SFT)

Author
Name: Reagan Fu

Affiliation: Independent Researcher

Email: reagan.fue@gmail.com

ORCID: (optional)

Abstract
This paper introduces the Contextual Field Theory (CFT), a multilayer semantic reasoning architecture that enables dialogue systems to reason over semantic chains, unlock knowledge via context-induced activation, and converge into a closed-field logic system. It proposes a high-dimensional contextual logic engine (CLE) with modular components including the ΨUnlockEngine, CSPController, and EchoResolver. Rather than retrieve-and-generate, it applies a novel cycle: unlock → expand → collapse → refocus. The system is mathematically modeled and includes formalized interfaces and logic graphs.


Notes
This model is intended as a new layer of semantic control architecture atop LLM systems, with potential application in philosophy-aware, ethical, and long-context AI dialogue systems.

The author is open to collaboration and extension under open research principles.

```
Files
PsiRuntimeSDK/
├── README.md              # Project Description Document
├── pyproject.toml            # Build system configuration
├── requirements.txt          # Dependency List
├── setup.py                 # Install script
├── psi_runtime_sdk/          # Main package directory
│   ├── __init__.py          # Suite initialization file
│   ├── logic_core/           # Basic reasoning logic layer
│   │   ├── __init__.py
│   │   └── basic_response_logic.py
│   ├── psi_field/            # Semantic field processing layer
│   │   ├── __init__.py
│   │   └── transient_judgment_of_semantic_field.py
│   └── quantum_engine/       # Quantum-inspired analysis layer
│       ├── __init__.py
│       └── quantum_analyzer_engine.py
└── examples/                 # Example code
    ├── basic_inference_example.py      # Basic inference example
    ├── semantic_field_example.py       # Semantic field analysis example
    ├── quantum_analyzer_example.py    #Quantum analysis example
    └── integrated_analysis_example.py   # Comprehensive analysis example
```

License

Default: CC BY 4.0

“Every utterance is a field event; every conversation is a topology in motion.”

“Future work includes deployment in dialogue-based AI assistants, and formalizing field-aware evaluation metrics for stability, safety, and reasoning quality in long-context semantic systems.”



## Contact Us

If you have any questions or suggestions, please contact us via the following methods:

- Email: reagan.fue@gmail.com
  
- Project homepage: https://github.com/reaganfue/PSI-Runtime-SDK

---

PSI Runtime SDK - Taking cognitive reasoning to a new dimension

