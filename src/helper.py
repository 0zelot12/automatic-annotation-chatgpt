import matplotlib.pyplot as plt
import numpy as np

from annotation_result import AnnotationResult
from datetime import datetime


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


def write_annotation_results_to_file(
    annotation_results: list[AnnotationResult],
) -> None:
    result_string = ""
    for annotation_result in annotation_results:
        result_string += f"""====================================
Document name: {annotation_result.document_name}

Input length: {annotation_result.input_length}

Expected O: {annotation_result.expected_o}
Correctly Identified O: {annotation_result.recognized_o} 

Expected Actor: {annotation_result.expected_actor}
Correctly Identified Actor: {annotation_result.recognized_actor} 

Expected Activity: {annotation_result.expected_activity}
Correctly Identified Activity: {annotation_result.recognized_activity} 

Expected Activity: {annotation_result.expected_activity_data}
Correctly Identified Activity: {annotation_result.recognized_activity_data}

Entities identified incorretly: {annotation_result.incorrect_entities}
====================================
    """
    with open(
        f"./out/annotation-result-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt",
        "w",
    ) as file:
        file.write(result_string)


def convert_tags(tags: list[str], entity: str) -> list[str]:
    filtered_tags = []
    for tag in tags:
        if tag == f"B-{entity}" or tag == f"I-{entity}":
            filtered_tags.append(entity)
        else:
            filtered_tags.append("O")
    return filtered_tags


def convert_result(annotations: list[str], entity: str) -> list[str]:
    converted_results = []
    for annotation in annotations:
        if annotation.startswith("<A>"):
            converted_results.append(entity)
        else:
            converted_results.append("O")
    return converted_results


def get_entity_type_count(tags: list[str], entity: str) -> int:
    count = 0
    for tag in tags:
        if tag == f"B-{entity}" or tag == f"I-{entity}":
            count += 1
    return count
