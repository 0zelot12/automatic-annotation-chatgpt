import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from collections import Counter
from pet_document import PetDocument

# Load data
df = pd.read_parquet("./assets/pet_dataset.parquet")

# Convert to objects
pet_documents = df.to_dict(orient="records")
records = []
# TODO: Refactor
for document in pet_documents:
    converted_document = PetDocument(
        name=document["document name"],
        tokens=document["tokens"],
        tokens_ids=document["tokens-IDs"],
        ner_tags=document["ner_tags"],
        sentence_ids=document["sentence-IDs"],
    )
    converted_document.relations["source_head_sentence_id"] = document[
        "relations.source-head-sentence-ID"
    ]
    converted_document.relations["source_head_word_id"] = document[
        "relations.source-head-word-ID"
    ]
    converted_document.relations["relation_type"] = document["relations.relation-type"]
    converted_document.relations["target_head_sentence_id"] = document[
        "relations.target-head-sentence-ID"
    ]
    converted_document.relations["target_head_word_id"] = document[
        "relations.target-head-word-ID"
    ]
    records.append(converted_document)

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

for string, count in ner_tags_counts.items():
    print(f"{string}: {count}")

# Calculate stats for relations
relations = []
for record in records:
    relations.extend(record.relations["relation_type"])

relations_counts = Counter(relations)

# Plot data
plot_categories = []
plot_values = []

for string, count in relations_counts.items():
    plot_categories.append(string)
    plot_values.append(count)

# Set the width of the bars
bar_width = 0.35

# Set the positions of the bars on the x-axis
bar_positions = np.arange(len(plot_categories))

# Create the bar plot
plt.bar(bar_positions, plot_values, width=bar_width)

# Add labels and title
plt.xlabel("Relationen")
plt.ylabel("Anzahl der Vorkommen im Datensatz")
plt.title("Verteilung von Relationen im PET-Datensatz")
plt.xticks(bar_positions, plot_categories)

for i, value in enumerate(plot_values):
    plt.text(bar_positions[i], value + 0.1, str(value), ha="center", va="bottom")

# Display the plot
plt.show()
