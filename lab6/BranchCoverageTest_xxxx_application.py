"""Tests explicitly exercising true/false decision branches in the module."""
import pytest
from vending_machine import select_item, make_change, purchase


def test_select_item_invalid_and_valid_item_branches():
    assert select_item("water", {}, 500) == "invalid"  # item not in PRICES: True
    assert select_item("cola", {"cola": 1}, 150) == "ok"  # item not in PRICES: False


def test_select_item_stock_zero_and_nonzero_branches():
    assert select_item("cola", {"cola": 0}, 150) == "sold_out"  # stock==0: True
    assert select_item("cola", {"cola": 1}, 150) == "ok"  # stock==0: False


def test_select_item_insufficient_and_sufficient_credit_branches():
    assert select_item("chips", {"chips": 1}, 99) == "insufficient"  # credit too low
    assert select_item("chips", {"chips": 1}, 100) == "ok"  # credit sufficient


def test_make_change_negative_and_nonnegative_branches():
    with pytest.raises(ValueError, match="negative amount"):
        make_change(-5)  # amount < 0: True
    assert make_change(0) == []  # amount < 0: False; amount > 0: False


def test_make_change_loop_true_and_false_and_exact_change():
    # Exercises the coin-append loop for all denominations and its exit branches.
    assert make_change(190) == [100, 50, 25, 10, 5]


def test_make_change_unmakeable_remainder_branch():
    assert make_change(3) is None  # amount > 0: True and no coin can be used


def test_purchase_non_ok_status_branch():
    assert purchase("water", {}, 200) == ("invalid", [])  # status != "ok": True


def test_purchase_change_is_none_branch():
    stock = {"candy": 1}
    assert purchase("candy", stock, 76) == ("no_exact_change", [])  # change is None
    assert stock["candy"] == 1


def test_purchase_change_is_available_branch():
    stock = {"chips": 2}
    assert purchase("chips", stock, 150) == ("dispensed", [50])  # change is not None
    assert stock["chips"] == 1
