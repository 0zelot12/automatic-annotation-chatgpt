import pandas as pd

from models.pet_document import PetDocument

# Load data
df = pd.read_parquet("./data/pet_dataset.parquet")

# Convert to objects
list_of_objects = df.to_dict(orient="records")

records = []

for o in list_of_objects:
    records.append(
        PetDocument(
            name=o["document name"],
            tokens=o["tokens"].tolist(),
            tokens_ids=o["tokens-IDs"].tolist(),
            ner_tags=o["ner_tags"].tolist(),
            sentence_ids=o["sentence-IDs"].tolist(),
            relations=o["relations"],
        )
    )
