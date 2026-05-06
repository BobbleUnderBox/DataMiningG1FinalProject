import sys

messages = {
    "help-header-top": "╔════════════════════════════════════════════════════════════╗",
    "help-header-mid": "║   BNPL 信用風險分類專案 - Makefile 任務列表               ║",
    "help-header-bot": "╚════════════════════════════════════════════════════════════╝",
    "help-env-title": "[INFO] 環境與管理",
    "help-env-info": "  make env-info         - 顯示當前 Python 環境資訊與路徑",
    "help-install-all": "  make install-all      - 安裝所有依賴 (pip install)",
    "help-setup-venv": "  make setup-venv       - 建立並初始化本地 .venv 環境",
    "help-data-title": "[DATA] 資料處理",
    "help-data": "  make data             - 載入資料 (優先使用本地 data/raw)",
    "help-sync-data": "  make sync-data        - 將 Kaggle 快取資料強制遷移至本地並清理快取",
    "help-eda": "  make eda              - 執行探索性資料分析",
    "help-preprocess": "  make preprocess       - 資料預處理與特徵工程",
    "help-model-title": "[MODEL] 建模與品質",
    "help-train": "  make train            - 訓練模型",
    "help-test": "  make test             - 執行單元測試",
    "help-clean-all": "  make clean-all        - 完全清理 (包括資料、模型、報告)",
    "env-info-header": "[INFO] 當前環境資訊:",
    "env-info-python": "  Python 路徑: {0}",
    "env-info-type": "  環境類型: {0}",
    "env-info-pip": "  Pip 版本: {0}",
    "env-info-dir": "  工作目錄: {0}",
    "env-info-hint": "提示: 如果環境不正確，請先激活你的 Conda 環境或執行 'make setup-venv'",
    "setup-venv-start": "[GEAR] 正在建立本地虛擬環境 (.venv)...",
    "setup-venv-ok": "[OK] 建立完成。請執行 '.\\.venv\\Scripts\\Activate' 激活環境後再執行 'make install-all'",
    "install-all-start": "[LOAD] 正在環境 [{0}] 中安裝依賴...",
    "install-all-ok": "[OK] 安裝完成",
    "sync-data-start": "[SYNC] 正在同步與本地化數據...",
    "sync-data-ok": "[OK] 數據已遷移至 data/raw，Kaggle 快取已清理",
    "data-load-start": "[LOAD] 載入資料...",
    "data-load-ok": "✅ 資料載入完成，形狀: {0}",
    "eda-start": "[CHART] 執行探索性資料分析...",
    "preprocess-start": "[GEAR] 執行資料預處理...",
    "clean-start": "[CLEAN] 清理暫存文件...",
    "clean-all-start": "🗑️  完全清理資料與模型...",
    "status-header": "[CHART] 專案狀態:",
    "status-python": "  Python: {0}",
    "status-data": "  資料集 (data/raw): {0} 個文件",
}

def main():
    if len(sys.argv) < 2:
        return
    key = sys.argv[1]
    if key in messages:
        msg = messages[key]
        if len(sys.argv) > 2:
            msg = msg.format(*sys.argv[2:])
        # Ensure UTF-8 output on Windows
        if sys.platform == "win32":
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        print(msg)

if __name__ == "__main__":
    main()
