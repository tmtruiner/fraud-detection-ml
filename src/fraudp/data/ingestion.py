from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from fraudp.utils import load_config, resolve_path

config = load_config()
RAW_DATA_PATH = resolve_path(config["raw"]["fraud_log"])

@dataclass(frozen=True)
class DataIngestionConfig:
    raw_data_path: Path = Path(RAW_DATA_PATH)


class DataIngestion:
    def __init__(self) -> None:
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self) -> pd.DataFrame:
        return pd.read_csv(self.ingestion_config.raw_data_path)