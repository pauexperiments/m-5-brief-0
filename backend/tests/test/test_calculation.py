import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from modules.calculation import calculate

@pytest.mark.parametrize("n,expected", [
    (0, 0),
    (1, 1),
    (2, 4),
    (-3, 9),
    (10, 100),
])
def test_calculate(n, expected):
    assert calculate(n) == expected
