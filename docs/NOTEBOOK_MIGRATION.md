"""
如何修改現有笔记本使用新的數據加載系統
=====================================

本指南說明如何更新 01_data_preprocessing.ipynb 以使用新的 src/data_loader 模塊
"""

# ============================================================
# ❌ 舊方式（需要改進）
# ============================================================

# 原始 Notebook 中的代碼
"""
import pandas as pd
import os

if not os.path.exists(r"C:\Users\chent\.cache\kagglehub\datasets\shree0910\..."):
    import kagglehub
    from getpass import getpass
    
    # 1. 使用 Kaggle Access Token 進行身份驗證
    print("🔐 Kaggle 身份驗證")
    print("-" * 40)
    
    # 方法：使用 Access Token 設定環境變數
    username = input("請輸入您的 Kaggle 用戶名: ").strip()
    access_token = getpass("請輸入您的 Kaggle Access Token (輸入不會顯示): ")
    
    # 設定環境變數、下載等...
    # ... 複雜的自定義邏輯 ...
"""

# ============================================================
# ✅ 新方式（推薦）
# ============================================================

"""
第一個 Cell（導入和初始化）：
"""

import sys
from pathlib import Path

# 添加項目根目錄到 Python 路徑
project_root = Path.cwd().parent  # 假設 Notebook 在 notebooks/ 目錄下
sys.path.insert(0, str(project_root))

# 導入新的數據加載系統
from src.data_loader import load_data, DataLoader, ConfigLoader

# 加載配置
config = ConfigLoader.load_config(project_root / "config.yaml")

# 初始化加載器
loader = DataLoader(config)

print("✅ 數據加載系統已初始化")

"""
第二個 Cell（加載數據）：
"""

# 方式一：一行代碼加載
df = load_data()

# 或方式二：使用加載器
df = loader.load_raw_data()

print(f"✅ 數據已加載 | 形狀: {df.shape}")

"""
第三個 Cell（可選：探索數據並保存中間結果）：
"""

# ... 進行 EDA ...
# ... 數據清理、轉換等 ...

# 保存中間數據
loader.save_interim_data(
    df,
    filename="01_eda_output.csv"
)

print("✅ 中間數據已保存到 data/interim/")

# ============================================================
# 🔧 修改步驟（逐步指南）
# ============================================================

"""
步驟 1：在第一個 Cell 添加導入代碼
==================================
```python
import sys
from pathlib import Path

# 添加項目根目錄到路徑
project_root = Path.cwd().parent
sys.path.insert(0, str(project_root))

# 導入數據加載系統
from src.data_loader import load_data, DataLoader, ConfigLoader

# 加載配置
config = ConfigLoader.load_config(project_root / "config.yaml")
loader = DataLoader(config)
```

步驟 2：替換原有的數據加載代碼
==============================
將：
```python
if not os.path.exists(r"C:\Users\chent\.cache\kagglehub\..."):
    import kagglehub
    from getpass import getpass
    # ... 複雜邏輯 ...
else:
    df = pd.read_csv(r"C:\Users\chent\.cache\...")
```

替換為：
```python
# 加載數據（自動處理 Kaggle 認證、下載、緩存）
df = load_data()

# 或使用加載器
df = loader.load_raw_data()
```

步驟 3：在需要時保存處理後的數據
=================================
```python
# EDA 完成後保存中間數據
loader.save_interim_data(df_eda, "01_eda_output.csv")

# 特徵工程完成後保存處理完成的數據
loader.save_processed_data(df_processed, "features_engineered.parquet")
```

步驟 4：在其他 Notebook 中加載中間/處理完成的數據
================================================
```python
# 加載中間數據
df_interim = loader.load_interim_data("01_eda_output.csv")

# 加載處理完成的數據
df_ready = loader.load_processed_data("features_engineered.parquet")
```
"""

# ============================================================
# 📋 各 Notebook 推薦結構
# ============================================================

"""
📓 01_data_preprocessing.ipynb
==============================
第 1 Cell：導入和初始化
第 2 Cell：加載原始數據
第 3-N Cells：數據清理、缺失值處理、類型轉換
最後 Cell：保存中間數據 (data/interim/)

第一個 Cell 的完整代碼：
```python
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 添加項目根目錄到路徑
project_root = Path.cwd().parent
sys.path.insert(0, str(project_root))

# 導入新的數據加載系統
from src.data_loader import load_data, DataLoader, ConfigLoader

# 加載配置
config = ConfigLoader.load_config(project_root / "config.yaml")
loader = DataLoader(config)

# 設置中文字體
plt.rcParams['font.family'] = ['Microsoft JhengHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

print("✅ 初始化完成")
```

第二個 Cell：
```python
# 加載原始數據
df = load_data()
print(f"數據形狀: {df.shape}")
print(df.head())
```


📓 02_exploratory_data_analysis.ipynb
======================================
第 1 Cell：導入和初始化（同上）
第 2 Cell：加載中間數據（EDA 開始點）
```python
df = loader.load_interim_data("01_eda_output.csv")
# 或直接加載原始數據重新進行 EDA
df = load_data()
```
第 3-N Cells：各種分析和可視化
最後 Cell：保存 EDA 結果（如需要）


📓 03_statistical_methods.ipynb
================================
第 1 Cell：導入和初始化
第 2 Cell：加載中間數據
第 3-N Cells：假設檢驗、方差分析等


📓 04_data_mining.ipynb
=======================
第 1 Cell：導入和初始化
第 2 Cell：加載處理完成的數據
```python
df = loader.load_processed_data("features_engineered.parquet")
```
第 3-N Cells：模型訓練、評估
"""

