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
- ~~整理前三步驟結論能怎麼幫助資料探勘~~

# ~~重新整理出了 clustering 要做的事情 (5/17)~~
詳情見 cluster_guide.md
- ~~前處理~~
- 特徵篩選
    - ~~列出處理前類別與處理後類別~~
    - 針對不同類別作檢定篩出與 flag 有關變數
    - Spearman Correlation 過濾
    - FAMD 貢獻度檢定 (Factor Analysis of Mixed Data) 過濾

- 決定群數
- k-prototype


# ~~完成前處理(5/18)~~
詳情請見 01_data_pre_briefing.md
03 step 已經列出處理前類別與處理後類別
category: Chi-Square-independence
ordinal:Mann-Whitney 獨立同分布或是異分布(陳柏宇需要聲這些類別在 default_flag = 0,1 下的分布圖，盧再去根據分布做同分布或是異分布)
Interval/ratio: Mann-Whitney 只有 app_usage_frequency 做獨立同分布，其餘 獨立異分布
ratio 中例外: risk_score 做 t-test 異分布
ordinal/interval/ratio: 混在一起做 spearman，篩出相關度>0.75的項目

~~# 架構流程調整討論 (2026-05-21)~~

針對 docs/prediction_flow.md 的流程調整估時與風險評估：

- 團隊 4 人、各自負責 notebook 的方式下，要補齊切分→訓練→評估→解釋→溝通，整體合理估時約 1.5–3 週。
- 如果你負責步驟 9（溝通/報告），單獨工期約 3–6 個工作天，但會被前面評估與解釋性輸出卡住。
- 主要風險：資料外洩修正（切分前/後流程調整）、模型與評估模組化、解釋性輸出不足導致報告難寫。

現有架構與問題：
- 現有檔案結構：notebooks\01–04 為主流程；src/ 只有 data_loader.py；scripts/ 只有 messages.py；Makefile 僅提供 data/eda/preprocess 任務；config.yaml 管理資料路徑與 Kaggle。
- 進度狀態：01/02 已試跑並產出 data/interim；03 有讀檔與欄位問題需修；04 尚未完成。
- 資料流問題：目前主要走 data/raw→data/interim，data/processed 尚未納入主流程，切分與後處理混在 01，易有資料外洩風險。
- 自動化不足：train/evaluate/interpret/report 尚無 CLI 或模組化出口，難以重現與產出報告。

修改的具體 steps：
1. 在 docs/prediction_flow.md 明確步驟與輸入/輸出，作為流程單一真相來源。
2. 拆分 notebooks\01_data_preprocessing.ipynb 成前切分與後處理，並保存 raw/interim/processed。
3. 補齊 split/preprocess/train/evaluate/interpret/report 的模組與 CLI（scripts），確保只以 train fit/取分位數。
4. Makefile 增加 train/evaluate 入口，串接 scripts 以便重現。
5. 更新 notebooks\04_data_mining.ipynb 以呼叫模組並輸出 reports/。

為了縮短開發時間的最小改動路徑：

可保留不動
- src/data_loader.py
- config.yaml 內的資料路徑與 Kaggle 設定
- Makefile 的 data/eda/preprocess 任務
- 既有 EDA 圖表與欄位定義文件

必須修改/新增
- 拆分 notebooks\01_data_preprocessing.ipynb 的前後流程
- 新增/補齊 split、模型、評估模組或 scripts
- 更新 notebooks\04_data_mining.ipynb
- 補上報告輸出流程（供步驟 9 使用）

scripts 的用途說明：
- scripts 是 CLI 入口，讓 notebook 的流程可以用命令重現與自動化（可掛到 Makefile 的 train/evaluate）

01_data_preprocessing.ipynb 拆分建議：
- 前切分：載入、資料品質檢查、變數分類、定義 target/features、train/val/test split、保存 raw/interim
- 後處理：時間特徵、Winsor（只用 train 分位數）、log 轉換、編碼/標準化（只 fit train）、保存 processed

## 補充整理（2026-05-22）
- 整體架構（調整後）：DataLoader/Config → 前切分流程 → data/raw + data/interim → 後處理流程 → data/processed(train/val/test) → scripts/train|evaluate|interpret|report → reports/（供步驟 9）
- scripts 是否必須：不強制；建議作為可重現 CLI。notebooks 保留敘事與可視化，僅呼叫 src 函式或 scripts 命令。
- 全體流程應放：docs/prediction_flow.md 作為單一真相來源；若需要更細步驟對照，可新增 docs/pipeline.md（步驟→腳本/輸出路徑）。
- 可能新增：scripts/split_data.py、scripts/preprocess.py、scripts/train.py、scripts/evaluate.py、scripts/interpret.py、scripts/report.py；src/preprocess.py、src/features.py、src/modeling.py、src/evaluation.py、src/interpretation.py、src/reporting.py。
- 可能修改：notebooks/01_data_preprocessing.ipynb、notebooks/04_data_mining.ipynb、Makefile(train/evaluate)、docs/prediction_flow.md、config.yaml（參數/路徑）。


## 03_statistical_methods.ipynb (2026/05/21)
~~Notebook重點問題：target 未定義，Cell 16/19/24 會 NameError；preprocessed_data_types 重複且第一版欄位名錯（*_Log1p, credit_score），易誤用；~~

Mann‑Whitney 清單硬寫未用 dict；Cell 16 依賴前一格 import；~~Chi‑square 只檢查期望次數未處理違反假設~~ 

Briefing問題：結論缺乏可追溯性（無 p 值/樣本數/資料版本/對應 cell），多重比較未提；“Very different”僅視覺描述，建議量化標準。

## 直接按照 prediction_flow 改整體流程(05/24)