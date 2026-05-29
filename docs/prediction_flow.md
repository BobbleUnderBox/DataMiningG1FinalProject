# 建立分類模型流程
## 理解問題
先買後付信用風險及違約預測
問題為預測用戶是否會違約
目標變數： default_flag — 1 = 違約，0 = 準時付款 (customer_segment 其實也可以是目標變數)
代價:邏輯上偽陰性代價會較高，因為判斷準時付款卻違約才可能造成公司實際損失
產出形式:明確的類別標籤 1,0

## 資料理解
請見 kaggle 上明確定義
時間特徵的區分應該要放在這裡做

## 資料品質評估
是否有缺失值、重複紀錄或是標籤雜訊、類別不平衡、抽樣偏誤、離群值、編碼不一致、有無冗餘變數

## 資料準備
進行資料清理，例如處理缺失資料、編碼類別變數 (Encoding categorical variables) 以及縮放數值變數 。 
切割資料集：因為分類屬於預測任務，必須將資料切割為訓練集 (Training set)、驗證集(Validation set) 與測試集 (Test set) 。  
避免資料外洩 (Data Leakage)：確保在切割資料前，沒有使用到未來預測時無法取得的資訊（例如不能用全部資料來做縮放或插值補值） 。

演算法 -> 對應每一種資料前處理方式(`debt_to_income_ratio` 先做檢定再決定要不要除去 outliner)

## 步驟五：模式發現與建立模型 (Pattern Discovery and Modeling)
選擇適合的演算法
挑選特徵 (Feature selection) 
設定參數
如果應用場景需要，還必須考慮模型的「可解釋性 (Interpretability)」需求 。 在這個階段，模型會從資料中學習並找出分類規則 (Classification rules) 。

## 步驟六：模型評估 (Evaluation)
這個階段要檢驗模型是否能推廣到未看過的資料 (Unseen data) 上 。
**指標**
- 準確率 (Accuracy)
- 精準度 (Precision)
- 召回率 (Recall)
- F1-score
- ROC-AUC
- 混淆矩陣 (Confusion matrix)


## 步驟七：超越指標的模式評估 (Pattern Evaluation Beyond Metrics)
除了準確度，還要評估模型找出的分類模式是否能跨樣本穩定存在。確認這個分類結果是否有被拿來支持實際決策的價值 。

## 步驟八：解釋 (Interpretation)解
釋模型為何會產生特定的預測或規則 。  釐清是哪些變數或特徵驅動了這個分類模式 ，並明確說明結果能適用於哪些群體 。

## 步驟九：溝通 (Communication)
將分析結果轉化為能支持決策的資訊 。  完整的溝通應包含：最初的分析問題、使用的方法、主要的分類結果、評估證據、模型的限制，以及最終建議採取的行動 。