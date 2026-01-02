import pytest
from playwright.sync_api import Page, expect

@pytest.mark.registration
@pytest.mark.regression
def test_succesful_registration(chromium_page: Page):
        chromium_page.goto('https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration')

        email = chromium_page.get_by_test_id('registration-form-email-input').locator('input')
        email.fill('timowka@mail.ru')

        username = chromium_page.get_by_test_id('registration-form-username-input').locator('input')
        username.fill('teswt1')

        password = chromium_page.get_by_test_id('registration-form-password-input').locator('input')
        password.fill('123123')

        reg = chromium_page.get_by_test_id('registration-page-registration-button')
        reg.click()

        dashboard_title = chromium_page.get_by_test_id('dashboard-toolbar-title-text')
        expect(dashboard_title).to_be_visible()



