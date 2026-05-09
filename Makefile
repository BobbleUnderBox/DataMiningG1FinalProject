# ============================================================
# 0. 環境偵測 (支援 Conda, venv, Global)
# ============================================================

# 偵測環境優先順序: Conda -> Active Venv -> Local Venv -> System

ifeq ($(OS),Windows_NT)
    NULL := NUL
else
    NULL := /dev/null
endif

# 偵測環境優先順序: Active Venv -> Local Venv -> Conda -> System

ifdef VIRTUAL_ENV
	# 使用 subst 將反斜線轉為正斜線，避免 sh.exe 轉義問題
	CLEAN_VENV := $(subst \,/,$(VIRTUAL_ENV))
    DETECTED_PYTHON := $(CLEAN_VENV)/Scripts/python.exe
    ENV_TYPE := Virtualenv (Active)
else
	ifneq ($(wildcard .venv/Scripts/python.exe),)
		DETECTED_PYTHON := .venv/Scripts/python.exe
		ENV_TYPE := Local venv (./.venv)
	else
		ifdef CONDA_PREFIX
			CLEAN_CONDA := $(subst \,/,$(CONDA_PREFIX))
			DETECTED_PYTHON := $(CLEAN_CONDA)/python.exe
			ENV_TYPE := Conda ($(notdir $(CONDA_PREFIX)))
		else
			DETECTED_PYTHON := python
			ENV_TYPE := System/Global
		endif
	endif
endif

# 專案變數
PROJECT_NAME := bnpl-credit-risk
PYTHON := $(DETECTED_PYTHON)
PIP := $(PYTHON) -m pip

