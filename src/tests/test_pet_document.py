# import unittest

# from entity_tag import EntityTag
# from entity import Entity
# from entity_type import EntityType
# from pet_document import PetDocument


# class TestPetDocument(unittest.TestCase):

#     def setUp(self):
#         self.document = PetDocument(
#             name="Test Document",
#             tokens=[
#                 "A",
#                 "company",
#                 "sends",
#                 "a",
#                 "letter",
#                 "to",
#                 "the",
#                 "customer",
#                 ".",
#             ],
#             ner_tags=[
#                 EntityTag.B_ACTOR,
#                 EntityTag.I_ACTOR,
#                 EntityTag.B_ACTIVITY,
#                 EntityTag.B_ACTIVITY_DATA,
#                 EntityTag.I_ACTIVITY_DATA,
#                 EntityTag.NO_ENTITY,
#                 EntityTag.B_ACTOR,
#                 EntityTag.I_ACTOR,
#                 EntityTag.NO_ENTITY,
#             ],
#         )

#     def test_get_actors(self):
#         actors = self.document.get_actors()
#         expected_actors = [
#             Entity(type=EntityType.ACTOR, start_index=0, tokens=["A", "company"]),
#             Entity(type=EntityType.ACTOR, start_index=6, tokens=["the", "customer"]),
#         ]
#         self.assertEqual(actors, expected_actors)

#     def test_get_activities(self):
#         activities = self.document.get_activites()
#         expected_activity = Entity(
#             type=EntityType.ACTIVITY, start_index=2, tokens=["sends"]
#         )
#         self.assertEqual(activities, [expected_activity])

#     def test_get_activity_data(self):
#         activity_data = self.document.get_activity_data()
#         expected_activity_data = Entity(
#             type=EntityType.ACTIVITY_DATA, start_index=3, tokens=["a", "letter"]
#         )
#         self.assertEqual(activity_data, [expected_activity_data])

#     def test_get_entities(self):
#         entities = self.document.get_entities()
#         expected_entities = [
#             Entity(type=EntityType.ACTOR, start_index=0, tokens=["A", "company"]),
#             Entity(type=EntityType.ACTIVITY, start_index=2, tokens=["sends"]),
#             Entity(
#                 type=EntityType.ACTIVITY_DATA, start_index=3, tokens=["a", "letter"]
#             ),
#             Entity(type=EntityType.ACTOR, start_index=6, tokens=["the", "customer"]),
#         ]
#         self.assertEqual(entities, expected_entities)


# if __name__ == "__main__":
#     unittest.main()
