import pandas as pd

from pet_document import PetDocument

from entity_tag import str_to_entity


ORDERED_DOCUMENT_NAMES = [
    "doc-1.1",
    "doc-1.2",
    "doc-1.3",
    "doc-1.4",
    "doc-2.1",
    "doc-2.2",
    "doc-3.1",
    "doc-3.2",
    "doc-3.3",
    "doc-3.5",
    "doc-3.6",
    "doc-3.7",
    "doc-3.8",
    "doc-4.1",
    "doc-5.1",
    "doc-5.2",
    "doc-5.3",
    "doc-5.4",
    "doc-6.1",
    "doc-6.2",
    "doc-6.3",
    "doc-6.4",
    "doc-7.1",
    "doc-8.1",
    "doc-8.2",
    "doc-8.3",
    "doc-9.1",
    "doc-9.2",
    "doc-9.3",
    "doc-9.4",
    "doc-9.5",
    "doc-10.1",
    "doc-10.2",
    "doc-10.3",
    "doc-10.4",
    "doc-10.5",
    "doc-10.6",
    "doc-10.7",
    "doc-10.8",
    "doc-10.9",
    "doc-10.10",
    "doc-10.11",
    "doc-10.12",
    "doc-10.13",
    "doc-10.14",
]


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
            df = pd.read_parquet("./data/pet_dataset.parquet")
            # This doesn't work corretly!
            df["index"] = df["document name"].apply(foo)
            cls._data = df.sort_values(by="index")
        return cls._instance

    def get_data(self):
        return self._data

    def get_document(self, document_number: int) -> PetDocument:
        converted_ner_tags = []
        print(self._data.iloc[document_number])
        for ner_tag in self._data.iloc[document_number]["ner_tags"]:
            converted_ner_tags.append(str_to_entity(ner_tag))
        return PetDocument(
            name=self._data.iloc[document_number]["document name"],
            tokens=self._data.iloc[document_number]["tokens"],
            ner_tags=converted_ner_tags,
            relations=self._data.iloc[document_number]["relations"],
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
