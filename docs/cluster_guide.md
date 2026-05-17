# 混合資料分群標準流程：無監督篩選與階層式樹狀圖

這份流程專為處理包含連續（Ratio/Interval）、類別（Categorical）、順序（Ordinal）與時間特徵的「混合型資料」所設計。

流程採用策略 B（無監督特徵篩選）**來剔除雜訊，並使用**階層式分群的樹狀圖（Dendrogram）來客觀決定最佳的分群數 k。

## 📊 流程圖 (Flowchart)

```
flowchart TD

    A([原始混合型資料集]) --> Phase1
    
    subgraph Phase1 [Phase 1: 資料前處理 Data Preprocessing]
        direction TB
        B1(1. 處理離群值\n對 Ratio/Interval 執行 Winsorization 截尾)
        B2(2. 矯正偏態\n對偏態數值特徵取 Log 或 Yeo-Johnson 轉換)
        B3(3. 時間特徵編碼\nmonth/dayofweek 轉為 Sine/Cosine)
        B4(4. 類別與順序特徵處理\nOrdinal Label化 / Nominal One-Hot或保留給特定演算法)
        
        B1 --> B2 --> B3 --> B4
    end

    Phase1 --> Phase2

    subgraph Phase2 [Phase 2: 策略 B 特徵篩選 Feature Selection]
        direction TB
        C1(1. Spearman 相關係數檢定\n找出 |r| > 0.75 的高度相關特徵群，保留一個)
        C2(2. FAMD 混合資料因素分析\n觀察特徵貢獻度，剔除對主成分貢獻度極低的雜訊變數)
        
        C1 --> C2
    end

    Phase2 --> Phase3

    subgraph Phase3 [Phase 3: 決定分群數 k - Dendrogram]
        direction TB
        D1(1. 資料抽樣\n隨機抽取 5,000 筆資料以節省運算資源)
        D2(2. 計算距離矩陣\n計算 Gower's Distance 處理混合型態)
        D3(3. 繪製樹狀圖\n使用 Average Linkage 建立階層樹狀圖，\n尋找最長垂直線段畫水平線，交點即為 k)
        
        D1 --> D2 --> D3
    end

    Phase3 --> E([Phase 4: 正式分群\n使用得到的 k 值與乾淨特徵，\n投入 K-Prototypes 模型對全體資料分群])
```

## 📝 流程步驟詳細說明

### Phase 1: 資料前處理 (Data Preprocessing)

這是決定分群品質最核心的步驟，針對這份資料特性的客製化處理：

1. **處理離群值 (Outliers)**
   - **對象**：`monthly_income`, `debt_to_income_ratio`, `risk_score`, `repayment_delay_days`, `missed_payments`
   - **作法**：使用 **Winsorization (截尾)**。將極端值（例如高於 99% 分位數的值）強制收斂到 99% 的數值邊界，避免極端值在計算距離時拉扯整個幾何空間。
2. **矯正偏態 (Skewness Correction)**
   - **對象**：`age`, `monthly_income`, `purchase_amount`, `repayment_delay_days`, `app_usage_frequency`, `debt_to_income_ratio`, `credit_score`
   - **作法**：套用 **Log Transformation (取對數)** 或 `PowerTransformer` (Yeo-Johnson)，讓長尾分佈的資料收斂成接近常態分佈。
3. **時間特徵轉換 (Cyclical Encoding)**
   - **對象**：`month`, `dayofweek`, `day`
   - **作法**：進行 **正餘弦轉換 (Sine/Cosine Encoding)**。將一個週期性變數拆分為兩個特徵（例如 `month_sin` 和 `month_cos`），使演算法能理解時間的首尾相接特性。
4. **順序與離散數值轉換**
   - **對象**：`customer_segment`, `bnpl_installments`, `missed_payments`
   - **作法**：使用 **Ordinal Encoding (整數編碼)**（例如 0, 1, 2, 3），以保留其等級或次數的大小關係。

### Phase 2: 無監督特徵篩選 (Strategy B)

透過特徵間的統計關係來去蕪存菁：

1. **相關性過濾 (Spearman Correlation)**
   - **作法**：計算所有數值型（含 Ordinal）特徵的 Spearman 相關係數矩陣。
   - **篩選**：找出相關係數絕對值 ∣r∣>0.75 的特徵組合，從中保留變異數較大或商業意義較直觀的一個，剔除其餘高度重複的變數。
2. **FAMD 貢獻度檢定 (Factor Analysis of Mixed Data)**
   - **作法**：執行 FAMD（混合資料的 PCA 延伸）。
   - **篩選**：檢查每個原始變數對前幾個主成分（累積解釋變異達 70%~80%）的貢獻度。將貢獻度極低的雜訊變數（例如缺乏鑑別力的分類）從資料中剔除。

### Phase 3: 決定分群數 k (Hierarchical Dendrogram)

讓資料本身反映出最佳的結構：

1. **資料抽樣 (Sampling)**
   - 為了避免 O(n2) 的龐大運算量，隨機抽取 5,000 至 10,000 筆資料作為代表。
2. **計算距離矩陣 (Gower's Distance)**
   - 計算 Gower's Distance，這是一種能同時處理數值與類別特徵，並融合出單一距離矩陣的演算法。
3. **繪製樹狀圖並切分**
   - 使用 `Average Linkage` 建立階層樹狀圖並繪製出來。
   - **判讀**：尋找圖中**最長的垂直線段**（代表合併難度最高的地方），在該段中間畫一條水平虛線，虛線與垂直線的**交點數量即為最佳的**k**值**。

### Phase 4: 正式分群

取得 k 值後，將 Phase 2 篩選後保留下來的**全體資料特徵**，投入 **K-Prototypes 演算法**中進行正式的群體劃分。