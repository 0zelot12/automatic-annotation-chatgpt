from datetime import datetime

import logging
import traceback
import os

import numpy as np

from itertools import chain

from dotenv import load_dotenv

from annotation.annotation import annotate_relations_and_entities

from pet.pet_dataset import PetDataset

from utils.helper import k_fold

load_dotenv()

dataset = PetDataset()
documents = dataset.get_all_documents()

np.random.seed(42)

folds = k_fold(data=documents, k=5)

folder_path = f"./out/cross-validation-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    for i in range(5):
        os.makedirs(f"./{folder_path}/fold-{i}")

for k in range(5):
    training_folds = []
    test_fold = []
    for fold, index in zip(folds, range(0, len(folds))):
        if index == k:
            test_fold = folds[k]
        else:
            training_folds.append(fold)
    training_documents = list(chain(*training_folds))
    test_documents = test_fold
    for test_document in test_documents:
        np.random.shuffle(training_documents)
        for i in range(5):
            print(f"Processing {test_document.name}")
            print(f"Test Documents: {[d.name for d in training_documents[0:3]]}")
            try:
                # annotation_result = annotate_relations_and_entities(
                #     document=test_document,
                #     model_name="gpt-3.5-turbo",
                #     training_documents=training_documents,
                #     temperature=0.7,
                # )
                # annotation_result.save_to_file("./out")
                print(f"Processing {test_document.name} completed ✅")
                break
            except Exception as e:
                print(f"Processing {test_document.name} failed ❌")
                logging.error("An exception occurred: %s", str(e))
                logging.error(traceback.format_exc())
