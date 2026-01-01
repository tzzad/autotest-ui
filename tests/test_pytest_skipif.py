import pytest
SystemVersion = "v1.34"

@pytest.mark.skipif(
    SystemVersion == "v1.340",
    reason="Версия не совпадает",
)
def test_pytest_version_as():
    ...


@pytest.mark.skipif(
    SystemVersion == "v1.34",
    reason="Версия не совпадает",
)
def test_pytest_version_as_al():
    ...
