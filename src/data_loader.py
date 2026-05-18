"""
資料載入與管理模組
支持多使用者、多平台、配置化的 Kaggle 資料集下載與本地快取管理
"""

import os
import sys
import yaml
import logging
from pathlib import Path
from typing import Optional, Dict, Any, cast
from getpass import getpass

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 定義專案根目錄（相對於此檔案的兩層上層目錄）
PROJECT_ROOT = Path(__file__).parent.parent.absolute()


class ConfigLoader:
    """設定檔載入器"""
    
    @staticmethod
    def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
        """
        載入 YAML 設定檔
        
        Args:
            config_path: 設定檔路徑，相對於專案根目錄
            
        Returns:
            設定字典
        """
        # 如果設定路徑不存在，嘗試從專案根目錄查找
        path_obj = Path(config_path)
        if not path_obj.exists():
            config_path = str(PROJECT_ROOT / config_path)
        
        if not Path(config_path).exists():
            raise FileNotFoundError(f"設定檔不存在: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        if not isinstance(config, dict):
            raise ValueError(f"設定檔格式錯誤，應為字典/對象: {config_path}")
        
        logger.info(f"✅ 設定檔已載入: {config_path}")
        return cast(Dict[str, Any], config)


class DataDownloader:
    """Kaggle 資料集下載管理器"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化下載器
        
        Args:
            config: 設定字典（來自 config.yaml）
        """
        self.config = config
        self.kaggle_config = config['kaggle']
        self.data_config = config['data']
        
        # 建立資料目錄
        self._ensure_data_dirs()
    
    def _ensure_data_dirs(self):
        """確保資料目錄存在"""
        for dir_key in ['raw_dir', 'interim_dir', 'processed_dir']:
            # 強制將相對路徑轉為專案根目錄下的絕對路徑
            dir_path = PROJECT_ROOT / self.data_config[dir_key]
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"✅ 目錄確認存在: {dir_path}")
    
    def _setup_kaggle_auth(self) -> bool:
        """
        設定 Kaggle API 身份驗證
        支持三種方法：環境變數 / 憑證檔案 / 互動式輸入
        
        Returns:
            認證成功傳回 True
        """
        auth_method = self.kaggle_config['auth_method']
        
        if auth_method == "credentials_file":
            # 使用 ~/.kaggle/kaggle.json 檔案（Kaggle 官方建議）
            credentials_path = Path(self.kaggle_config['credentials_path']).expanduser()
            if credentials_path.exists():
                logger.info(f"✅ 使用憑證檔案認證: {credentials_path}")
                return True
            else:
                logger.warning(f"⚠️  憑證檔案不存在: {credentials_path}")
                return False
        
        elif auth_method == "env_vars":
            # 方法1：從環境變數讀取（建議）
            username = os.environ.get('KAGGLE_USERNAME')
            api_key = os.environ.get('KAGGLE_KEY')
            
            if username and api_key:
                logger.info("✅ 從環境變數讀取 Kaggle 憑證")
                return True
            
            # 方法2：從設定檔讀取（備選，僅用於演示）
            config_username = self.kaggle_config.get('username', '').strip()
            config_api_key = self.kaggle_config.get('api_key', '').strip()
            
            if config_username and config_api_key:
                os.environ['KAGGLE_USERNAME'] = config_username
                os.environ['KAGGLE_KEY'] = config_api_key
                logger.info("✅ 使用設定檔中的 Kaggle 憑證（僅用於演示）")
                return True
            
            # 方法3：互動式輸入（使用者互動）
            logger.warning("⚠️  未檢測到 Kaggle 憑證，需要互動式輸入")
            return self._interactive_auth()
        
        elif auth_method == "custom_token_file":
            # 使用自定義純文字 token 檔案 (例如 C:\Users\User\.kaggle\access_token)
            token_path = Path(self.kaggle_config['credentials_path']).expanduser()
            if token_path.exists():
                try:
                    with open(token_path, 'r', encoding='utf-8') as f:
                        token = f.read().strip()
                        os.environ["KAGGLE_API_TOKEN"] = token
                    logger.info(f"✅ 已讀取自定義 Token 並設定環境變數: {token_path}")
                    return True
                except Exception as e:
                    logger.error(f"❌ 讀取自定義 Token 檔案失敗: {e}")
                    return False
            else:
                logger.warning(f"⚠️  自定義 Token 檔案不存在: {token_path}")
                return False
        
        return False
    
    def _interactive_auth(self) -> bool:
        """互動式 Kaggle 身份驗證"""
        try:
            print("\n" + "="*60)
            print("🔐 Kaggle 身份驗證")
            print("="*60)
            print("請從 https://www.kaggle.com/settings/account 取得 API Token")
            print("下載 kaggle.json，放在 ~/.kaggle/ 目錄下")
            print("-"*60)
            
            username = input("請輸入您的 Kaggle 使用者名稱 (或直接回車略過互動): ").strip()
            
            if not username:
                logger.warning("⚠️  略過互動式認證")
                return False
            
            api_key = getpass("請輸入您的 Kaggle API Key (輸入不顯示): ")
            
            if not api_key:
                logger.warning("⚠️  API Key 為空，認證失敗")
                return False
            
            os.environ['KAGGLE_USERNAME'] = username
            os.environ['KAGGLE_KEY'] = api_key
            logger.info("✅ 互動式認證成功")
            return True
        
        except Exception as e:
            logger.error(f"❌ 互動式認證失敗: {e}")
            return False
    
    def download_dataset(self, force_redownload: bool = False) -> str:
        """
        下載 Kaggle 資料集
        
        Args:
            force_redownload: 是否強制重新下載（忽略快取）
            
        Returns:
            資料集檔案的完整路徑
        """
        if not self.kaggle_config['enable_download']:
            logger.info("⚠️  Kaggle 下載已停用，嘗試使用本地快取...")
            return self._get_cached_dataset()
        
        try:
            import kagglehub
        except ImportError:
            logger.error("❌ kagglehub 模組未安裝，請執行: pip install kagglehub")
            raise
        
        # 設定認證
        if not self._setup_kaggle_auth():
            logger.error("❌ Kaggle 認證失敗")
            raise RuntimeError("無法進行 Kaggle 認證")
        
        # 下載資料集
        dataset_id = self.kaggle_config['dataset_id']
        logger.info(f"📥 正在下載資料集: {dataset_id}")
        
        try:
            path = kagglehub.dataset_download(dataset_id)
            logger.info(f"✅ 資料集已下載至: {path}")
            return self._find_csv_in_directory(path)
        
        except Exception as e:
            logger.error(f"❌ 下載失敗: {e}")
            raise
    
    def _find_csv_in_directory(self, directory: str) -> str:
        """
        在指定目錄中查找 CSV 檔案
        
        Args:
            directory: 目錄路徑
            
        Returns:
            找到的 CSV 檔案完整路徑
        """
        csv_files = list(Path(directory).glob('*.csv'))
        
        if not csv_files:
            raise FileNotFoundError(f"在 {directory} 中沒有找到 CSV 檔案")
        
        # 傳回第一個 CSV 檔案
        csv_file = csv_files[0]
        logger.info(f"✅ 找到 CSV 檔案: {csv_file.name}")
        return str(csv_file)
    
    def sync_to_local(self, source_path: Optional[str] = None) -> str:
        """
        將資料從快取（或其他來源）同步至專案本地的 data/raw 目錄
        確保資料只有一份且存放在專案內。
        
        Args:
            source_path: 來源路徑，若為 None 則嘗試從快取中尋找
            
        Returns:
            本地 data/raw 中的資料路徑
        """
        import shutil
        
        raw_dir = PROJECT_ROOT / self.data_config['raw_dir']
        raw_filename = self.config['data'].get('raw_filename', 'Buy_Now_Pay_Later_BNPL_CreditRisk_Dataset.csv')
        dest_path = raw_dir / raw_filename
        
        # 如果 source_path 為空，嘗試找快取
        if not source_path:
            try:
                source_path = self._get_cached_dataset()
            except FileNotFoundError:
                logger.error("❌ 無法同步：找不到來源資料")
                raise
        
        # 如果來源與目的地相同，直接傳回
        if Path(source_path).resolve() == dest_path.resolve():
            return str(dest_path)
            
        # 搬移檔案
        logger.info(f"🔄 正在將資料遷移至本地: {source_path} -> {dest_path}")
        raw_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, dest_path)
        
        # 檢查是否需要清理快取（若來源在快取中則刪除快取，實現「唯一性」）
        if "kagglehub" in str(source_path).lower():
            logger.info("🧹 清理 Kaggle 快取副本...")
            try:
                # 這裡安全起見只刪除該 CSV
                os.remove(source_path)
            except Exception as e:
                logger.warning(f"⚠️ 無法刪除快取檔案: {e}")
                
        logger.info(f"✅ 資料本地化完成: {dest_path}")
        return str(dest_path)

    def _get_cached_dataset(self) -> str:
        """
        取得快取的資料集
        
        Returns:
            快取資料集的路徑，如果快取不存在則拋出異常
        """
        # 檢查本地 raw 目錄
        raw_dir = PROJECT_ROOT / self.data_config['raw_dir']
        raw_files = list(raw_dir.glob('*.csv'))
        
        if raw_files:
            logger.info(f"✅ 使用本地 raw 目錄中的資料: {raw_files[0]}")
            return str(raw_files[0])
        
        # 檢查 Kaggle 預設快取
        default_cache = Path.home() / ".cache" / "kagglehub"
        cache_files = list(default_cache.glob('**/Buy_Now_Pay_Later*.csv'))
        
        if cache_files:
            logger.info(f"✅ 使用 Kaggle 快取中的資料: {cache_files[0]}")
            return str(cache_files[0])
        
        raise FileNotFoundError(
            "無法找到資料集。請執行 downloader.download_dataset() 進行下載。"
        )


