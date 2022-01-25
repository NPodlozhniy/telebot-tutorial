import pytest
from dataloader import stats

def test_stats():
    assert bool(stats()) == True