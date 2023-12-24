import pandas as pd

from collections import Counter
from pet_document import PetDocument

df = pd.read_parquet("../assets/pet_dataset.parquet")

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

from helper import generate_horizontal_bar_chart

total_tokens = 0
for record in records:
    total_tokens += len(record.tokens)


def get_lengths(documents):
    result = []
    for document in documents:
        result.append(len(document.tokens))
    return result


min_tokens = min(get_lengths(records))
max_tokens = max(get_lengths(records))
avg_tokens = total_tokens / len(records)

generate_horizontal_bar_chart(
    values=[min_tokens, max_tokens, avg_tokens],
    categories=["Minimum", "Maximum", "Durchschnitt"],
    xLabel="Tokens",
    yLabel="",
    title="Anzahl an Tokens pro Dokument",
)

ner_tags = []
for record in records:
    ner_tags.extend(record.ner_tags)

ner_tags_counts = Counter(ner_tags)

plot_categories = []
plot_values = []

for string, count in ner_tags_counts.items():
    plot_categories.append(string)
    plot_values.append(count)

generate_horizontal_bar_chart(
    values=plot_values,
    categories=plot_categories,
    xLabel="ner-Tags",
    yLabel="Anzahl der Vorkommen im Datensatz",
    title="Verteilung von NER-Tags im PET-Datensatz",
)

filtered_ner_tags = []
plot_categories = []
plot_values = []

for item in ner_tags_counts.items():
    if not item[0].startswith("I"):
        filtered_ner_tags.append(item)

for tag, count in filtered_ner_tags:
    plot_categories.append(tag.replace("B-", ""))
    plot_values.append(count)

generate_horizontal_bar_chart(
    values=plot_values,
    categories=plot_categories,
    xLabel="Anzahl der Vorkommen im Datensatz",
    yLabel="ner-Tags ",
    title="Verteilung von NER-Tags im PET-Datensatz",
)

from helper import generate_simple_bar_chart

relations = []
for record in records:
    relations.extend(record.relations["relation_type"])

relations_counts = Counter(relations)

plot_categories = []
plot_values = []

for string, count in relations_counts.items():
    plot_categories.append(string)
    plot_values.append(count)

generate_simple_bar_chart(
    values=plot_values,
    categories=plot_categories,
    xLabel="Relationen",
    yLabel="Anzahl der Vorkommen im Datensatz",
    title="Verteilung von Relationen im PET-Datensatz",
)
