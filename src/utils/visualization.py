import matplotlib.pyplot as plt
import numpy as np
import os
import json


def generate_simple_bar_chart(values, categories, xLabel, yLabel, title, show):
    bar_width = 0.35

    bar_positions = np.arange(len(categories))

    figure_width = max(10, len(categories) * 0.8)

    plt.figure(figsize=(figure_width, 6))

    plt.bar(bar_positions, values, width=bar_width)

    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.xticks(bar_positions, categories)

    for i, value in enumerate(values):
        plt.text(bar_positions[i], value + 0.1, str(value), ha="center", va="bottom")

    plt.savefig("sample_plot.png")

    if show:
        plt.show()


def generate_horizontal_bar_chart(
    values: list,
    categories: list[str],
    xLabel: str,
    yLabel: str,
    title: str,
    show: bool,
):
    bar_height = 0.35

    bar_positions = np.arange(len(categories))

    figure_height = max(6, len(categories) * 0.8)

    plt.figure(figsize=(10, figure_height))

    plt.barh(bar_positions, values, height=bar_height)

    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.xlim(0.0, 1.0)
    plt.yticks(bar_positions, categories)

    for i, value in enumerate(values):
        plt.text(value + 0.1, bar_positions[i], str(value), ha="left", va="center")

    plt.savefig(f"{title.lower()}.png", dpi=700)

    if show:
        plt.show()


def generate_scatterplot(
    x_values: list,
    y_values: list,
    x_label: str,
    y_label: str,
    show: bool,
    title: str,
):
    plt.figure(figsize=(8, 6))
    plt.scatter(x_values, y_values, color="blue", alpha=0.5)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xlim(0.0, 800)
    plt.ylim(0.0, 1.0)
    plt.grid(True)

    plt.savefig(f"{title.lower()}.png", dpi=700)

    if show:
        plt.show()


def generate_plots(data_path: str):
    data = []
    for filename in os.listdir(data_path):
        if filename.endswith(".json"):
            filepath = os.path.join(data_path, filename)
            with open(filepath, "r") as file:
                json_data = json.load(file)
                data.append(json_data)

    f1_scores = [d["metrics"]["overall_metrics"]["f1_score"] for d in data]

    f1_scores_entity = [
        d["metrics"]["entity_metrics"]["overall"]["f1_score"] for d in data
    ]

    f1_scores_relation = [
        d["metrics"]["relation_metrics"]["overall"]["f1_score"] for d in data
    ]

    mean_f1_score = np.mean(f1_scores)
    mean_f1_score_entity = np.mean(f1_scores_entity)
    mean_f1_score_relation = np.mean(f1_scores_relation)

    print(f"Overall {mean_f1_score}")
    print(f"Entity: {mean_f1_score_entity}")
    print(f"Relation {mean_f1_score_relation}")

    entity_keys = [
        "actor",
        "activity",
        "activity_data",
        "and_gateway",
        "xor_gateway",
        "condition_specification",
    ]

    relation_keys = [
        "actor_performer",
        "actor_recipient",
        "same_gateway",
        "flow",
        "uses",
    ]

    mean_f1_scores_entity = {}
    for entity_key in entity_keys:
        mean_f1_scores_entity[entity_key] = np.round(
            np.mean(
                [d["metrics"]["entity_metrics"][entity_key]["f1_score"] for d in data]
            ),
            2,
        )

    mean_f1_scores_relations = {}
    for relation_key in relation_keys:
        mean_f1_scores_relations[relation_key] = np.round(
            np.mean(
                [
                    d["metrics"]["relation_metrics"][relation_key]["f1_score"]
                    for d in data
                ]
            ),
            2,
        )

    generate_horizontal_bar_chart(
        values=list(mean_f1_scores_entity.values()),
        categories=entity_keys,
        title="F1-Scores and Entity Types",
        xLabel="F1-Score",
        yLabel="Entity Type",
        show=False,
    )

    generate_horizontal_bar_chart(
        values=list(mean_f1_scores_relations.values()),
        categories=relation_keys,
        title="F1-Scores and Relation Types",
        xLabel="F1-Score",
        yLabel="Relation Type",
        show=False,
    )

    lengths = [d["document_length"] for d in data]

    generate_scatterplot(
        x_values=lengths,
        y_values=f1_scores,
        title="Length and F1-Score",
        x_label="Length (#Tokens)",
        y_label="F1-Score",
        show=False,
    )
