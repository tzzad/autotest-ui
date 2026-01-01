import pytest
@pytest.mark.xfail()

def test_with_bug():
    assert 1 == 2

@pytest.mark.xfail()
def test_with_lag():
    ...