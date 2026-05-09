# 🏦 BNPL 信用風險分類與預測項目

> Buy-Now-Pay-Later (BNPL) 信用風險分類與預測  
> 基於高階統計方法、資料採礦與機器學習的綜合資料科學項目

## 📋 項目概覽

本項目致力於構建一個**生產級資料科學項目**，用於預測 BNPL 平台用戶的信用風險。採用現代 Python 開發趨勢和 CCDS v2 標準化目錄架構，確保代碼可復用、可維護、易擴展。

---

## 📊 進度更新

### 最新 (5/7) - Windows 相容性與穩定性優化
- ✅ **解決 Makefile 亂碼**：實作 Python 基礎的訊息系統 (`scripts/messages.py`)，確保 Windows 終端機正確顯示中文與 Emoji。
- ✅ **路徑自動解析**：修正筆記本路徑問題，透過 `PROJECT_ROOT` 自動偵測，確保 `data/` 與 `logs/` 永遠位於專案根目錄。
- ✅ **環境驗證修復**：修正 `pyproject.toml` 設定錯誤，確保 `make install-all` 流程順暢。
- ✅ **任務自動化**：優化 `Makefile` 任務，支援一鍵安裝、環境資訊顯示與資料同步。

### 階段性達成 (5/6) - 專案架構重組
- ✅ **模組化重構**：將資料處理邏輯遷移至 `src/data_loader.py`，提升代碼複用性。
- ✅ **配置中心化**：引入 `config.yaml` 統一管理資料路徑、Kaggle API 與離群值處理策略。
- ✅ **現代化包裝**：採用 `pyproject.toml` 取代傳統 requirements，建立生產級專案標準。
- ✅ **清理與規範**：清理冗餘暫存檔，並建立完善的 `.gitignore` 規則。

### 5/4
- ✅ 從 Kaggle 取得資料
- ✅ 分類資料型態（類別型、順序型、區間型、比率型）
- ✅ 執行初步探索性資料分析 (EDA)
- ✅ 生成視覺化圖表

---

## 📋 欄位說明

| 欄位 | 型態 | 說明 |
|------|------|------|
| user_id | int | 唯一使用者id |
| age | int | 使用者年齡（18–59 歲） |
| employment_type | str | 全職 / 自僱 / 學生 / 失業 |
| monthly_income | float | 月收入（美元） |
| credit_score | int | 標準信用評分（300–850） |
| purchase_amount | float | BNPL 交易金額（美元） |
| product_category | str | 電子產品、服裝、運動、家居、美容 |
| bnpl_installments | int | 分期次數（3、6、9、12 期） |
| repayment_delay_days | int | 逾期天數（0–33 天） |
| missed_payments | int | 過去漏繳分期付款的總次數（0–7 次） |
| default_flag | int | **target：** 1 = 違約，0 = 已付款 ✅ |
| app_usage_frequency | float | 應用程式每週開啟次數 |
| location | str | 國家（美國、印度、英國、德國、加拿大、澳洲） |
| transaction_date | str | 購買日期（YYYY-MM-DD） |
| debt_to_income_ratio | float | 債務收入比（月債務 / 月收入） |
| risk_score | float | 風險評分（0–398）— 越高越危險 |
| customer_segment | str | 低風險 / 中風險 / 高風險 |

---

## 📁 專案結構

```text
DataMiningG1FinalProject/
├── config.yaml          # 全域設定檔（路徑、參數、策略）
├── pyproject.toml       # 專案依賴與現代化打包設定
├── Makefile             # 自動化任務腳本（Windows/Unix 雙支援）
├── data/                # 資料目錄
│   ├── raw/             # 原始資料（Kaggle 下載）
│   ├── interim/         # 中間處理資料（EDA 過程）
│   └── processed/       # 最終特徵資料（建模用）
├── notebooks/           # Jupyter Notebooks 分析流程
│   ├── 01_data_preprocessing.ipynb
│   ├── 02_exploratory_data_analysis.ipynb
│   └── ...
├── src/                 # 專案原始碼模組
│   ├── __init__.py
│   └── data_loader.py   # 資料載入、路徑管理與下載邏輯
├── scripts/             # 工具腳本
│   └── messages.py      # 跨平台 UTF-8 訊息系統
├── logs/                # 執行日誌
└── models/              # 已訓練模型存放
```

---