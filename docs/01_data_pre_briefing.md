# 01_data_preprocessing.ipynb 程式流程簡述

本筆記本的目標是將原始 BNPL 資料整理成可直接建模的資料集，並額外輸出一份 PCA 專用版本。

## 流程總覽

1. **環境初始化**
   - 匯入 `pandas / numpy / matplotlib / seaborn` 等套件。
   - 設定字型與專案路徑。
   - 載入 `config.yaml`，初始化 `DataLoader`。

2. **載入原始資料**
   - 透過 `load_data()` 讀取資料（必要時可自動處理下載流程）。
   - 顯示資料形狀、前幾筆與統計摘要。

3. **資料品質檢查**
   - 檢視欄位型別 (`df.info()`)。
   - 統計缺失值與重複筆數。

4. **變數分類**
   - 依統計尺度分成 `Categorical / Ordinal / Interval / Ratio`。
   - 作為後續轉換與編碼依據。

5. **時間特徵工程**
   - 將 `transaction_date` 轉為 datetime。
   - 拆出 `year / month / day / dayofweek / is_weekend`。

6. **離群值檢查（IQR）**
   - 對目標數值欄位計算 IQR 上下界與離群值數量。     (ratio+inteval 中 monthly_income, debt_to_income_ratio, risk_score, repayment_delay_days, missed_payments 有離群值)
   - 目前以「檢查與回報」為主，未直接刪除資料。

7. **偏態修正（Log / Log1p）**
   - 對右偏欄位做 `log` 或 `log1p` 轉換。
   - 以 Histogram 與 QQ plot 比較轉換前後分佈。

8. **特徵編碼**
   - `customer_segment` 以順序映射編碼。
   - 類別欄位採 One-Hot 編碼。
   - 移除不建模欄位（如 `user_id`, `transaction_date`）。
   - 產出 `df_encoded`（通用預處理資料）。

9. **PCA 專用前處理**
   - `Ratio` 欄位做 `log1p`。
   - `Interval` 欄位做 Z-score 標準化。
   - 產出 `df_pca`（供 PCA 使用）。

10. **輸出資料**
    - 儲存 `01_preprocessed.csv`（一般建模用）。
    - 儲存 `processed_for_pca.csv`（PCA 用）。

## 產出檔案

- `data/processed/01_preprocessed.csv`
- `data/processed/processed_for_pca.csv`
