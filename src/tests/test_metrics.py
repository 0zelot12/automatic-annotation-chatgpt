from utils.helper import get_recall, get_precision


def test_recall():
    true_positives = 10
    postives_total = 100
    assert get_recall(true_positives, postives_total) == 0.1


def test_recall_zero():
    true_positives = 0
    postives_total = 0
    assert get_recall(true_positives, postives_total) == 0.0


def test_recall_one():
    true_positives = 10
    postives_total = 10
    assert get_recall(true_positives, postives_total) == 1.0


def test_precision():
    true_positives = 10
    total = 100
    assert get_recall(true_positives, total) == 0.1


def test_precision_zero():
    true_positives = 0
    total = 0
    assert get_recall(true_positives, total) == 0.0


def test_precision_one():
    true_positives = 10
    postives_total = 10
    assert get_recall(true_positives, postives_total) == 1.0
