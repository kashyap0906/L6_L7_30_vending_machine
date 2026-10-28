"""Tests focused on executing every line of vending_machine.py."""
import pytest
from vending_machine import select_item, make_change, purchase


def test_select_item_statuses():
    assert select_item("water", {}, 100) == "invalid"
    assert select_item("cola", {"cola": 0}, 200) == "sold_out"
    assert select_item("cola", {"cola": 2}, 100) == "insufficient"
    assert select_item("cola", {"cola": 2}, 150) == "ok"


def test_make_change_zero_and_coins():
    assert make_change(0) == []
    assert make_change(190) == [100, 50, 25, 10, 5]


def test_make_change_negative_amount():
    with pytest.raises(ValueError, match="negative amount"):
        make_change(-1)


def test_make_change_impossible_amount():
    assert make_change(3) is None


def test_purchase_invalid_sold_out_and_insufficient():
    assert purchase("water", {}, 200) == ("invalid", [])
    assert purchase("cola", {"cola": 0}, 200) == ("sold_out", [])
    assert purchase("cola", {"cola": 1}, 100) == ("insufficient", [])


def test_purchase_with_no_exact_change_does_not_decrement_stock():
    stock = {"candy": 2}
    assert purchase("candy", stock, 76) == ("no_exact_change", [])
    assert stock["candy"] == 2


def test_purchase_dispenses_and_decrements_stock():
    stock = {"chips": 2}
    assert purchase("chips", stock, 150) == ("dispensed", [50])
    assert stock["chips"] == 1
