
from playwright.sync_api import expect, Page

def test_wrong_email_or_password(chromium_page: Page):
        chromium_page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/login")  # страница куда зайти
        disable = chromium_page.get_by_test_id('login-page-login-button')
        expect(disable).to_be_disabled()  # проверяем, что до ввода данных кнопка не активна
        email = chromium_page.get_by_test_id('login-form-email-input').locator('input')  # локатор куда заполнять
        email.fill('test@test.ru')  # Филом заполнил этими данными
        password = chromium_page.locator('[data-testid="login-form-password-input"] input')
        password.fill('123')
        login = chromium_page.get_by_test_id('login-page-login-button')
        login.click()

        alert = chromium_page.locator('[data-testid="login-page-wrong-email-or-password-alert"]')
        expect(alert).to_be_visible()  # проверка, что локатор видим/не видим visible - виден, hidden - не виден
        expect(alert).to_have_text('Wrong email or password')  # проверка, что содержится текст который нам необходим

        reglink = chromium_page.get_by_test_id('login-page-registration-link')
        reglink.hover()  # ховер это наведение мыши чтоб проверить активность
        chromium_page.wait_for_timeout(2050) # ожидание 2с для демо проверки, что рил выполняются действия в браузере, в проектах не используется


        print('✅Тест пройден✅')