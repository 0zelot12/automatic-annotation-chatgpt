from utils.helper import get_recall, get_precision, get_f1_score


def test_recall():
    ok = 10
    gold = 100
    assert get_recall(ok, gold) == 0.1


def test_recall_zero():
    ok = 0
    gold = 0
    assert get_recall(ok, gold) == 0.0


def test_recall_one():
    ok = 10
    gold = 10
    assert get_recall(ok, gold) == 1.0


def test_precision():
    ok = 10
    pred = 100
    assert get_precision(ok, pred) == 0.1


def test_precision_zero():
    ok = 0
    pred = 0
    assert get_precision(ok, pred) == 0.0


def test_precision_one():
    ok = 10
    pred = 10
    assert get_precision(ok, pred) == 1.0


def test_f1_score():
    assert get_f1_score(0.3, 0.6) == 0.4


def test_f1_score_zero():
    assert get_f1_score(1.0, 0) == 0.0