# ============================================================
# 🚀 快速轉換（針對現有 Notebook）
# ============================================================

"""
如果你想快速轉換現有的 Notebook：

1. 打開 01_data_preprocessing.ipynb

2. 在第一個 Cell 替換為：
   ```python
   import sys
   from pathlib import Path
   import pandas as pd
   
   project_root = Path.cwd().parent
   sys.path.insert(0, str(project_root))
   from src.data_loader import load_data, DataLoader, ConfigLoader
   
   config = ConfigLoader.load_config(project_root / "config.yaml")
   loader = DataLoader(config)
   ```

3. 查找包含 kagglehub 或長路徑的 Cell，替換為：
   ```python
   df = load_data()
   ```

4. 在 Notebook 最後添加：
   ```python
   # 保存中間數據供後續使用
   loader.save_interim_data(df, "01_eda_output.csv")
   ```

5. 完成！新的系統會自動處理：
   - Kaggle API 認證
   - 數據下載與緩存
   - 多用戶配置支持
   - 數據版本管理
"""

# ============================================================
# ⚙️ 配置文件自定義（可選）
# ============================================================

"""
如果需要自定義配置，編輯 config.yaml：

1. 修改數據路徑：
   data:
     raw_dir: "path/to/your/raw/data"
     interim_dir: "path/to/your/interim"
     processed_dir: "path/to/your/processed"

2. 修改 Kaggle 設置：
   kaggle:
     enable_download: true
     auth_method: "env_vars"
     dataset_id: "your-username/your-dataset"

3. 修改異常值處理策略：
   outlier_handling:
     field_strategies:
       monthly_income:
         action: "keep"
         transform: "log"
"""

# ============================================================
# 📚 完整示例：修改後的完整 Notebook 結構
# ============================================================

"""
=== 01_data_preprocessing.ipynb ===

Cell 1: 導入與初始化
```python
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

project_root = Path.cwd().parent
sys.path.insert(0, str(project_root))

from src.data_loader import load_data, DataLoader, ConfigLoader

config = ConfigLoader.load_config(project_root / "config.yaml")
loader = DataLoader(config)

plt.rcParams['font.family'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

print("✅ 環境初始化完成")
```

Cell 2: 加載數據
```python
# 加載原始數據（自動處理 Kaggle 認證）
df = load_data()

print(f"數據形狀: {df.shape}")
print(f"欄位數: {len(df.columns)}")
print(f"\\n欄位列表:\\n{df.columns.tolist()}")
```

Cell 3: 數據基本信息
```python
print("資料筆數與欄位數:", df.shape)
print("\\n欄位型態與非空值數量:")
df.info()
print("\\n缺失值統計:")
print(df.isna().sum())
```

... 中間的分析 Cell 保持不變 ...

Last Cell: 保存處理結果
```python
# 保存中間數據，供 02_eda.ipynb 使用
loader.save_interim_data(df, "01_data_cleaned.csv")

print("✅ 預處理完成，數據已保存到 data/interim/")
print(f"最終數據形狀: {df.shape}")
```
"""

# ============================================================
# 💡 故障排除
# ============================================================

"""
問題：ModuleNotFoundError: No module named 'src'
解決：
1. 確保在項目根目錄中運行 Notebook
2. 或修改 project_root 的路徑：
   project_root = Path("/path/to/DataMiningG1FinalProject")

問題：FileNotFoundError: config.yaml
解決：
1. 確保 config.yaml 存在於項目根目錄
2. 或明確指定配置文件路徑：
   config = ConfigLoader.load_config("/path/to/config.yaml")

問題：Kaggle 認證失敗
解決：
1. 檢查環境變量：
   echo $KAGGLE_USERNAME  # Linux/Mac
   echo %KAGGLE_USERNAME%  # Windows
2. 或放置 kaggle.json：
   ~/.kaggle/kaggle.json (Linux/Mac)
   C:\\Users\\YourUsername\\.kaggle\\kaggle.json (Windows)
"""
