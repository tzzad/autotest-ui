from playwright.sync_api import sync_playwright, expect
import logging
import pytest
# with sync_playwright() as playwright:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto('http://release.goulash.tech/')
#
#     page.locator('#LoginForm_username').fill('test')
#     page.locator('#LoginForm_password').fill('1')
#     page.locator('#login-submit').click
#     page.wait_for_timeout(5000)

# with sync_playwright() as playwright:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto('https://k8s-devtest1.goulash.tech/')
#     login = page.locator('#LoginForm_username')
#     login.fill('test')
#     password = page.locator('#LoginForm_password')
#     password.fill('1')
#     submit = page.locator('#login-submit')
#     submit.click()
#
#     context.storage_state(path='browser-state.json')

# with (sync_playwright() as playwright):
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context(storage_state='browser-state.json')
#     page = context.new_page()
#     page.goto('https://k8s-devtest1.goulash.tech/promoevent/promoevent/create')
#     page.wait_for_timeout(5000) # ждем загрузку страницы
#     page.locator('#Promoevent_name').fill("Promoevent_name")
#     page.locator('#Promoevent_name_site').fill("Promoevent_name_site")
#     page.locator('#Promoevent_is_active').click()
#     page.select_option('#Promoevent_usage', '1') # выбираем value из выпадающего списка
#     page.click('#promo')
#     #expect('Promoevent_code').not.toHaveValue(''); #разобраться как проверить что проле заполнено
#     page.click('#yt23')
#     page.wait_for_timeout(200)
#     page.select_option('condition-type', '2')
#     page.select_option('#PromoeventCondition_6956c8907adaa_order_trait', '9')
#     page.click('#yt25')
#     page.wait_for_timeout(200)
#     page.select_option('#PromoeventReward_6956c8ef182e7_type', '1')
#     page.click('#yt28')
#     page.wait_for_timeout(3000)
#     print('✅Тест завершен успешно')
