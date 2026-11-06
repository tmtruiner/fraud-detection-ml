from dataclasses import dataclass
from pathlib import Path

from .ingestion import DataIngestion


@dataclass(frozen=True)
class DataSplittingConfig:
    train_data_path: Path = Path("data/processed") / "train.csv"
    validation_data_path: Path = Path("data/processed") / "validation.csv"
    test_data_path: Path = Path("data/processed") / "test.csv"

    train_size: float = 0.7
    validation_size: float = 0.5


class DataSplitting:
    def __init__(self) -> None:
        self.splitting_config = DataSplittingConfig()
        self.data = DataIngestion()

    def initiate_data_split(self) -> tuple[Path, Path, Path]:
        df = self.data.initiate_data_ingestion()

        train_length = int(df.shape[0] * self.splitting_config.train_size)
        train_max_step = df.iloc[train_length]['step'] 

        train_set = df[df['step'] <= train_max_step] #Step 323 is ~70% of the dataset
        other_set = df[df["step"] > train_max_step]

        other_length = int(other_set.shape[0] * self.splitting_config.validation_size)
        other_max_step = other_set.iloc[other_length]['step']

        validation_set = other_set[other_set['step'] <= other_max_step]
        test_set = other_set[other_set['step'] > other_max_step]

        if all((
            Path("data/processed").exists(),
            self.splitting_config.train_data_path.exists(),
            self.splitting_config.validation_data_path.exists(),
            self.splitting_config.test_data_path.exists()
            
        )):
            pass

        else:  
            Path("data/processed").mkdir(parents=True, exist_ok=True)

            train_set.to_csv(self.splitting_config.train_data_path, index=False)
            validation_set.to_csv(self.splitting_config.validation_data_path, index=False)
            test_set.to_csv(self.splitting_config.test_data_path, index=False)

        return (
            train_set,
            validation_set,
            test_set
        )