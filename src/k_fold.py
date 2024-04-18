import logging
import traceback

from dotenv import load_dotenv
from annotation.annotation import annotate_relations
from pet.pet_dataset import PetDataset
from utils.helper import k_fold
from itertools import chain


dataset = PetDataset()

load_dotenv()

documents = dataset.get_all_documents()
# documents_names = [d.name for d in documents]

folds = k_fold(data=documents, k=5)

test_documents = folds[0]

training_documents = folds[1:]
training_documents = list(chain(*training_documents))

for test_document in test_documents:
    for i in range(5):
        print(f"Processing {test_document.name}")
        try:
            annotation_result = annotate_relations(
                document=test_document,
                model_name="gpt-3.5-turbo",
                training_documents=training_documents,
                temperature=0.7,
            )
            annotation_result.save_to_file("./out")
            print(f"Processing {test_document.name} completed ✅")
            break
        except Exception as e:
            print(f"Processing {test_document.name} failed ❌")
            logging.error("An exception occurred: %s", str(e))
            logging.error(traceback.format_exc())
