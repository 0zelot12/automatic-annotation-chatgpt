import matplotlib.pyplot as plt
import numpy as np
import os
import json

from helper import avg


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


def generate_scatterplot(path: str):
    data = []
    for filename in os.listdir(path):
        if filename.endswith(".json"):
            filepath = os.path.join(path, filename)
            with open(filepath, "r") as file:
                json_data = json.load(file)
                data.append(json_data)

    plot_data = []

    for d in data:
        plot_data.append(
            {
                "recall": d["metrics"]["recall"],
                "precision": d["metrics"]["precision"],
                "f1_score": d["metrics"]["f1_score"],
                "document_length": len(d["tokens"]),
            }
        )

    # Extract recall and precision values from the data
    recalls = [d["recall"] for d in plot_data]
    precisions = [d["precision"] for d in plot_data]
    f1_scores = [d["f1_score"] for d in plot_data]
    lengths = [d["document_length"] for d in plot_data]

    # # Create scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(lengths, f1_scores, color="blue", alpha=0.5)
    plt.title("Length and F1-Score")
    plt.xlabel("Length (#Tokens)")
    plt.ylabel("F1-Score")
    plt.xlim(0.0, 800)
    plt.ylim(0.0, 1.0)
    plt.grid(True)
    plt.show()


generate_scatterplot(
    path="/Users/andreaslauritz/Desktop/Testreihen/Zwei Beispiele + Kurze Defintionen/Annotationen_04_03_2024_Short_Examples_Few_Shot"
)
