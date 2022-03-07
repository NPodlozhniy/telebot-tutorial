import time
import random
import pytest
from dataloader import stats, lifetime

def test_stats():
    time.sleep(random.randrange(0, 210, 30))
    button = random.choice(["Cards", "Transactions", "Verifications"])
    assert bool(stats(button)) == True


def test_lifetime():
    time.sleep(random.randrange(0, 210, 30))
    assert bool(lifetime()) == True