import pandas as pd
from collections import Counter

from pet_document import PetDocument

# Load data
df = pd.read_parquet("./assets/pet_dataset.parquet")

# Convert to objects
pet_documents = df.to_dict(orient="records")
records = []
for document in pet_documents:
    records.append(
        PetDocument(
            name=document["document name"],
            tokens=document["tokens"],
            tokens_ids=document["tokens-IDs"],
            ner_tags=document["ner_tags"],
            sentence_ids=document["sentence-IDs"],
        )
    )

# Calculate stats for tokens
total_tokens = 0
for record in records:
    total_tokens += len(record.tokens)


avg_tokens = total_tokens / len(records)


def get_lengths(documents):
    result = []
    for document in documents:
        result.append(len(document.tokens))
    return result


min_tokens = min(get_lengths(records))
max_tokens = max(get_lengths(records))

# Calculate stats for ner-tags
ner_tags = []
for record in records:
    ner_tags.extend(record.ner_tags)

ner_tags_counts = Counter(ner_tags)

# for string, count in ner_tags_counts.items():
#     print(f"{string}: {count}")
