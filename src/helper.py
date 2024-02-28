import matplotlib.pyplot as plt
import numpy as np

from annotation_result import AnnotationResult
from datetime import datetime
from entity import Entity
from entity_type import EntityType

from entity_tag import EntityTag
from visualization import convert_to_html


def generate_simple_bar_chart(values, categories, xLabel, yLabel, title):
    """
    Generate a simple bar chart using matplotlib.

    Parameters:
    - values (list): A list of numerical values representing the heights of the bars.
    - categories (list): A list of categories or labels corresponding to each bar.
    - xLabel (str): The label for the x-axis.
    - yLabel (str): The label for the y-axis.
    - title (str): The title of the bar chart.

    Returns:
    None

    This function creates a bar chart with the specified values, categories, and labels using matplotlib.
    It automatically adjusts the figure width based on the number of categories to improve readability.
    Each bar is labeled with its corresponding value, and the chart is displayed using plt.show().
    """

    # Set the width of the bars
    bar_width = 0.35

    # Set the positions of the bars on the x-axis
    bar_positions = np.arange(len(categories))

    # Calculate the dynamic figure width based on the number of categories
    figure_width = max(10, len(categories) * 0.8)

    # Set the figure size dynamically
    plt.figure(figsize=(figure_width, 6))  # Adjust the height as needed

    # Create the bar plot
    plt.bar(bar_positions, values, width=bar_width)

    # Add labels and title
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.xticks(bar_positions, categories)

    for i, value in enumerate(values):
        plt.text(bar_positions[i], value + 0.1, str(value), ha="center", va="bottom")

    # Display the plot
    plt.show()


def generate_horizontal_bar_chart(values, categories, xLabel, yLabel, title):
    """
    Generate a horizontal bar chart using matplotlib.

    Parameters:
    - values (list): A list of numerical values representing the lengths of the bars.
    - categories (list): A list of categories or labels corresponding to each bar.
    - xLabel (str): The label for the x-axis.
    - yLabel (str): The label for the y-axis.
    - title (str): The title of the horizontal bar chart.

    Returns:
    None

    This function creates a horizontal bar chart with the specified values, categories, and labels using matplotlib.
    It automatically adjusts the figure height based on the number of categories to improve readability.
    Each bar is labeled with its corresponding value, and the chart is displayed using plt.show().
    """

    # Set the height of the bars
    bar_height = 0.35

    # Set the positions of the bars on the y-axis
    bar_positions = np.arange(len(categories))

    # Calculate the dynamic figure height based on the number of categories
    figure_height = max(6, len(categories) * 0.8)

    # Set the figure size dynamically
    plt.figure(figsize=(10, figure_height))  # Adjust the width as needed

    # Create the horizontal bar plot
    plt.barh(bar_positions, values, height=bar_height)

    # Add labels and title
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.yticks(bar_positions, categories)

    for i, value in enumerate(values):
        plt.text(value + 0.1, bar_positions[i], str(value), ha="left", va="center")

    # Display the plot
    plt.show()


def parse_entities(response: list[str]) -> list[Entity]:
    entities = []
    current_entity = None
    offset = 0
    for r, i in zip(response, range(0, len(response))):
        if r == "<ACTOR>":
            offset += 1
            current_entity = Entity(
                type=EntityType.ACTOR, start_index=(i - offset) + 1, tokens=[]
            )
            continue
        if r == "</ACTOR>":
            offset += 1
            entities.append(current_entity)
            current_entity = None
            continue
        if r == "<ACTIVITY>":
            offset += 1
            current_entity = Entity(
                type=EntityType.ACTIVITY, start_index=(i - offset) + 1, tokens=[]
            )
            continue
        if r == "</ACTIVITY>":
            offset += 1
            entities.append(current_entity)
            current_entity = None
            continue
        if r == "<ACTIVITY_DATA>":
            offset += 1
            current_entity = Entity(
                type=EntityType.ACTIVITY_DATA, start_index=(i - offset) + 1, tokens=[]
            )
            continue
        if r == "</ACTIVITY_DATA>":
            offset += 1
            entities.append(current_entity)
            current_entity = None
            continue
        if current_entity:
            current_entity.tokens.append(r)
    return entities


