class PetDocument:
    """Class representing one document in the PET dataset."""

    # Maybe use dataclass here?

    def __init__(self, name, tokens, tokens_ids, ner_tags, sentence_ids, relations):
        self.name = name
        self.tokens = tokens
        self.tokens_ids = tokens_ids
        self.ner_tags = ner_tags
        self.sentence_ids = sentence_ids
        self.relations = relations
