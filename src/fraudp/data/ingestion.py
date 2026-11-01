from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class DataIngestionConfig:
    raw_data_path: Path = Path("data/raw") / "fraud_log.csv"
    train_data_path: Path = Path("data/processed") / "train.csv"
    validation_data_path: Path = Path("data/processed") / "validation.csv"
    test_data_path: Path = Path("data/processed") / "test.csv"

    train_size: float = 0.7
    validation_size: float = 0.5



class DataIngestion:
    def __init__(self) -> None:
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self) -> tuple[Path, Path, Path]:
        Path("data/raw").mkdir(parents=True, exist_ok=True)
        df = pd.read_csv(self.ingestion_config.raw_data_path)

        train_length = int(df.shape[0] * self.ingestion_config.train_size)
        train_max_step = df.iloc[train_length]['step'] 

        train_set = df[df['step'] <= train_max_step] #Step 323 is ~70% of the dataset
        other_set = df[df["step"] > train_max_step]

        other_length = int(other_set.shape[0] * self.ingestion_config.validation_size)
        other_max_step = other_set.iloc[other_length]['step']

        validation_set = other_set[other_set['step'] <= other_max_step]
        test_set = other_set[other_set['step'] > other_max_step]


        Path("data/processed").mkdir(parents=True, exist_ok=True)

        train_set.to_csv(
            self.ingestion_config.train_data_path, index=False
        )
        validation_set.to_csv(self.ingestion_config.validation_data_path, index=False)

        test_set.to_csv(self.ingestion_config.test_data_path, index=False)

        return (
            self.ingestion_config.train_data_path,
            self.ingestion_config.validation_data_path,
            self.ingestion_config.test_data_path
        )

obj = DataIngestion()
print(obj.initiate_data_ingestion())
