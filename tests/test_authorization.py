import logging
import pytest
from playwright.sync_api import sync_playwright, expect #импорт плейврайта
@pytest.mark.login
def test_login():
    with sync_playwright() as playwright: #sync_playwright() — запускает Playwright, чтобы мы могли использовать его API для управления браузерами.
        # with — блок гарантирует, что браузер автоматически закроется после завершения работы (без необходимости вручную его закрывать).
        browser = playwright.chromium.launch(headless=False) #playwright.chromium.launch(headless=False) — запускаем браузер Chromium в видимом режиме (headless=False). Это означает, что мы увидим, как браузер открывается и работает.
        logging.info("Начало тестирования")
        page = browser.new_page()  # открываем новую страницу для работы. Playwright может работать с несколькими страницами.
        page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/login") #страница куда зайти
        disable = page.get_by_test_id('login-page-login-button')
        expect(disable).to_be_disabled() #проверяем,что до ввода данных кнопка не активна
        email = page.get_by_test_id('login-form-email-input').locator('input') #локатор куда заполнять
        email.fill('test@test.ru') # филл заполнил этимим данными
        password = page.locator('[data-testid="login-form-password-input"] input')
        password.fill('123')
        login = page.get_by_test_id('login-page-login-button')
        login.click()
        alert = page.locator('[data-testid="login-page-wrong-email-or-password-alert"]')
        expect(alert).to_be_visible() #проверка, что локатор видим/не видим visible - виден, hidden - не виден
        expect(alert).to_have_text('Wrong email or password') # проверка, что содерижтся текст который нам необходим
        reglink = page.get_by_test_id('login-page-registration-link')
        reglink.hover() #ховер это наведение мыши чтоб проверить активность



    # page.wait_for_timeout(2050) #ожидание 2с для демо проверки, что рил выполняются действия в браузере, в проектах не используется




    print('Тест пройден')