import pytest
import random

#Перезапуск автотеста
PLATFORM = 'Windows'

@pytest.mark.flaky(reruns=3, reruns_delay=3)
def test_run():
    assert random.choice([True, False])

@pytest.mark.flaky(reruns=3, reruns_delay=3)
class TestReruns:
    def test_run1(self):
        assert random.choice([True, False])
    def test_run2(self):
        assert random.choice([True, False])

@pytest.mark.flaky(reruns=3, reruns_delay=3,condition=PLATFORM == 'Windows')
def test_conditions():
    assert random.choice([True, False])