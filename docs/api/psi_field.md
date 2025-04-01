# PSI Field API 參考

本文檔提供 PSI Field 模組的詳細 API 參考，包括 `PsiFieldModel` 類及其方法。

## PsiFieldModel

`PsiFieldModel` 是 PSI Field 模組的核心類，提供語義場分析與處理功能。

### 初始化

```python
from psi_field import PsiFieldModel

# 默認配置初始化
model = PsiFieldModel()

# 自定義配置初始化
model = PsiFieldModel(config={
    "use_advanced": True,
    "field_dimension": 128,
    "stability_threshold": 0.85
})
```

### 配置參數

| 參數 | 類型 | 默認值 | 說明 |
|-----|-----|-------|-----|
| `use_advanced` | bool | `False` | 是否使用進階語義場分析 |
| `field_dimension` | int | `64` | 語義場向量維度 |
| `stability_threshold` | float | `0.75` | 語義場穩定性閾值 |
| `enable_detailed_logging` | bool | `False` | 是否啟用詳細日誌 |

### 方法

#### process

```python
def process(text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
```

處理輸入文本並生成情境場域分析結果。

**參數:**
- `text (str)`: 需處理的輸入文本。
- `context (Optional[Dict[str, Any]])`: 可選的上下文信息，包含時間戳等元數據。

**返回:**
- `Dict[str, Any]`: 包含處理結果的字典，具體格式如下：

```python
{
    "status": "success",  # 處理狀態
    "processed_text": "原始文本",  # 原始處理文本
    "timestamp": "2025-03-12T10:00:00",  # 處理時間戳
    "semantic_field": {  # 語義場信息
        "dimensions": 64,  # 語義場維度
        "tension": 0.75,  # 語義場張力
        "stability_score": 0.82,  # 穩定性分數
        "is_stable": True,  # 是否達到穩定相位
        "active_knowledge_count": 5,  # 激活的知識點數量
        "field_type": "穩定場"  # 語義場類型
    },
    "keywords": ["人工智能", "語義", "場域", "分析", "量子"],  # 提取的關鍵詞
    "insights": [  # 生成的洞察
        "主要關注領域: 自然語言處理",
        "語義場高度穩定，概念清晰且一致"
    ]
}
```

**示例:**

```python
from psi_field import PsiFieldModel

model = PsiFieldModel()
result = model.process("探索人工智能與語義場分析技術的結合")
print(result["semantic_field"]["tension"])  # 語義場張力
print(result["insights"])  # 生成的洞察
```

#### train

```python
def train(training_data: List[Dict[str, Any]], epochs: int = 5, learning_rate: float = 0.01) -> Dict[str, float]:
```

使用提供的訓練數據訓練或微調語義場模型。

**參數:**
- `training_data (List[Dict[str, Any]])`: 訓練數據列表，每項應包含 "text" 和 "label" 字段。
- `epochs (int)`: 訓練輪數，默認為 5。
- `learning_rate (float)`: 學習率，默認為 0.01。

**返回:**
- `Dict[str, float]`: 包含訓練指標的字典，包括 "accuracy" 和 "loss"。

**示例:**

```python
from psi_field import PsiFieldModel

model = PsiFieldModel()

training_data = [
    {"text": "探索人工智能的應用", "label": "技術"},
    {"text": "語義場理論與實踐", "label": "理論"}
]

metrics = model.train(training_data, epochs=10)
print(f"訓練準確率: {metrics['accuracy']}")
```

#### evaluate

```python
def evaluate(evaluation_data: List[Dict[str, Any]]) -> Dict[str, float]:
```

評估模型在給定評估數據上的表現。

**參數:**
- `evaluation_data (List[Dict[str, Any]])`: 評估數據列表，格式與訓練數據相同。

**返回:**
- `Dict[str, float]`: 包含評估指標的字典，包括 "precision", "recall" 和 "f1_score"。

**示例:**

