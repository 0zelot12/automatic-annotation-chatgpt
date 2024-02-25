import matplotlib.pyplot as plt
import numpy as np

from annotation_result import AnnotationResult
from datetime import datetime

from entity import Entity
from pet_dataset import PetDataset
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


def generate_html(title: str, tokens: list[str], ner_tags: list[str]) -> None:
    # TODO: Maybe split this method and only generate the HTML string while make saving to file a generic method
    with open("../assets/template.html", "r") as file:
        html_template = file.read()
        content = ""
        for token, ner_tag in zip(tokens, ner_tags):
            if ner_tag == "O":
                content += f"{token} "
            else:
                content += f"<span class='{ner_tag}'>{token}</span> "

        result_string = html_template.replace("<!-- CONTENT  -->", content)
        result_string = result_string.replace("<!-- TITLE -->", title)

        with open(f"../out/{title}.html", "w") as file:
            file.write(result_string)


# TODO: Refactor
def save_annotation_result(
    annotation_result: AnnotationResult,
) -> None:
    with open("./assets/result-template.html", "r", encoding="utf-8") as file:
        file_content = file.read()
        file_content = (
            file_content.replace(
                "<!-- RESULT -->",
                convert_to_html(annotation_result.annotated_tokens),
            )
            .replace(
                "<!-- REFERENCE -->",
                convert_to_html(annotation_result.reference_annotated_tokens),
            )
            .replace(
                "<!-- RECOGNIZED_ACTOR -->", str(annotation_result.recognized_actor)
            )
            .replace("<!-- EXPECTED_ACTOR -->", str(annotation_result.expected_actor))
            .replace(
                "<!-- RECOGNIZED_ACTVITIY -->",
                str(annotation_result.recognized_activity),
            )
            .replace(
                "<!-- EXPECTED_ACTVITIY -->",
                str(annotation_result.expected_activity),
            )
            .replace(
                "<!-- RECOGNIZED_ACTIVITY_DATA -->",
                str(annotation_result.recognized_activity_data),
            )
            .replace(
                "<!-- EXPECTED_ACTIVITY_DATA -->",
                str(annotation_result.expected_activity_data),
            )
            .replace("<!-- PRECISION -->", str(annotation_result.get_precision()))
            .replace("<!-- RECALL -->", str(annotation_result.get_recall()))
            .replace("<!-- F1_SCORE -->", str(annotation_result.get_f1_score()))
            .replace("<!-- DOCUMENT_NAME -->", annotation_result.document_name)
            .replace("<!-- INPUT_LENGTH -->", str(annotation_result.input_length))
            .replace("<!-- ERRORS -->", str(annotation_result.incorrect_entities))
        )
    with open(
        f"./out/{annotation_result.document_name}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.html",
        "w",
    ) as file:
        file.write(file_content)


def process_model_reponse(response: list[str]) -> list[Entity]:
    entities = []
    current_entity = None
    offset = 0
    for r, i in zip(response, range(0, len(response))):
        if r == "<ACTOR>":
            offset += 1
            current_entity = {
                "type": "ACTOR",
                "tokens": [],
                "start_index": (i - offset) + 1,
            }
            continue
        if r == "</ACTOR>":
            offset += 1
            entities.append(current_entity)
            current_entity = None
            continue
        if r == "<ACTIVITY>":
            offset += 1
            current_entity = {
                "type": "ACTIVITY",
                "tokens": [],
                "start_index": (i - offset) + 1,
            }
            continue
        if r == "</ACTIVITY>":
            offset += 1
            entities.append(current_entity)
            current_entity = None
            continue
        if r == "<ACTIVITY_DATA>":
            offset += 1
            current_entity = {
                "type": "ACTIVITY_DATA",
                "tokens": [],
                "start_index": (i - offset) + 1,
            }
            continue
        if r == "</ACTIVITY_DATA>":
            offset += 1
            entities.append(current_entity)
            current_entity = None
            continue
        if current_entity:
            current_entity["tokens"].append(r)
    return entities


def convert_to_template_example(tokens: list[str], ner_tags: list[Entity]) -> list[str]:
    result = []
    for token, ner_tag, index in zip(tokens, ner_tags, range(len(tokens))):

        # ACTOR
        if ner_tag == Entity.B_ACTOR and ner_tags[index + 1] == Entity.I_ACTOR:
            result.append(f"<ACTOR>")
            result.append(f"{token}")
            continue
        if ner_tag == Entity.B_ACTOR and ner_tags[index + 1] != Entity.I_ACTOR:
            result.append(f"<ACTOR>")
            result.append(f"{token}")
            result.append(f"</ACTOR>")
            continue
        if ner_tag == Entity.I_ACTOR and ner_tags[index + 1] == Entity.I_ACTOR:
            result.append(f"{token}")
            continue
        if ner_tag == Entity.I_ACTOR and ner_tags[index + 1] != Entity.I_ACTOR:
            result.append(f"{token}")
            result.append(f"</ACTOR>")
            continue

        # ACTIVITY
        if ner_tag == Entity.B_ACTIVITY and ner_tags[index + 1] == Entity.I_ACTIVITY:
            result.append(f"<ACTIVITY>")
            result.append(f"{token}")
            continue
        if ner_tag == Entity.B_ACTIVITY and ner_tags[index + 1] != Entity.I_ACTIVITY:
            result.append(f"<ACTIVITY>")
            result.append(f"{token}")
            result.append(f"</ACTIVITY>")
            continue
        if ner_tag == Entity.I_ACTIVITY and ner_tags[index + 1] == Entity.I_ACTIVITY:
            result.append(f"{token}")
            continue
        if ner_tag == Entity.I_ACTIVITY and ner_tags[index + 1] != Entity.I_ACTIVITY:
            result.append(f"{token}")
            result.append(f"</ACTIVITY>")
            continue

        # ACTIVITY_DATA
        if (
            ner_tag == Entity.B_ACTIVITY_DATA
            and ner_tags[index + 1] == Entity.I_ACTIVITY_DATA
        ):
            result.append(f"<ACTIVITY_DATA>")
            result.append(f"{token}")
            continue
        if (
            ner_tag == Entity.B_ACTIVITY_DATA
            and ner_tags[index + 1] != Entity.I_ACTIVITY_DATA
        ):
            result.append(f"<ACTIVITY_DATA>")
            result.append(f"{token}")
            result.append(f"</ACTIVITY_DATA>")
            continue
        if (
            ner_tag == Entity.I_ACTIVITY_DATA
            and ner_tags[index + 1] == Entity.I_ACTIVITY_DATA
        ):
            result.append(f"{token}")
            continue
        if (
            ner_tag == Entity.I_ACTIVITY_DATA
            and ner_tags[index + 1] != Entity.I_ACTIVITY_DATA
        ):
            result.append(f"{token}")
            result.append(f"</ACTIVITY_DATA>")
            continue

        # NO_ENTITY
        if ner_tag == Entity.NO_ENTITY:
            result.append(f"{token}")
            continue

    return result


def evaluate_model_response(model_annotations, reference_annotations):
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    for reference_annotation in reference_annotations:
        found_element = next(
            (
                o
                for o in model_annotations
                if o["start_index"] == reference_annotation["start_index"]
            ),
            None,
        )
        if found_element:
            print(reference_annotation)
            print(found_element)
