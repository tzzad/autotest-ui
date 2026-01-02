from symtable import Class
import pytest
from playwright.sync_api import Page, playwright, sync_playwright


@pytest.fixture(scope="session")
def open_system(playwright, Playwright) -> Page :
    browser = playwright.chromium.launch(headless=False)

    browser.goto('http://release.goulash.tech/')

    login_input = browser.locator('#LoginForm_username').fill('test')
    password_input = browser.locator('#LoginForm_password').fill('1')
    login_submit = browser.locator('#login-submit').click()
