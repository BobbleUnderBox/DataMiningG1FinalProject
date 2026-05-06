# 資料探勘期末專案 - BNPL 資料集分析

## 📌 專案概述
本專案分析 **BUY NOW PAY LATER (BNPL)** 金融科技資料集，以瞭解使用者付款行為並建構信用風險評估的預測模型。

**資料集來源：** [Kaggle - Buy Now Pay Later (BNPL) Fintech ML Dataset](https://www.kaggle.com/datasets/shree0910/buy-now-and-pay-later-fintech-ml-dataset)

---

## 📊 進度更新

### 最新 (5/4)
- ✅ 從 Kaggle 取得資料
- ✅ 分類資料型態（類別型、順序型、區間型、比率型）
- ✅ 執行初步探索性資料分析 (EDA)
- ✅ 生成視覺化圖表

**技術說明：**
- Kaggle token認證透過檔案儲存

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

```
DataMiningG1FinalProject/
├── README.md
├── COLUMN_GUIDE.md
├── environment.yml
└── notebooks/
    ├── 01_data_preprocessing.ipynb
    ├── 02_exploratory_data_analysis.ipynb
    ├── 03_statistical_methods.ipynb
    └── 04_data_mining.ipynb
```

---