class DataLoader:
    """資料載入管理器"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化資料加載器
        
        Args:
            config: 設定字典
        """
        self.config = config
        self.downloader = DataDownloader(config)
    
    def load_raw_data(self, force_redownload: bool = False) -> pd.DataFrame:
        """
        載入原始資料集
        
        Args:
            force_redownload: 是否強制重新下載
            
        Returns:
            Pandas DataFrame
        """
        # 1. 優先檢查本地 raw 目錄 (PROJECT_ROOT/data/raw)
        raw_dir = PROJECT_ROOT / self.config['data']['raw_dir']
        raw_filename = self.config['data'].get('raw_filename', 'Buy_Now_Pay_Later_BNPL_CreditRisk_Dataset.csv')
        local_path = raw_dir / raw_filename
        
        if local_path.exists() and not force_redownload:
            logger.info(f"✅ 優先使用專案本地資料: {local_path}")
            csv_path = str(local_path)
        else:
            # 2. 若本地無資料或要求重新下載，則走下載/快取流程
            try:
                csv_path = self.downloader.download_dataset(force_redownload)
                # 自動同步到本地以確保唯一性
                csv_path = self.downloader.sync_to_local(csv_path)
            except RuntimeError:
                csv_path = self.downloader._get_cached_dataset()
        
        # 讀取 CSV
        logger.info(f"📖 讀取資料檔案: {csv_path}")
        df = pd.read_csv(csv_path)
        logger.info(f"✅ 資料已載入 | 形狀: {df.shape}")
        
        return df
    
    def load_interim_data(self, filename: str) -> pd.DataFrame:
        """
        從 interim 目錄載入處理中的資料
        
        Args:
            filename: 檔案名稱
            
        Returns:
            Pandas DataFrame
        """
        interim_path = PROJECT_ROOT / self.config['data']['interim_dir'] / filename
        
        if not interim_path.exists():
            raise FileNotFoundError(f"中間資料檔案不存在: {interim_path}")
        
        logger.info(f"📖 讀取中間資料: {interim_path}")
        df = pd.read_csv(interim_path) if interim_path.suffix == '.csv' else \
             pd.read_parquet(interim_path) if interim_path.suffix == '.parquet' else None
        
        if df is None:
            raise ValueError("不支持的檔案格式")
        
        logger.info(f"✅ 中間資料已載入 | 形狀: {df.shape}")
        return df
    
    def load_processed_data(self, filename: str) -> pd.DataFrame:
        """
        從 processed 目錄載入處理完成的資料
        
        Args:
            filename: 檔案名稱
            
        Returns:
            Pandas DataFrame
        """
        processed_path = PROJECT_ROOT / self.config['data']['processed_dir'] / filename
        
        if not processed_path.exists():
            raise FileNotFoundError(f"處理完成的資料檔案不存在: {processed_path}")
        
        logger.info(f"📖 讀取處理完成的資料: {processed_path}")
        df = pd.read_csv(processed_path) if processed_path.suffix == '.csv' else \
             pd.read_parquet(processed_path) if processed_path.suffix == '.parquet' else None
        
        if df is None:
            raise ValueError("不支持的檔案格式")
        
        logger.info(f"✅ 處理完成的資料已載入 | 形狀: {df.shape}")
        return df
    
    def save_interim_data(self, df: pd.DataFrame, filename: str, format: str = 'csv'):
        """
        儲存處理中的資料
        
        Args:
            df: Pandas DataFrame
            filename: 檔案名稱
            format: 檔案格式 ('csv' 或 'parquet')
        """
        interim_dir = PROJECT_ROOT / self.config['data']['interim_dir']
        interim_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = interim_dir / filename
        
        if format == 'csv':
            df.to_csv(filepath, index=False, encoding='utf-8')
        elif format == 'parquet':
            df.to_parquet(filepath, index=False)
        else:
            raise ValueError("不支持的檔案格式")
        
        logger.info(f"✅ 中間資料已儲存 (interim): {filepath}")
    
    def save_processed_data(self, df: pd.DataFrame, filename: str, format: str = 'csv'):
        """
        儲存處理完成的資料
        
        Args:
            df: Pandas DataFrame
            filename: 檔案名稱
            format: 檔案格式 ('csv' 或 'parquet')
        """
        processed_dir = PROJECT_ROOT / self.config['data']['processed_dir']
        processed_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = processed_dir / filename
        
        if format == 'csv':
            df.to_csv(filepath, index=False, encoding='utf-8')
        elif format == 'parquet':
            df.to_parquet(filepath, index=False)
        else:
            raise ValueError("不支持的檔案格式")
        
        logger.info(f"✅ 處理完成的資料已儲存 (processed): {filepath}")


# ============================================================
# 便利函式（供 Notebook 使用）
# ============================================================

def load_data(config_path: str = "config.yaml", 
              force_redownload: bool = False) -> pd.DataFrame:
    """
    便利函式：一行代碼載入資料
    
    使用示例:
        df = load_data()  # 使用預設設定
        df = load_data(force_redownload=True)  # 強制重新下載
    
    Args:
        config_path: 設定檔路徑
        force_redownload: 是否強制重新下載
        
    Returns:
        Pandas DataFrame
    """
    config = ConfigLoader.load_config(config_path)
    loader = DataLoader(config)
    return loader.load_raw_data(force_redownload)


if __name__ == "__main__":
    # 演示用法
    print("="*60)
    print("資料載入模組演示")
    print("="*60)
    
    # 載入設定
    config = ConfigLoader.load_config()
    
    # 初始化載入器
    loader = DataLoader(config)
    
    # 載入資料
    try:
        df = loader.load_raw_data(force_redownload=False)
        print(f"\n✅ 資料載入成功！")
        print(f"形狀: {df.shape}")
        print(f"\n前 5 列:")
        print(df.head())
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        sys.exit(1)

