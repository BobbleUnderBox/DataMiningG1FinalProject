# 01_data_preprocessing.ipynb 資料前處理簡述

本筆記本將原始 BNPL 資料轉成可建模的特徵表，主要流程是：資料檢查 → 時間特徵工程 → 偏態轉換 → 編碼 → 輸出。

## 前處理前：原始資料型別與欄位

`df.info()` 顯示共有 17 欄、10345 筆，型別分佈如下：

- `int64`（7 欄）：`user_id`, `age`, `credit_score`, `bnpl_installments`, `repayment_delay_days`, `missed_payments`, `default_flag`
- `float64`（5 欄）：`monthly_income`, `purchase_amount`, `app_usage_frequency`, `debt_to_income_ratio`, `risk_score`
- `object`（5 欄）：`employment_type`, `product_category`, `location`, `transaction_date`, `customer_segment`

另外也有做缺失值與重複值檢查（此資料集中缺失值為 0）。

## 前處理流程（依 notebook 實作）

1. **時間特徵工程**
   - `transaction_date` 轉為 datetime。
   - 拆出：`transaction_year_onehot`, `transaction_month`, `transaction_day`, `transaction_dayofweek`, `transaction_is_weekend`。
   - 再做週期特徵：`transaction_month_sin/cos`, `transaction_day_sin/cos`, `transaction_dayofweek_sin/cos`。
   - 最後移除原始 `transaction_date`。

2. **變數分類與處理策略設定**
   - Categorical：`employment_type`, `product_category`, `location`, `default_flag`
   - Ordinal：`customer_segment`
   - Interval：`credit_score`
   - Ratio：`age`, `monthly_income`, `purchase_amount`, `bnpl_installments`, `repayment_delay_days`, `missed_payments`, `app_usage_frequency`, `debt_to_income_ratio`, `risk_score`

3. **離群值處理（實際為檢查/回報）**
   - 程式會計算 IQR 邊界與離群值數量（如 `monthly_income`, `debt_to_income_ratio`, `risk_score` 等）。
   - 目前 notebook 內此步驟沒有真正做截尾（Winsorize）或刪除，只是列印結果並回傳資料副本。

4. **偏態轉換（Log1p）**
   - 對 `credit_score`, `age`, `monthly_income`, `purchase_amount`, `repayment_delay_days`, `app_usage_frequency`, `debt_to_income_ratio` 做 `log1p`。
   - 產生新欄位（如 `credit_score_log1p`），並刪除原欄位。

5. **編碼**
   - `customer_segment` 做 ordinal mapping：`Low Risk=0`, `Medium Risk=1`, `High Risk=2`。
   - `employment_type`, `product_category`, `location`, `default_flag` 做 One-Hot (`pd.get_dummies`)。
   - 移除 `user_id`（`transaction_date` 若存在也會移除）。

6. **標準化**
   - 對 `risk_score` 做 `StandardScaler`（Z-score）。

7. **輸出**
   - 儲存 `data/processed/01_preprocessed.csv`。

## 前處理後：輸出變數（`01_preprocessed.csv`）

共 39 欄，主要包含：

- 保留/數值欄位：`bnpl_installments`, `missed_payments`, `risk_score`, `customer_segment`
- 時間特徵欄位：`transaction_year_onehot`, `transaction_month`, `transaction_day`, `transaction_dayofweek`, `transaction_is_weekend`, `transaction_month_sin`, `transaction_month_cos`, `transaction_day_sin`, `transaction_day_cos`, `transaction_dayofweek_sin`, `transaction_dayofweek_cos`
- Log1p 欄位：`credit_score_log1p`, `age_log1p`, `monthly_income_log1p`, `purchase_amount_log1p`, `repayment_delay_days_log1p`, `app_usage_frequency_log1p`, `debt_to_income_ratio_log1p`
- One-Hot 欄位：
  - `employment_type_*`
  - `product_category_*`
  - `location_*`
  - `default_flag_0`, `default_flag_1`

> 註：目前 notebook 實際儲存的是 `01_preprocessed.csv`；未看到 `processed_for_pca.csv` 的實際輸出程式碼。
