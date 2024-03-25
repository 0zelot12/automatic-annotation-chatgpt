from pet_dataset import PetDataset

from dataclasses import dataclass, field

from relation_type import RelationType


@dataclass
class Relation:
    type: RelationType


def str_to_type(string_value: str) -> RelationType:
    for type in RelationType:
        if type.value == string_value:
            return type
    raise ValueError()


pet = PetDataset()

document = pet.get_document(10)

# print(document.relations)

relations = []
for relation in document.relations:
    relations.append(Relation(type=str_to_type(relation)))

print(relations)
print(document)
