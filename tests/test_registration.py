import pytest
from playwright.sync_api import sync_playwright
@pytest.mark.registration
@pytest.mark.regression
def test_succesful_registration():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto('https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration')
        email = page.get_by_test_id('registration-form-email-input').locator('input')
        email.fill('timowka@mail.ru')
        username = page.get_by_test_id('registration-form-username-input').locator('input')
        username.fill('teswt1')
        password = page.get_by_test_id('registration-form-password-input').locator('input')
        password.fill('123123')
        reg = page.get_by_test_id('registration-page-registration-button')
        reg.click()

        context.storage_state(path='browser-state.json')

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(storage_state='browser-state.json')
        page = context.new_page()
        page.goto('https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/login')

        # page.wait_for_timeout(3008)
        print('Succesful registration')
