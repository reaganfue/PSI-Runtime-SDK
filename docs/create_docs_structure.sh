#!/bin/bash
# 創建文檔目錄結構

# 創建主要文檔目錄
mkdir -p docs/api docs/examples

# 創建文件
touch docs/architecture.md
touch docs/concepts.md

# 創建 API 文檔
touch docs/api/psi_field.md
touch docs/api/quantum_engine.md
touch docs/api/logic_core.md

# 創建示例文檔
touch docs/examples/getting_started.md
touch docs/examples/advanced_usage.md

echo "文檔目錄結構已創建" 
