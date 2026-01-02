import pytest
from playwright.sync_api import Page, Playwright


@pytest.fixture(scope="session")
def open_system(playwright: Playwright) -> Page:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto('http://release.goulash.tech/')

    page.locator('#LoginForm_username').fill('test')
    page.locator('#LoginForm_password').fill('1')
    page.locator('#login-submit').click()
    yield page
    browser.close()

@pytest.fixture(scope="session")
def create_promoevent(open_system, playwright: Playwright) -> Page:
    page = open_system
    page.goto('https://release.goulash.tech/promoevent/promoevent/create')
    page.locator('#Promoevent_name').fill('Promoevent_name')
    page.locator('#Promoevent_name_site').fill('Promoevent_name_site')
    page.locator('#Promoevent_is_active').click()
