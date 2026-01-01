from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://k8s-devtest1.goulash.tech/')
    login = page.locator('#LoginForm_username')
    login.fill('test')
    password = page.locator('#LoginForm_password')
    password.fill('1')
    submit = page.locator('#login-submit')
    submit.click()

    context.storage_state(path='browser-state.json')

with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(storage_state='browser-state.json')
        page = context.new_page()
        page.goto('https://k8s-devtest1.goulash.tech/promoevent/promoevent/create')

        page.wait_for_timeout(3000)
        print('✅Тест завершен успешно')