# 顏色與圖示輸出
BLUE   := \033[0;34m
GREEN  := \033[0;32m
YELLOW := \033[0;33m
NC     := \033[0m
ICON_INFO := 📋
ICON_OK   := ✅
ICON_WARN := ⚠️
ICON_DATA := 📊
ICON_MODEL := 🤖
ICON_SYNC := 🔄
ICON_LOAD := 📥
ICON_CHART := 📊
ICON_GEAR := 🔧
ICON_TEST := 🧪
ICON_SWEEP := 🧹

# Windows 平台相容性修正
ifeq ($(OS),Windows_NT)
    # 使用 Python 處理訊息，這是最可靠的跨平台 UTF-8 解決方案
    MSG := python scripts/messages.py
    # 強制將路徑轉為反斜線，以相容於 cmd.exe
    RUN_PYTHON := set PYTHONIOENCODING=utf-8 && $(subst /,\,$(PYTHON))
    RUN_PIP    := $(subst /,\,$(PIP))
else
    # Unix-like: 保持原有的彩色與 Emoji 輸出
    MSG := echo
    RUN_PYTHON := $(PYTHON)
    RUN_PIP    := $(PIP)
endif

.PHONY: help install data eda preprocess train evaluate clean test lint format env-info sync-data

help:
ifeq ($(OS),Windows_NT)
	@$(MSG) help-header-top
	@$(MSG) help-header-mid
	@$(MSG) help-header-bot
	@$(MSG) ""
	@$(MSG) help-env-title
	@$(MSG) help-env-info
	@$(MSG) help-install-all
	@$(MSG) help-setup-venv
	@$(MSG) ""
	@$(MSG) help-data-title
	@$(MSG) help-data
	@$(MSG) help-sync-data
	@$(MSG) help-eda
	@$(MSG) help-preprocess
	@$(MSG) ""
	@$(MSG) help-model-title
	@$(MSG) help-train
	@$(MSG) help-test
	@$(MSG) help-clean-all
	@$(MSG) ""
else
	@echo "$(BLUE)╔════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║   BNPL 信用風險分類專案 - Makefile 任務列表               ║$(NC)"
	@echo "$(BLUE)╚════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(GREEN)$(ICON_INFO) 環境與管理$(NC)"
	@echo "  make env-info         - 顯示當前 Python 環境資訊與路徑"
	@echo "  make install-all      - 安裝所有依賴 (pip install)"
	@echo "  make setup-venv       - 建立並初始化本地 .venv 環境"
	@echo ""
	@echo "$(GREEN)$(ICON_DATA) 資料處理$(NC)"
	@echo "  make data             - 載入資料 (優先使用本地 data/raw)"
	@echo "  make sync-data        - 將 Kaggle 快取資料強制遷移至本地並清理快取"
	@echo "  make eda              - 執行探索性資料分析"
	@echo "  make preprocess       - 資料預處理與特徵工程"
	@echo ""
	@echo "$(GREEN)$(ICON_MODEL) 建模與品質$(NC)"
	@echo "  make train            - 訓練模型"
	@echo "  make test             - 執行單元測試"
	@echo "  make clean-all        - 完全清理 (包括資料、模型、報告)"
	@echo ""
endif

# ============================================================
# 1. 環境管理
# ============================================================

env-info:
ifeq ($(OS),Windows_NT)
	@$(MSG) env-info-header
	@$(MSG) env-info-python "$(shell $(subst /,\,$(PYTHON)) -c "import sys; print(sys.executable)")"
	@$(MSG) env-info-type "$(ENV_TYPE)"
	@$(MSG) env-info-pip "$(shell $(subst /,\,$(PIP)) --version 2>$(NULL) || echo "Not Found")"
	@$(MSG) env-info-dir "$(CURDIR)"
	@$(MSG) ""
	@$(MSG) env-info-hint
else
	@echo "$(BLUE)$(ICON_INFO) 當前環境資訊:$(NC)"
	@echo "  Python 路徑: $(shell $(PYTHON) -c "import sys; print(sys.executable)")"
	@echo "  環境類型:    $(ENV_TYPE)"
	@echo "  Pip 版本:    $(shell $(PIP) --version 2>/dev/null || echo 'Not Found')"
	@echo "  工作目錄:    $(CURDIR)"
	@echo ""
	@echo "$(YELLOW)提示: 如果環境不正確，請先激活你的 Conda 環境或執行 'make setup-venv'$(NC)"
endif

setup-venv:
ifeq ($(OS),Windows_NT)
	@$(MSG) setup-venv-start
	python -m venv .venv
	@$(MSG) setup-venv-ok
else
	@echo "$(BLUE)$(ICON_GEAR) 正在建立本地虛擬環境 (.venv)...$(NC)"
	python -m venv .venv
	@echo "$(GREEN)$(ICON_OK) 建立完成。請執行 \".\.venv\Scripts\Activate\" 激活環境後再執行 \"make install-all\"$(NC)"
endif

install-all:
ifeq ($(OS),Windows_NT)
	@$(MSG) install-all-start "$(ENV_TYPE)"
	$(RUN_PIP) install -e ".[dev,ml]"
	@$(MSG) install-all-ok
else
	@echo "$(BLUE)$(ICON_LOAD) 正在環境 [$(ENV_TYPE)] 中安裝依賴...$(NC)"
	$(PIP) install -e ".[dev,ml]"
	@echo "$(GREEN)$(ICON_OK) 安裝完成$(NC)"
endif

# ============================================================
# 2. 資料處理
# ============================================================

sync-data:
ifeq ($(OS),Windows_NT)
	@$(MSG) sync-data-start
	$(RUN_PYTHON) -c "from src.data_loader import DataLoader, ConfigLoader; loader=DataLoader(ConfigLoader.load_config()); loader.downloader.sync_to_local()"
	@$(MSG) sync-data-ok
else
	@echo "$(BLUE)$(ICON_SYNC) 正在同步與本地化數據...$(NC)"
	$(PYTHON) -c "from src.data_loader import DataLoader, ConfigLoader; loader=DataLoader(ConfigLoader.load_config()); loader.downloader.sync_to_local()"
	@echo "$(GREEN)$(ICON_OK) 數據已遷移至 data/raw，Kaggle 快取已清理$(NC)"
endif

data:
ifeq ($(OS),Windows_NT)
	@$(MSG) data-load-start
	$(RUN_PYTHON) -c "from src.data_loader import load_data; load_data()"
else
	@echo "$(BLUE)$(ICON_LOAD) 載入資料...$(NC)"
	$(PYTHON) -c "from src.data_loader import load_data; load_data()"
endif

eda:
ifeq ($(OS),Windows_NT)
	@$(MSG) eda-start
	$(RUN_PYTHON) -m jupyter notebook notebooks/02_exploratory_data_analysis.ipynb
else
	@echo "$(BLUE)$(ICON_CHART) 執行探索性資料分析...$(NC)"
	$(PYTHON) -m jupyter notebook notebooks/02_exploratory_data_analysis.ipynb
endif

preprocess:
ifeq ($(OS),Windows_NT)
	@$(MSG) preprocess-start
	$(RUN_PYTHON) -m jupyter notebook notebooks/01_data_preprocessing.ipynb
else
	@echo "$(BLUE)$(ICON_GEAR) 執行資料預處理...$(NC)"
	$(PYTHON) -m jupyter notebook notebooks/01_data_preprocessing.ipynb
endif

# ============================================================
# 3. 其他工具
# ============================================================

test:
	$(RUN_PYTHON) -m pytest tests/ -v

clean:
ifeq ($(OS),Windows_NT)
	@$(MSG) clean-start
	rm -rf .pytest_cache/ .mypy_cache/ .coverage htmlcov/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>$(NULL) || true
else
	@echo "$(BLUE)$(ICON_SWEEP) 清理暫存文件...$(NC)"
	rm -rf .pytest_cache/ .mypy_cache/ .coverage htmlcov/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
endif

clean-all: clean
ifeq ($(OS),Windows_NT)
	@$(MSG) clean-all-start
	rm -rf data/raw/* data/interim/* data/processed/*
	rm -rf models/* logs/*
else
	@echo "$(BLUE)🗑️  完全清理資料與模型...$(NC)"
	rm -rf data/raw/* data/interim/* data/processed/*
	rm -rf models/* logs/*
endif

status:
ifeq ($(OS),Windows_NT)
	@$(MSG) status-header
	@$(MSG) status-python "$(shell $(subst /,\,$(PYTHON)) --version)"
	@$(MSG) status-data "$(shell dir /b data\raw 2>$(NULL) | find /c /v "")"
else
	@echo "$(BLUE)$(ICON_CHART) 專案狀態:$(NC)"
	@echo "  Python: $(shell $(PYTHON) --version)"
	@echo "  資料集 (data/raw): $(shell ls -1 data/raw 2>/dev/null | wc -l) 個文件"
endif

.DEFAULT_GOAL := help
