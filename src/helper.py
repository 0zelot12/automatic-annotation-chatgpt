import matplotlib.pyplot as plt
import numpy as np

from annotation_result import AnnotationResult
from datetime import datetime


def generate_simple_bar_chart(values, categories, xLabel, yLabel, title):
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


def generate_html(title, tokens, ner_tags):
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


def write_annotation_result_to_file(annotation_result):
    result_string = f"""====================================

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
    """
    with open(
        f"./out/annotation-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt",
        "w",
    ) as file:
        file.write(result_string)
