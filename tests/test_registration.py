import pytest
from playwright.sync_api import Page, expect
from pages.dashboard_page import DashboardPage
from pages.registration_page import RegistrationPage

@pytest.mark.regression
@pytest.mark.parametrize('email,username,password', [
        ('user.name@gmail.com','user', 'password'),
])
def test_succesful_registration(dashboard_page: DashboardPage, registration_page: RegistrationPage, email: str, username: str, password: str):
        registration_page.visit('https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration')
        registration_page.fill_registration_form(email=email, username=username, password=password)
        registration_page.click_registration_button()

        dashboard_page.check_visible_dashboard_title()

