# 🏦 BNPL 信用風險分類與預測

> Buy-Now-Pay-Later（先買後付）違約風險預測 — 統計方法與資料採礦期末專案
> **Group 4**｜組員：張博勛、盧宸立、陳霆翰、陳柏宇

---

## 📋 專案概述

先買後付（BNPL）是近年成長最快的金融科技領域之一。本專案使用 [Kaggle 合成資料集](https://www.kaggle.com/datasets/shree0910/buy-now-and-pay-later-fintech-ml-dataset)（模擬 2023–2024 年、6 個國家、10,345 筆 BNPL 交易紀錄），以 `default_flag`（是否違約）為目標變數，完整走過一次 CRISP-DM 流程：資料理解 → 資料品質檢查 → 前處理 → 統計檢定特徵篩選 → 建模（Random Forest / XGBoost / DNN）→ 評估 → 商業意涵解讀 → SHAP 模型解釋。

**重要聲明（EDA 發現的抽樣偏誤）：** 此資料集為合成資料，存在月薪未依國家區分、信用分數統一套用美國 FICO 範圍、違約比例偏高（39% vs. 真實世界個位數 %）等偏誤，**不適用於實務風控部署**，僅供統計檢定方法與建模流程練習。完整簡報見 [`docs/BNPL_FinalReport.pdf`](docs/)（另附投影片 PDF）。

---

## 🏆 專案成果摘要

### 特徵篩選（17 → 9 個特徵）

僅使用訓練集（防止 data leakage）進行卡方檢定 + WoE/IV（類別變數）、Mann-Whitney U 檢定（次序/區間/比率變數）與 Spearman 相關係數（共線性檢查，門檻 |r| ≥ 0.85），最終保留 9 個特徵：

`employment_type`、`product_category`、`missed_payments`、`transaction_dayofweek`、`age`、`monthly_income`、`purchase_amount`、`repayment_delay_days`、`debt_to_income_ratio`

被移除者包含：`user_id`（無關）、`risk_score` / `credit_score` / `customer_segment`（與 target 高度相關的冗餘變數，直接使用會造成 data leakage）、`location` / `transaction_is_weekend`（卡方不顯著）、`bnpl_installments` / `app_usage_frequency` / `transaction_year` / `month` / `day`（MWU 不顯著）。

### 模型表現（80/20 分層切割，測試集 n=2,069）

因「預測不違約但實際違約」（False Negative）代價極高，評估以 **F2-Score**（Recall 權重為 Precision 兩倍）選定決策門檻：

| 模型 | ROC-AUC | PR-AUC | Recall @F2最佳門檻 | Precision @F2最佳門檻 | F2-Score |
|---|---|---|---|---|---|
| Random Forest（`class_weight=balanced`） | 0.7595 | 0.6896 | 0.9950 | 0.4658 | 0.8108 |
| XGBoost（`scale_pos_weight`） | 0.7577 | 0.6808 | 0.9926 | 0.4685 | 0.8111 |
| DNN / MLP（Keras） | **0.7672** | **0.6950** | 0.9790 | 0.4829 | **0.8121** |

三個模型排序能力與機率校準（decile calibration）皆接近，DNN 略優且無過擬合/崩跌現象；三者一致認為 **`monthly_income`、`repayment_delay_days`、`missed_payments`、`debt_to_income_ratio`** 是最重要的違約驅動因子（以 SHAP 驗證，方向符合金融直覺：收入越高、負債比越低則違約機率下降；逾期天數與漏繳次數越多則違約機率上升）。

### 限制與應用邊界

- 合成資料與真實分布有落差，具體門檻/機率數值無法直接落地；但**特徵篩選邏輯、門檻選擇策略、SHAP 驅動的拒絕原因說明**等方法論可遷移至真實場景。
- 模型捕捉的是與違約高度相關的行為訊號（相關性），非違約的根本原因（因果）；且缺乏時序性特徵（近期遲繳趨勢）與壓力特徵，仍有精進空間。
- 建議用途：輔助風控單位制定業務規則／門檻，或作為高風險客戶被拒絕的主要因子說明；**不應**用於全自動決策而無人工覆核，尤其面對極端值或資料不足的少數族群。

詳細方法論、圖表與商業意涵討論，見 [`docs/prediction_flow.md`](docs/prediction_flow.md) 與各 `notebooks/0X_*.ipynb`。

---

## 📁 專案結構

```text
DataMiningG1FinalProject/
├── config.yaml            # 全域設定檔（資料路徑、Kaggle 認證、日誌）
├── pyproject.toml         # 專案依賴與現代化打包設定
├── Makefile                # 自動化任務（環境建立、安裝、資料同步、測試）
├── CLAUDE.md               # 開發者/AI 協作指南（指令、架構、流程細節）
├── data/
│   ├── raw/                # 原始 Kaggle CSV（10,345 筆）
│   ├── interim/             # 01/02 階段輸出（資料理解、特徵篩選中繼結果）
│   └── processed/          # 03 階段輸出：rf/xgb/dnn 各自的 train/test CSV
├── notebooks/               # CRISP-DM 流程，依序執行 01 → 08
│   ├── 01_data_understanding.ipynb    # 欄位盤點、型態分類、時間特徵拆解
│   ├── 02_data_quality.ipynb          # 缺失值/重複值/離群值/標籤雜訊檢查
│   ├── 03_data_preprocessing.ipynb    # 先切分再前處理（防止 leakage），三模型各自編碼
│   ├── 04_statistical_methods.ipynb   # 卡方+WoE/IV、Mann-Whitney U、Spearman 特徵篩選
│   ├── 05_modeling.ipynb              # 訓練 Random Forest / XGBoost / DNN
│   ├── 06_evaluation.ipynb            # 機率校準、ROC/PR 曲線、F2 門檻選擇、混淆矩陣
│   ├── 07_beyond_metrics.ipynb        # 商業情境下的指標意涵與取捨
│   └── 08_explain.ipynb               # SHAP 模型解釋
├── models/                  # 已訓練模型（rf_model.joblib, xgb_model.joblib, dnn_model.keras）
├── src/data_loader.py       # 唯一的原始碼模組：資料載入 / 下載 / 存取路徑管理
├── docs/                    # prediction_flow.md（流程文件）、期末簡報 PDF
└── tests/                   # pytest（目前為空，pyproject 已配置 pytest/pytest-cov）
```

> 目前專案以 Jupyter Notebook 驅動分析（無 CLI pipeline），`src/` 僅提供資料 I/O。完整指令與架構細節見 [`CLAUDE.md`](CLAUDE.md)。

---

## 📊 資料欄位說明

原始資料 17 欄，其中 `transaction_date` 於 01 階段拆解為年/月/日/星期幾/是否週末（17 → 21 欄）。

| 欄位 | 型態分類 | 說明 |
|------|------|------|
| user_id | 冗餘（刪除） | 唯一使用者 id，與 target 無關 |
| age | Ratio | 使用者年齡（18–59 歲） |
| employment_type | Category | Salaried / Self-Employed / Student / Unemployed |
| monthly_income | Ratio | 月收入（美元） |
| credit_score | 冗餘（刪除） | 標準信用評分（300–850），統一套用美國 FICO 範圍，跨國偏誤嚴重 |
| purchase_amount | Ratio | BNPL 交易金額（美元） |
| product_category | Category | Fashion / Electronics / Beauty / Home / Sports |
| bnpl_installments | Ordinal | 分期次數（3、6、9、12 期） |
| repayment_delay_days | Ratio | 逾期天數（0–33 天） |
| missed_payments | Ordinal | 過去漏繳分期付款的總次數（0–7 次） |
| default_flag | **Target** | 1 = 違約，0 = 已付款（違約率 39.05%，實務通常個位數 %） |
| app_usage_frequency | Ratio | 應用程式每週開啟次數 |
| location | Category（不顯著，刪除） | 國家（美國、印度、英國、德國、加拿大、澳洲） |
| transaction_date | — | 購買日期，拆解為 year/month/day/dayofweek/is_weekend 後刪除 |
| debt_to_income_ratio | Ratio | 債務收入比（月債務 / 月收入） |
| risk_score | 冗餘（刪除） | 風險評分（0–398），與 target Spearman 相關 0.39，會造成 leakage |
| customer_segment | 冗餘（刪除） | Low / Medium / High Risk，分群邏輯與 target 高度相關 |

---

## 🚀 快速開始

```bash
make env-info          # 檢查目前使用的 Python/pip 環境
make setup-venv         # 建立 ./.venv
make install-all        # 安裝依賴（pip install -e ".[dev,ml]"）
make data               # 載入資料（優先讀 data/raw，否則從 Kaggle 下載）
make test                # 執行 pytest tests/ -v
```

安裝完成後，依序在 Jupyter / VS Code 中執行 `notebooks/01_data_understanding.ipynb` 至 `notebooks/08_explain.ipynb`（每個 notebook 讀取前一階段輸出，須依序執行，勿跳階段）。完整指令、環境細節與資料流見 [`CLAUDE.md`](CLAUDE.md)。

---

## 👥 團隊

Group 4：張博勛、盧宸立、陳霆翰、陳柏宇
