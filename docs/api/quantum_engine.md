# Quantum Engine API 參考

本文檔提供 Quantum Engine 模組的詳細 API 參考，包括 `QuantumAnalyzer` 類及其方法。

## QuantumAnalyzer

`QuantumAnalyzer` 是量子分析引擎的核心類，提供基於量子計算原理的文本分析功能。

### 初始化

```python
from quantum_engine import QuantumAnalyzer, Config

# 默認配置初始化
analyzer = QuantumAnalyzer()

# 使用配置對象初始化
config = Config(log_level=10, mode="advanced")
analyzer = QuantumAnalyzer(config)
```

### 配置參數

| 參數 | 類型 | 默認值 | 說明 |
|-----|-----|-------|-----|
| `log_level` | int | `20` | 日誌級別 (10=DEBUG, 20=INFO, 30=WARNING) |
| `mode` | str | `"standard"` | 量子分析模式 ("standard", "advanced", "experimental") |
| `test_mode` | bool | `False` | 是否為測試模式 |
| `use_cache` | bool | `True` | 是否使用結果快取 |

### 方法

#### run_inference

```python
def run_inference(text: str, use_basic_logic: bool = False) -> Dict[str, Any]:
```

執行量子分析推理計算。

**參數:**
- `text (str)`: 需分析的輸入文本。
- `use_basic_logic (bool)`: 是否使用基礎邏輯進行分析，默認為 False。

**返回:**
- `Dict[str, Any]`: 包含分析結果的字典，具體格式如下：

```python
{
    "text": "原始文本",  # 原始輸入文本
    "quantum_state": [0.1, 0.2, 0.3, ...],  # 模擬量子態表示
    "analysis_type": "quantum",  # 分析類型
    "entropy": 0.75,  # 文本熵值
    "coherence": 0.82,  # 語義連貫性
    "final_result": 0.78,  # 最終分析分數
    "insights": [  # 分析洞察
        "文本展現高度連貫性",
        "主題關注點明確集中"
    ]
}
```

**示例:**

```python
from quantum_engine import QuantumAnalyzer

analyzer = QuantumAnalyzer()
result = analyzer.run_inference("探索量子計算在自然語言處理中的應用")
print(f"文本熵值: {result['entropy']}")
print(f"最終分析分數: {result['final_result']}")
```

#### comprehensive_analysis

```python
def comprehensive_analysis(text: str, domain_weights: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
```

執行綜合分析，結合量子分析與基礎邏輯。

**參數:**
- `text (str)`: 需分析的輸入文本。
- `domain_weights (Optional[Dict[str, float]])`: 各領域權重配置，例如 `{"medical": 0.8, "general": 0.2}`。

**返回:**
- `Dict[str, Any]`: 包含綜合分析結果的字典，具體格式如下：

```python
{
    "text": "原始文本",  # 原始輸入文本
    "integrated_score": 0.82,  # 整合分析分數
    "quantum_contribution": 0.7,  # 量子分析貢獻
    "logic_contribution": 0.3,  # 邏輯分析貢獻
    "domain_analysis": {  # 各領域分析 (如有提供 domain_weights)
        "medical": 0.85,
        "general": 0.76
    },
    "insights": [  # 分析洞察
        "文本在醫療領域具有高度相關性",
        "建議進一步探索醫療應用方向"
    ],
    "actions": [  # 建議行動
        "深入研究醫療文獻",
        "尋找與醫療專家的合作機會"
    ]
}
```

**示例:**

```python
from quantum_engine import QuantumAnalyzer

analyzer = QuantumAnalyzer()

# 一般分析
result = analyzer.comprehensive_analysis("探索量子計算與深度學習的結合")

# 領域加權分析 (例如醫療領域文本)
domain_result = analyzer.comprehensive_analysis(
    "探索量子計算在醫療診斷中的應用",
    domain_weights={"medical": 0.8, "technology": 0.2}
)

print(f"一般分析分數: {result['integrated_score']}")
print(f"醫療領域分析分數: {domain_result['domain_analysis']['medical']}")
```

#### visualize_quantum_state

```python
def visualize_quantum_state(text: str) -> Dict[str, Any]:
```

生成文本的量子態視覺化數據。

**參數:**
- `text (str)`: 需視覺化的輸入文本。

**返回:**
- `Dict[str, Any]`: 包含量子態視覺化數據的字典，具體格式如下：

```python
{
    "amplitude_data": [0.1, 0.2, 0.3, ...],  # 量子態振幅
    "phase_data": [0.0, 0.5, 1.0, ...],  # 量子態相位
    "basis_labels": ["basis_0", "basis_1", ...],  # 基態標籤
    "dominant_basis": "basis_3",  # 主導基態
    "entanglement_measure": 0.75  # 糾纏度量
}
```

**示例:**

```python
from quantum_engine import QuantumAnalyzer
import matplotlib.pyplot as plt
import numpy as np

analyzer = QuantumAnalyzer()
viz_data = analyzer.visualize_quantum_state("量子計算基礎與應用")

# 繪製振幅圖
plt.figure(figsize=(10, 6))
plt.bar(viz_data["basis_labels"], viz_data["amplitude_data"])
plt.title("量子態振幅分布")
plt.xlabel("基態")
plt.ylabel("振幅")
plt.xticks(rotation=45)
plt.show()
```

#### reset

```python
def reset() -> None:
```

重置分析器狀態，清除緩存和臨時數據。

**示例:**

```python
from quantum_engine import QuantumAnalyzer

analyzer = QuantumAnalyzer()
analyzer.run_inference("測試文本")

# 重置分析器狀態
analyzer.reset()
```

## 輔助類與函數

### Config

`Config` 類用於配置量子分析引擎的各種參數。

```python
from quantum_engine import Config

config = Config(
    log_level=10,  # DEBUG 級別
    mode="advanced",
    use_cache=True
)
```

### QuantumState

`QuantumState` 類代表文本的量子態表示。

```python
from quantum_engine import QuantumState

# 創建量子態
state = QuantumState(dimension=8)

# 測量量子態
measurement = state.measure()
``` 
