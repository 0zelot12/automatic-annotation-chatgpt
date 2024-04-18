import numpy as np
import os
import json

import numpy as np
from scipy import stats

data_path = "C:\\Users\\alauritz\\Desktop\\one-shot"
data_path_test = "C:\\Users\\alauritz\\Desktop\\three-shot"

n = 45

################################################################################################################################

data = []
for filename in os.listdir(data_path):
    if filename.endswith(".json"):
        filepath = os.path.join(data_path, filename)
        with open(filepath, "r") as file:
            json_data = json.load(file)
            data.append(json_data)

f1_scores = [d["metrics"]["overall_metrics"]["f1_score"] for d in data]

mean_f1_score = np.mean(f1_scores)

standard_deviation_f1_score = np.std(f1_scores)

variance_f1_score = standard_deviation_f1_score * standard_deviation_f1_score

print(
    f"(Overall) Mean F1-Score: {mean_f1_score} - Standard Deviation: {np.std(f1_scores)}"
)

################################################################################################################################

data_test = []
for filename in os.listdir(data_path_test):
    if filename.endswith(".json"):
        filepath = os.path.join(data_path_test, filename)
        with open(filepath, "r") as file:
            json_data = json.load(file)
            data_test.append(json_data)

f1_scores_test = [d["metrics"]["overall_metrics"]["f1_score"] for d in data_test]

mean_f1_score_test = np.mean(f1_scores_test)

standard_deviation_f1_score_test = np.std(f1_scores_test)

variance_f1_score_test = (
    standard_deviation_f1_score_test * standard_deviation_f1_score_test
)

print(
    f"(Overall) Mean F1-Score: {mean_f1_score_test} - Standard Deviation: {np.std(f1_scores_test)}"
)

################################################################################################################################

# t_value = np.abs(
#     standard_deviation_f1_score - standard_deviation_f1_score_test
# ) / np.sqrt((variance_f1_score / n) + (variance_f1_score_test / n))

# print(t_value)


# print(stats.ttest_rel(f1_scores, f1_scores_test))

# Sample data
group1 = [4, 5, 6, 7, 8]
group2 = [2, 3, 4, 5, 6]


# Print the results
print(stats.ttest_rel(f1_scores, f1_scores_test))
