import pandas as pd

from pet_document import PetDocument

from entity import str_to_entity


# TODO: Rename
def foo(x):
    return float(x.replace("doc-", ""))


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
            df = pd.read_parquet("./assets/pet_dataset.parquet")
            # This doesn't work corretly!
            df["index"] = df["document name"].apply(foo)
            cls._data = df.sort_values(by="index")
        return cls._instance

    def get_data(self):
        return self._data

    def get_document(self, document_number: int) -> PetDocument:
        converted_ner_tags = []
        for ner_tag in self._data.iloc[document_number]["ner_tags"]:
            converted_ner_tags.append(str_to_entity(ner_tag))
        return PetDocument(
            name=self._data.iloc[document_number]["document name"],
            tokens=self._data.iloc[document_number]["tokens"],
            ner_tags=converted_ner_tags,
        )

    def get_document_by_name(self, document_name: str) -> PetDocument:
        matching_rows = self._data[self._data["document name"] == document_name]
        document = matching_rows.iloc[0]
        converted_ner_tags = []
        for ner_tag in document["ner_tags"]:
            converted_ner_tags.append(str_to_entity(ner_tag))
        return PetDocument(
            name=document["document name"],
            tokens=document["tokens"],
            ner_tags=converted_ner_tags,
        )
