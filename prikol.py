from playwright.sync_api import sync_playwright, expect
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('http://127.0.0.1:5500/techo-stats.html', wait_until='load')
    login = page.locator('#username')
    login.fill('tzadmin')
    password = page.locator('#password')
    password.fill('1')
    button = page.locator('#btn_log')
    button.click()
    user_list = page.locator('#userListBtn')
    user_list.click()
    create_user = page.locator('#createUserBtn')
    create_user.click()
    new_user = page.locator('#newUserFIO')
    new_user.fill('Попов Антон Николаевич')
    user_phone = page.locator('#newUserPhone')
    user_phone.fill('89090104904')
    email = page.locator('#newUserEmail')
    email.fill('tzzelen@my.net')
    new_username = page.locator('#newUsername')
    new_username.fill('trest')
    new_password = page.locator('#newPassword')
    new_password.fill('1')
    page.select_option('#newUserRole')  # выбор локатора
    page.select_option('#newUserRole', 'reader')
    confirm = page.locator('#userFormSubmitBtn')
    confirm.click()
    alert = page.locator('#customAlertOkBtn')
    alert.click()
    close_btn = page.locator('#closeModalBtn')
    close_btn.click()
    create_state = page.get_by_role("button", name="Создать статью")
    create_state.click()
    articleTitle = page.locator('#articleTitle')
    articleTitle.fill('test')
    headerText = page.locator('#headerText')
    headerText.fill('test')
    write = page.locator('div.ck-editor__editable_inline')
    write.fill('test')
    submit = page.locator('button:has-text("Сохранить")')
    submit.click()















    # page.wait_for_timeout(3000)
    print('Успех')