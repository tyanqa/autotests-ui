import time

from playwright.sync_api import expect, sync_playwright

# 1. Открываем страницу регистрации и заполняем форму
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration")

    email_input = page.get_by_test_id('registration-form-email-input').locator('input')
    email_input.fill(f'user.{int(time.time())}@gmail.com')

    username_input = page.get_by_test_id('registration-form-username-input').locator('input')
    username_input.fill('username')

    password_input = page.get_by_test_id('registration-form-password-input').locator('input')
    password_input.fill('password12345')

    registration_button = page.get_by_test_id('registration-page-registration-button')
    registration_button.click()

    # 2. Открывается страница "Dashboard". Сохраняем состояние браузера
    expect(page).to_have_url("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/dashboard")
    context.storage_state(path="browser-state.json")

    page.wait_for_timeout(5000)

# 3. Открываем страницу courses с использованием сохраненного контекста и проверяем элементы
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="browser-state.json")
    page = context.new_page()

    page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses")

    title = page.get_by_test_id('courses-list-toolbar-title-text')
    expect(title).to_have_text("Courses")

    empty_view_icon = page.get_by_test_id('courses-list-empty-view-icon')
    expect(empty_view_icon).to_be_visible()

    empty_view_title = page.get_by_test_id('courses-list-empty-view-title-text')
    expect(empty_view_title).to_have_text("There is no results")

    empty_view_description = page.get_by_test_id('courses-list-empty-view-description-text')
    expect(empty_view_description).to_have_text("Results from the load test pipeline will be displayed here")

    page.wait_for_timeout(5000)
