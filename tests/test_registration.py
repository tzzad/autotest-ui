import pytest
from playwright.sync_api import Page, expect

@pytest.mark.registration
@pytest.mark.regression
def test_succesful_registration(chromium_page: Page):
        chromium_page.goto('https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration')

        chromium_page.get_by_test_id('registration-form-email-input').locator('input').fill('timowka@mail.ru')

        chromium_page.get_by_test_id('registration-form-username-input').locator('input').fill('teswt1')

        chromium_page.get_by_test_id('registration-form-password-input').locator('input').fill('123123')

        chromium_page.get_by_test_id('registration-page-registration-button').click()

        dashboard_title = chromium_page.get_by_test_id('dashboard-toolbar-title-text')
        expect(dashboard_title).to_be_visible()
        opcode


