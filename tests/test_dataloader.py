import time
import random
import pytest
from dataloader import stats, lifetime

def test_stats():
    for button in ["Cards", "Transactions", "Verifications"]:
        time.sleep(random.randrange(0, 150, 30))
        assert bool(stats(button)) == True


def test_lifetime():
    time.sleep(random.randrange(0, 150, 30))
    assert bool(lifetime()) == True