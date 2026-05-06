"""
快速使用指南 - 新的數據加載系統
=====================================

本文檔說明如何使用重構後的 BNPL 項目
"""

# ============================================================
# 0️⃣ 初始化項目
# ============================================================
"""
第一次使用時，運行以下命令進行初始化：

$ make install              # 安裝開發環境
$ make data                 # 下載 Kaggle 數據集
"""

# ============================================================
# 1️⃣ 在 Notebook 中加載數據
# ============================================================

# 方式一：使用便利函數（推薦）
from src.data_loader import load_data

df = load_data()  # 一行代碼加載數據
print(f"數據形狀: {df.shape}")
print(df.head())

# ============================================================
# 2️⃣ 自定義配置加載
# ============================================================

from src.data_loader import ConfigLoader, DataLoader

# 加載配置文件
config = ConfigLoader.load_config("config.yaml")

# 初始化數據加載器
loader = DataLoader(config)

# 加載原始數據
df = loader.load_raw_data()

# ============================================================
# 3️⃣ 保存中間/處理完成的數據
# ============================================================

# 保存 EDA 後的中間數據
loader.save_interim_data(
    df_eda,
    filename="01_eda_output.csv",
    format="csv"
)

# 保存預處理後的數據
loader.save_processed_data(
    df_processed,
    filename="02_features_engineered.parquet",
    format="parquet"  # 推薦 parquet 格式以節省空間
)

# 加載中間數據
df_interim = loader.load_interim_data("01_eda_output.csv")

# 加載處理完成的數據
df_ready = loader.load_processed_data("02_features_engineered.parquet")

# ============================================================
# 4️⃣ 配置 Kaggle API（首次使用）
# ============================================================

"""
選項 A：使用環境變量（推薦）
==========================
在系統環境變量中設置：
  - KAGGLE_USERNAME: 你的 Kaggle 用戶名
  - KAGGLE_KEY: 你的 Kaggle API Key

從 https://www.kaggle.com/settings/account 下載 kaggle.json


選項 B：使用凭证文件
===================
1. 從 Kaggle 下載 kaggle.json
2. 放在 ~/.kaggle/ 目錄下
3. 在 config.yaml 中設置 auth_method: "credentials_file"


選項 C：交互式輸入
=================
首次運行時程序會提示輸入用戶名和 API Key
"""

# ============================================================
# 5️⃣ 強制重新下載數據
# ============================================================

# 如果需要重新下載數據
df = load_data(force_redownload=True)

# 或使用加載器
loader = DataLoader(config)
df = loader.load_raw_data(force_redownload=True)

# ============================================================
# 6️⃣ 配置文件說明
# ============================================================

"""
config.yaml 的關鍵配置項：

1. data:
   - raw_dir: 原始數據目錄（從 Kaggle 下載）
   - interim_dir: 中間數據目錄（EDA、特徵工程輸出）
   - processed_dir: 處理完成的數據目錄（直接用於建模）

2. kaggle:
   - enable_download: 是否啟用 Kaggle 下載
   - auth_method: 認證方式（"env_vars" 或 "credentials_file"）
   - dataset_id: Kaggle 數據集標識符

3. outlier_handling:
   - detection_method: 異常值檢測方法（"iqr", "zscore", etc）
   - field_strategies: 各字段的異常值處理策略
     - monthly_income: 保留 + Log 變換
     - repayment_delay_days: 保留 + Robust Scaling
     - debt_to_income_ratio: 保留 + Robust Scaling
     - risk_score: 保留 + 標準化
"""

# ============================================================
# 7️⃣ 使用 Makefile 進行工作流
# ============================================================

"""
常用命令：

$ make help               # 查看所有可用命令

# 數據處理
$ make data              # 首次下載數據
$ make data-force        # 強制重新下載
$ make eda               # 打開 EDA Notebook
$ make preprocess        # 打開預處理 Notebook

# 模型訓練
$ make train             # 訓練模型
$ make evaluate          # 評估模型
$ make train-evaluate    # 完整流程

# 代碼質量
$ make test              # 運行單元測試
$ make lint              # 代碼風格檢查
$ make format            # 自動格式化代碼

# 項目管理
$ make clean             # 清理臨時文件
$ make status            # 查看項目狀態
"""

# ============================================================
# 8️⃣ 故障排除
# ============================================================

"""
問題 1: 找不到 Kaggle 凭证
解決: 
  1. 確保已下載 kaggle.json
  2. 放在 ~/.kaggle/ 目錄下（Windows: C:\Users\YourUsername\.kaggle\）
  3. 檢查環境變量 KAGGLE_USERNAME 和 KAGGLE_KEY 是否已設置

問題 2: 下載速度慢或超時
解決:
  1. 檢查網絡連接
  2. 使用 make data-force 重試
  3. 考慮使用本地緩存（config.yaml 中的 use_kagglehub_cache）

問題 3: 無法導入 src 模塊
解決:
  1. 確保運行 make install
  2. 確保在項目根目錄中運行 Notebook
  3. 或在 Notebook 開頭添加:
     import sys
     sys.path.insert(0, '/path/to/project/root')
"""

# ============================================================
# 9️⃣ 項目目錄結構速查
# ============================================================

"""
新的標準化目錄結構：

DataMiningG1FinalProject/
├── data/
│   ├── raw/                         # 原始數據（Kaggle 下載）
│   ├── interim/                     # 中間數據（EDA、特徵工程）
│   └── processed/                   # 處理完成的數據（建模用）
├── notebooks/
│   ├── 01_data_preprocessing.ipynb
│   ├── 02_exploratory_data_analysis.ipynb
│   ├── 03_statistical_methods.ipynb
│   └── 04_data_mining.ipynb
├── src/
│   ├── __init__.py
│   ├── data_loader.py               # ⭐ 新的數據加載模塊
│   ├── preprocessor.py              # 特徵工程（待實現）
│   └── models.py                    # 模型定義（待實現）
├── models/                          # 訓練的模型
├── reports/figures/                 # 生成的圖表
├── tests/                           # 單元測試
├── config.yaml                      # ⭐ 新的配置文件
├── pyproject.toml                   # ⭐ 新的項目配置
├── Makefile                         # ⭐ 新的任務自動化
└── README.md                        # ⭐ 更新的項目文檔
"""

# ============================================================
# 🔟 總結
# ============================================================

"""
優勢：
✅ 配置化 - 支持多用戶、多路徑、多平台
✅ 自動化 - Kaggle API 自動認證和下載
✅ 標準化 - 遵循現代 Python 開發規範
✅ 可復用 - src/ 中的代碼可作為包導入
✅ 易維護 - 清晰的目錄結構和文檔

下一步：
1. 修改 config.yaml 中的路徑和 Kaggle 設置
2. 運行 make install 安裝依賴
3. 運行 make data 下載數據
4. 開始在 Notebook 中使用 from src.data_loader import load_data
"""
