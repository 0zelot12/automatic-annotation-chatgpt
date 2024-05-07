from utils.helper import get_recall, get_precision, get_f1_score


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
    assert get_precision(true_positives, total) == 0.1


def test_precision_zero():
    true_positives = 0
    total = 0
    assert get_precision(true_positives, total) == 0.0


def test_precision_one():
    true_positives = 10
    postives_total = 10
    assert get_precision(true_positives, postives_total) == 1.0


def test_f1_score():
    assert get_f1_score(0.3, 0.6) == 0.4


def test_f1_score_zero():
    assert get_f1_score(1.0, 0) == 0.0
