# 建立分類模型流程
## 理解問題
先買後付信用風險及違約預測
問題為預測用戶是否會違約
目標變數： default_flag — 1 = 違約，0 = 準時付款 (customer_segment 其實也可以是目標變數)
代價:邏輯上偽陰性代價會較高，因為判斷準時付款卻違約才可能造成公司實際損失
產出形式:明確的類別標籤 1,0

## 資料理解
確定變數定義以及判斷變數定義與目標變數的關係
進行時間特徵的區分

## 資料品質評估
是否有缺失值、重複紀錄或是標籤雜訊、類別不平衡、抽樣偏誤、離群值、編碼不一致、有無冗餘變數

## 資料準備
切割資料集：因為分類屬於預測任務，必須將資料切割為訓練集 (Training set)與測試集 (Test set) 。 
將訓練集資料整理後丟給下一步驟進行假設檢定與相關性分析。 
避免資料外洩 (Data Leakage)：確保在切割資料前，沒有使用到未來預測時無法取得的資訊（例如不能用全部資料來做縮放或插值補值）。
進行資料清理，針對不同選定模型進行編碼類別變數 (Encoding categorical variables) 以及縮放數值變數 。 

## 挑選模型輸入特徵
利用卡方與 IV 來篩選出類別型特徵
利用 Mann-Whitney U 來篩選出 ordinal, interval, ratio 型態特徵
利用 Spearman correlation 來剔除高度相關 ordinal, interval, ratio 型態特徵

## 建立模型 (Pattern Discovery and Modeling)
選擇使用 Random Forest, XGBoost, DNN
建構模型

## 模型評估 (Evaluation)
這個階段要檢驗模型是否能推廣到未看過的資料 (Unseen data) 上 。
- 檢視預測機率的分桶違約率（機率校準度 Calibration）
- ROC-AUC 與 AUC-PR
- 找到對於兩倍 Recall 的 F2-Score 最佳化門檻
- 計算不同門檻下 混淆矩陣、Accuracy、Precision、Recall、F1-score

## 步驟七：超越指標的模式評估 (Pattern Evaluation Beyond Metrics)
說明 Evaluation 的各步驟情境意義
比較三種模型在各步驟評估下的表現

總結
- Is the pattern practically important? (說明因為是擬合出來的資料所以並訓練結果沒有實務價值)
- What is the cost of acting on the pattern incorrectly? (說明一下問題理解部分的"邏輯上偽陰性代價會較高，因為判斷準時付款卻違約才可能造成公司實際損失")
- What limitations must be reported? (說明讓 Recall 提升會造成甚麼問題?)

## 步驟八：解釋 (Interpretation)
釋模型為何會產生特定的預測或規則 。  釐清是哪些變數或特徵驅動了這個分類模式 ，並明確說明結果能適用於哪些群體 。

## 步驟九：溝通 (Communication)
將分析結果轉化為能支持決策的資訊 。  完整的溝通應包含：最初的分析問題、使用的方法、主要的分類結果、評估證據、模型的限制，以及最終建議採取的行動 。