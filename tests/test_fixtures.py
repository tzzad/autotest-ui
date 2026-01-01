import pytest
import logging
from playwright.sync_api import sync_playwright

@pytest.fixture(autouse=True)
def send_analytics_data():
    ...

@pytest.fixture(scope="session")
def settings():
    ...

@pytest.fixture(scope="class")
def user():
    ...
@pytest.fixture(scope="function")
def browser():
    ...
