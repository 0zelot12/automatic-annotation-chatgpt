import pandas as pd

from pet_document import PetDocument


class PetDataset:
    """
    Singleton class for accessing the PET dataset.

    This class ensures that only one instance is created and provides a global
    point of access to the pet dataset.

    Attributes:
    - _instance (PetDataset): The single instance of the PetDataset class.
    - _data (pd.DataFrame): The pet dataset loaded from a .parquet file.

    Methods:
    - __new__(cls): Creates a new instance if it doesn't exist, otherwise returns
      the existing instance.
    - get_data(self): Returns the loaded dataframe.

    Usage:
    ```python
    # Creating an instance of the PetDataset class
    pet_data_instance = PetDataset()

    # Accessing the pet dataset
    data = pet_data_instance.get_data()
    ```

    Note: The pet dataset is loaded from a parquet file during the creation of
    the first instance.
    """

    _instance = None
    _data = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PetDataset, cls).__new__(cls)
            cls._data = pd.read_parquet("./assets/pet_dataset.parquet")
        return cls._instance

    def get_data(self):
        return self._data

    def get_document(self, document_number: int) -> PetDocument:
        return PetDocument(
            name=self._data.iloc[document_number]["document name"],
            tokens=self._data.iloc[document_number]["tokens"],
            ner_tags=self._data.iloc[document_number]["ner_tags"],
        )
