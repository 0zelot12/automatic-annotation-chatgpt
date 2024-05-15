from relation.relation import parse_relations

test_relation_strings = [
    "ACTIVITY,$1,$1,ACTOR_PERFORMER,ACTOR,$0,$0",
    "ACTIVITY,$1,$1,FLOW,ACTIVITY,$4,$5",
]

test_tokens = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]


def test_parse_relations():
    relations, errors = parse_relations(
        relation_strings=test_relation_strings, tokens=test_tokens
    )
    assert errors == []
    for relation, test_relation in zip(relations, test_relation_strings):
        assert str(relation).replace("\n", "") == test_relation