def convert_to_template_example(
    tokens: list[str], ner_tags: list[EntityTag]
) -> list[str]:
    result = []
    for token, ner_tag, index in zip(tokens, ner_tags, range(len(tokens))):

        # ACTOR
        if ner_tag == EntityTag.B_ACTOR and ner_tags[index + 1] == EntityTag.I_ACTOR:
            result.append("<ACTOR>")
            result.append(f"{token}")
            continue
        if ner_tag == EntityTag.B_ACTOR and ner_tags[index + 1] != EntityTag.I_ACTOR:
            result.append("<ACTOR>")
            result.append(f"{token}")
            result.append("</ACTOR>")
            continue
        if ner_tag == EntityTag.I_ACTOR and ner_tags[index + 1] == EntityTag.I_ACTOR:
            result.append(f"{token}")
            continue
        if ner_tag == EntityTag.I_ACTOR and ner_tags[index + 1] != EntityTag.I_ACTOR:
            result.append(f"{token}")
            result.append("</ACTOR>")
            continue

        # ACTIVITY
        if (
            ner_tag == EntityTag.B_ACTIVITY
            and ner_tags[index + 1] == EntityTag.I_ACTIVITY
        ):
            result.append("<ACTIVITY>")
            result.append(f"{token}")
            continue
        if (
            ner_tag == EntityTag.B_ACTIVITY
            and ner_tags[index + 1] != EntityTag.I_ACTIVITY
        ):
            result.append("<ACTIVITY>")
            result.append(f"{token}")
            result.append("</ACTIVITY>")
            continue
        if (
            ner_tag == EntityTag.I_ACTIVITY
            and ner_tags[index + 1] == EntityTag.I_ACTIVITY
        ):
            result.append(f"{token}")
            continue
        if (
            ner_tag == EntityTag.I_ACTIVITY
            and ner_tags[index + 1] != EntityTag.I_ACTIVITY
        ):
            result.append(f"{token}")
            result.append("</ACTIVITY>")
            continue

        # ACTIVITY_DATA
        if (
            ner_tag == EntityTag.B_ACTIVITY_DATA
            and ner_tags[index + 1] == EntityTag.I_ACTIVITY_DATA
        ):
            result.append("<ACTIVITY_DATA>")
            result.append(f"{token}")
            continue
        if (
            ner_tag == EntityTag.B_ACTIVITY_DATA
            and ner_tags[index + 1] != EntityTag.I_ACTIVITY_DATA
        ):
            result.append("<ACTIVITY_DATA>")
            result.append(f"{token}")
            result.append("</ACTIVITY_DATA>")
            continue
        if (
            ner_tag == EntityTag.I_ACTIVITY_DATA
            and ner_tags[index + 1] == EntityTag.I_ACTIVITY_DATA
        ):
            result.append(f"{token}")
            continue
        if (
            ner_tag == EntityTag.I_ACTIVITY_DATA
            and ner_tags[index + 1] != EntityTag.I_ACTIVITY_DATA
        ):
            result.append(f"{token}")
            result.append("</ACTIVITY_DATA>")
            continue

        # NO_ENTITY
        if ner_tag == EntityTag.NO_ENTITY:
            result.append(f"{token}")
            continue

    return result


def calculate_metrics(
    model_annotations: list[Entity], reference_annotations: list[Entity]
):
    true_positives = 0
    false_negatives = 0
    for reference_annotation in reference_annotations:
        found_element = next(
            (
                o
                for o in model_annotations
                if o.start_index == reference_annotation.start_index
            ),
            None,
        )
        if found_element and reference_annotation.tokens == found_element.tokens:
            true_positives += 1
        else:
            false_negatives += 1

    precision = true_positives / len(model_annotations)
    recall = true_positives / len(reference_annotations)

    if precision + recall == 0:
        return [
            precision,
            recall,
            -1,
        ]  # TODO: Clarify what to return when precision + recall = 0

    f1_score = round(2 * precision * recall / (precision + recall), 2)

    return [precision, recall, f1_score]
