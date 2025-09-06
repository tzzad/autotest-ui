from playwright.sync_api import sync_playwright, expect
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/login')
    disable = page.get_by_test_id('login-page-login-button')
    expect(disable).to_be_disabled()
    email = page.get_by_test_id('login-form-email-input').locator('input')
    email.focus()
    for char in 'tzzelen@yandex.ru':
        page.keyboard.type(char, delay=100)  #имитация ввода по клавиатуре
    page.keyboard.press('ControlOrMeta+A', delay=100) #delay=задержка действия





    page.wait_for_timeout(1500)


    print('Successfully!')