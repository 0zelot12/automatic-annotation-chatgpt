import pandas as pd


class PetDataset:
    _instance = None
    _data = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PetDataset, cls).__new__(cls)
            cls._data = pd.read_parquet(
                "./assets/pet_dataset.parquet"
            )
        return cls._instance

    def get_data(self):
        return self._data
