from datetime import datetime

import logging
import traceback
import os

import numpy as np

from dotenv import load_dotenv

from annotation.annotation import annotate_relations, get_failure_annotation

from pet.pet_dataset import PetDataset
from utils.helper import k_fold

load_dotenv()

dataset = PetDataset()
documents = dataset.get_all_documents()

np.random.seed(42)
np.random.shuffle(documents)

folds = k_fold(data=documents, k=5)

for j in range(5):
    folder_path = (
        f"./out/cross-validation-run-{j}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
    )
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for i in range(5):
        os.makedirs(f"./{folder_path}/{i}")
    print(f"⚠️ Run {j + 1} of {5} ⚠️")
    for k in range(5):
        print(f"\t ➡️ Fold {k + 1} of {5} ⬅️")
        test_documents = folds[k]
        training_documents = []
        for fold, index in zip(folds, range(0, len(folds))):
            if index == k:
                continue
            else:
                training_documents.extend(fold)
        np.random.shuffle(training_documents)
        for test_document in test_documents:
            print(f"\t\t Processing {test_document.name} ⏳")
            for i in range(0, 5):
                try:
                    annotation_result = annotate_relations(
                        document=test_document,
                        model_name="gpt-3.5-turbo",
                        training_documents=training_documents[0:2],
                        temperature=0.3,
                    )
                    annotation_result.save_to_file(f"{folder_path}/{k}")
                    print(f"\t\t Processing {test_document.name} completed ✅")
                    break
                except Exception as e:
                    print(f"\t\t Processing {test_document.name} failed ❌")
                    logging.error("An exception occurred: %s", str(e))
                    logging.error(traceback.format_exc())
                    if i == 4:
                        annotation_result = get_failure_annotation(
                            document=test_document,
                            model_name="gpt-3.5-turbo",
                            training_documents=[],
                            temperature=0.7,
                        )
                        annotation_result.save_to_file(f"{folder_path}/{k}")