```python
from psi_field import PsiFieldModel

model = PsiFieldModel()

eval_data = [
    {"text": "語義場在醫療領域的應用", "label": "應用"},
    {"text": "量子計算的理論基礎", "label": "理論"}
]

metrics = model.evaluate(eval_data)
print(f"評估 F1 分數: {metrics['f1_score']}")
```

#### visualize

```python
def visualize(text: str) -> Dict[str, Any]:
```

為輸入文本生成語義場視覺化數據，用於圖形化展示。

**參數:**
- `text (str)`: 需要視覺化的輸入文本。

**返回:**
- `Dict[str, Any]`: 包含視覺化數據的字典，具體格式如下：

```python
{
    "nodes": [  # 節點列表
        {"id": "1", "label": "人工智能", "size": 30, "color": "#ff0000"},
        {"id": "2", "label": "語義場", "size": 25, "color": "#00ff00"},
        # ...更多節點
    ],
    "edges": [  # 邊列表
        {"source": "1", "target": "2", "weight": 0.8, "label": "關聯"},
        {"source": "1", "target": "3", "weight": 0.5, "label": "依賴"},
        # ...更多邊
    ],
    "field_properties": {  # 場屬性
        "center_concept": "人工智能",
        "average_connectivity": 2.5,
        "field_cohesion": 0.7
    }
}
```

**示例:**

```python
from psi_field import PsiFieldModel
import matplotlib.pyplot as plt
import networkx as nx

model = PsiFieldModel()
viz_data = model.visualize("探索人工智能與語義場理論的結合")

# 使用 NetworkX 和 Matplotlib 繪製語義場圖
G = nx.Graph()

# 添加節點
for node in viz_data["nodes"]:
    G.add_node(node["id"], label=node["label"], size=node["size"])

# 添加邊
for edge in viz_data["edges"]:
    G.add_edge(edge["source"], edge["target"], weight=edge["weight"])

# 繪製圖形
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)
nx.draw_networkx(G, pos, with_labels=True, node_size=[G.nodes[n]["size"]*10 for n in G.nodes])
plt.title("語義場視覺化")
plt.show()
```

#### get_status

```python
def get_status() -> Dict[str, Any]:
```

獲取模型當前狀態信息。

**返回:**
- `Dict[str, Any]`: 包含模型狀態的字典，包括版本、配置信息等。

**示例:**

```python
from psi_field import PsiFieldModel

model = PsiFieldModel()
status = model.get_status()
print(f"模型版本: {status['version']}")
print(f"初始化狀態: {status['initialized']}")
```

#### to_dict

```python
def to_dict() -> Dict[str, Any]:
```

將模型轉換為字典格式，便於序列化與保存。

**返回:**
- `Dict[str, Any]`: 模型的字典表示。

**示例:**

```python
from psi_field import PsiFieldModel
import json

model = PsiFieldModel()
model_dict = model.to_dict()

# 將模型字典保存為 JSON 文件
with open("model_config.json", "w", encoding="utf-8") as f:
    json.dump(model_dict, f, indent=2, ensure_ascii=False)
```

## 輔助類與函數

### FieldConfig

`FieldConfig` 類用於配置語義場引擎的各種參數。

```python
from psi_field import FieldConfig

config = FieldConfig(
    enable_detailed_logging=True,
    field_dimension=128,
    stability_threshold=0.8
)
```

### DataParser

`DataParser` 類用於解析輸入數據並提取知識關鍵詞。

```python
from psi_field import DataParser

# 解析輸入文本
semantic_input = DataParser.parse("探索人工智能的應用")

# 提取知識關鍵詞
keywords = DataParser.extract_knowledge_keys("語義場理論與量子計算")
```

### SemanticFieldEngine

`SemanticFieldEngine` 類是語義場引擎的核心實現，提供知識解鎖與語義場分析功能。

```python
from psi_field import SemanticFieldEngine, FieldConfig

# 初始化配置
config = FieldConfig(enable_detailed_logging=True)

# 初始化語義場引擎
engine = SemanticFieldEngine(config)

# 處理輸入文本
result = engine.process_input("探索人工智能與語義場分析")
``` 
