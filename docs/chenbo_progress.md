# 專案目前大致架構(05/10)

已完成整體盤點。這個專案是 BNPL（先買後付）違約風險預測 的資料科學專案（見 [README.md](http://readme.md/)、config.yaml、src/data_loader.py）。

架構重點

- data/：raw、interim、processed 三層資料流。
- notebooks/：01 前處理、02 EDA、03/04 統計與建模（規劃中）。
- src/：核心程式，現有 data_loader.py（設定讀取、Kaggle下載、資料I/O）。
- models/、reports/figures/：模型與輸出圖表。
- Makefile + pyproject.toml：環境、任務與套件管理。

使用方式（建議）

1. 建環境並安裝：make setup-venv、make install-all
2. 下載/載入資料：make data（搭配 Kaggle API）
3. 分析流程：make preprocess → make eda
4. 驗證與清理：make test、make clean

目前缺口：03/04 notebook、tests/ 與部分 src 模組尚未完整。

# 目前 data_processing 重點(05/10)

當然可以，notebooks\01_data_preprocessing.ipynb 可重點看成「把 raw 資料整理成可分析中介資料」的流程。

內容重點（章節）

**01 資料預處理：初始化、載入 ConfigLoader/DataLoader、load_data()。**

1. 資料品質檢查：[df.info](http://df.info/)()、缺值統計、重複值檢查。
2. 變數分類：依統計型態分 Nominal/Ordinal/Discrete/Continuous/Interval。
3. 時間特徵工程：由 transaction_date 萃取年/月/日/星期/是否週末。
4. 離群值處理：handle_outliers_iqr() 以 IQR 做截尾/修正。
5. Log 轉換：plot_log_comparison() 比較轉換前後分布（含 log1p）。
6. 儲存結果：loader.save_interim_data(df, "01_preprocessed.csv")。

使用方法（建議步驟）

1. 先在專案根目錄啟動 Notebook 環境。
2. 依序執行所有 cell（此本內容有前後依賴）。
3. 確認 data/raw 有資料；沒有則 load_data() 會依設定嘗試抓 Kaggle。
4. 執行完成後，到 data/interim/ 取 01_preprocessed.csv 供下一本 EDA 使用。

注意

- transaction_date 轉 datetime 使用 errors='coerce'，無效日期會變 NaT。
- IQR 與 Log 轉換會改變數值分布，建議保留原始欄位備查。

# 目前 EDA 重點整理(05/10)

可以，這本 notebooks\02_exploratory_data_analysis.ipynb 是在做預處理後資料的結構化 EDA，重點如下：

重點內容

**02 探索性資料分析 (EDA)**

- 載入資料：用 ConfigLoader/DataLoader，讀 interim 階段資料。
1. 變數統計分類與摘要
分成 Categorical / Ordinal / Interval / Ratio 做分布與描述統計。
2. 時間序列特徵分析
針對日期欄位檢查缺失、分布，並做時間特徵檢視。
3. 相關性分析 (Spearman)
對編碼後欄位計算 corr(method='spearman')，並以熱圖呈現關聯。

如何使用

1. 先完成 01_data_preprocessing.ipynb，確保 data/interim 有資料。
2. 開啟本 notebook，由上到下依序執行（有前後依賴）。
3. 觀察各型態變數分布、類別比例與時間特徵，再看 Spearman 熱圖找重要關聯。
4. 將結果用於下一步統計檢定/建模特徵選擇。

注意

- 此本主要偏分析展示，未看到明確輸出圖檔/報表存檔步驟。
- 若要可重現報告，建議補 savefig 或輸出統計摘要檔。

# 環境設置 for @ChenBo (5/10)

確認環境存在：dataMining ✅

- 確認版本：Python
3.11.15、pip 26.0.1 ✅
- 安裝專案：conda run --no-capture-output -n dataMining python -m pip install -e . ✅
- 驗證依賴與專案模組：pandas/sklearn/matplotlib/seaborn + src.data_loader ✅

接下來執行

conda activate dataMining 
make env-info
make data

# 環境設置執行紀錄 for @ChenBo (5/11)

- 已執行指令 1：`conda run --no-capture-output -n dataMining python -c "import src.data_loader; print('OK')"` → 輸出 `OK` ✅
- 已執行指令 2：`conda run --no-capture-output -n dataMining python -c "import sys; print(sys.executable)"` → 輸出 `C:\Users\fromn\miniconda3\envs\dataMining\python.exe` ✅
- 結論：`dataMining` 環境可正常載入專案模組，環境設置完成 ✅

# 試跑 01_data_preprocessing.ipynb (5/11)
所有儲存格已經跑過
加載了資料原始檔案到 data/raw 
產出到 data/interim

疑問:
- cell 7 target_columns 也太少，數值型別欄位應該更多才對(ans. @EricChen 說會補上)
- cell 8 log 對象 如何挑出來的 (02中有列出所有的分布狀況)
- cell 8 log 完後是否並無存到 interim 輸出中 (ans. 有的，function 仔細看有 return)
- 取 log 完後為何不直接取代原本的數值 (確實需要保留)

# 試跑 02_exploratory_data_analysis.ipynb (5/11)
改了 cell 9 因為 pandas 版本不同而造成的型別錯誤

疑問:
- data/process, data/processed 兩個都沒用到，應該用 processed 來取代 interim 嗎(會再改正)

# 試跑 03_statistical_methods.inpynb (5/11)
第一步讀檔的路徑就發生錯誤

疑問:
- 欲取用之檔案似乎為 raw_data? 為何不用 processed 解?(已經解決)

# 03_statistical_methods.inpynb (5/13)

我幫你整理好 03_statistical_methods.ipynb 的流程重點如下：

資料先從 ../data/raw/raw_bnpl_data.csv 讀入，接著做日期拆解（年/月/日/週幾/是否週末）與偏態數值的 log1p 轉換，並輸出前處理後資料到 
../data/interim/01_preprocessed.csv
。之後再載入此檔進行統計分析。

分析分三塊：分類變數用卡方檢定（含 Cramér’s V）看與 default_flag 的關聯；數值變數用 Spearman 相關看單調關係與共線性；再用 
Mann–Whitney U 比較違約/非違約兩組分布差異。整體結論是：行為特徵（
missed_payments, repayment_delay_days, risk_score）最有力，傳統 credit_score 幾乎不顯著。另有 heatmap 輔助解讀相關結構。

疑問:
- 第一格的資料來源為何不是直接取用處理完的資料，前面應該已經做好資料處理了(已經解決)
- 少了對時間分析
- credit_score 應該用 interval 方法去做?
 
# 03_statistical_methods.inpynb 修正及增加功能計畫 (5/14)
後面階段的分析都不是用取 log 完的結果去進行分析
所以我開始更改
1. 此檔案路徑問題 (已經解決)
2. 沒有用 log 後數值分析的問題 (spearson 是 ranking 的，所以單調函數對結果沒有影響，顆顆)
3. 想多做 PCA

# 03_statistical_methods.inpynb 分析能用結果 (5/14)
category data 中只有 employment_type 與結果有足夠關聯度

# 列出截至目前為止的待處理事項 (5/16)
- ~~push 目前進度上去~~
- ~~看 @EricChen 改的怎麼樣~~
- ~~merge 各個分支~~
- 整理前三步驟結論能怎麼幫助資料探勘
- 做 PCA