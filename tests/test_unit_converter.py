"""Tests for unit_converter.py: unit names must be case-insensitive."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from unit_converter import convert  # noqa: E402


def test_uppercase_data_units():
    assert convert(1, "MB", "KB") == 1024
    assert convert(1, "GB", "MB") == 1024
    assert convert(1024, "B", "KB") == 1


def test_lowercase_still_works():
    assert convert(1, "m", "cm") == 100
    assert convert(32, "f", "c") == pytest.approx(0)


def test_cross_group_still_rejected():
    with pytest.raises(ValueError):
        convert(1, "m", "c")
