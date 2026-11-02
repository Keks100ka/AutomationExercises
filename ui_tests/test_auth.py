import re
from playwright.sync_api import Page, expect
from pages.auth_page import AuthPage

def test_tc1_register_user(page: Page):

    """TC1: Зарегистрировать нового пользователя, проверить создание и удаление аккаунта"""
    page.goto("https://automationexercise.com/")
    expect(page).to_have_title(re.compile("Automation Exercise"))

    page.get_by_role("link", name="Signup / Login").click()
    expect(page.get_by_text("New User Signup!")).to_be_visible()

    # Уникальный email
    import time
    email = f"tc1_{int(time.time())}@test.com"
    page.locator("[data-qa='signup-name']").fill("TC1 User")
    page.locator("[data-qa='signup-email']").fill(email)
    page.locator("[data-qa='signup-button']").click()

    # Заполнение формы
    expect(page.get_by_text("ENTER ACCOUNT INFORMATION")).to_be_visible()
    page.locator("#id_gender1").check()
    page.locator("#password").fill("Pass123")
    page.locator("#days").select_option("10")
    page.locator("#months").select_option("5")
    page.locator("#years").select_option("1990")
    page.locator("#newsletter").check()
    page.locator("#optin").check()
    page.locator("#first_name").fill("TC1")
    page.locator("#last_name").fill("User")
    page.locator("#company").fill("TestCo")
    page.locator("#address1").fill("123 St")
    page.locator("#address2").fill("Apt 1")
    page.locator("#country").select_option("United States")
    page.locator("#state").fill("CA")
    page.locator("#city").fill("LA")
    page.locator("#zipcode").fill("12345")
    page.locator("#mobile_number").fill("1234567890")
    page.get_by_role("button", name="Create Account").click()

    expect(page.get_by_text("ACCOUNT CREATED!")).to_be_visible()
    page.get_by_role("link", name="Continue").click()
    expect(page.get_by_text("Logged in as")).to_be_visible()

    # Удаление аккаунта
    page.get_by_role("link", name="Delete Account").click()
    expect(page.get_by_text("ACCOUNT DELETED!")).to_be_visible()


def test_tc2_login_correct(page: Page, test_user):

    """TC2: Вход с правильными email и паролем"""
    page.goto("https://automationexercise.com/")
    page.get_by_role("link", name="Signup / Login").click()
    expect(page.get_by_text("Login to your account")).to_be_visible()

    page.locator("[data-qa='login-email']").fill(test_user["email"])
    page.locator("[data-qa='login-password']").fill(test_user["password"])
    page.locator("[data-qa='login-button']").click()

    expect(page.get_by_text(f"Logged in as {test_user['name']}")).to_be_visible()


def test_tc3_login_incorrect(page: Page):

    """TC3: Вход с неправильными email и паролем, проверить сообщение об ошибке"""
    page.goto("https://automationexercise.com/")
    page.get_by_role("link", name="Signup / Login").click()
    expect(page.get_by_text("Login to your account")).to_be_visible()

    page.locator("[data-qa='login-email']").fill("wrong@example.com")
    page.locator("[data-qa='login-password']").fill("wrongpass")
    page.locator("[data-qa='login-button']").click()

    expect(page.get_by_text("Your email or password is incorrect!")).to_be_visible()


def test_tc4_logout(page: Page, test_user):

    """TC4: После входа выполнить выход и проверить возврат на страницу входа"""
    page.goto("https://automationexercise.com/")
    page.get_by_role("link", name="Signup / Login").click()

    page.locator("[data-qa='login-email']").fill(test_user["email"])
    page.locator("[data-qa='login-password']").fill(test_user["password"])
    page.locator("[data-qa='login-button']").click()
    expect(page.get_by_text("Logged in as")).to_be_visible()

    page.get_by_role("link", name="Logout").click()
    expect(page).to_have_url(re.compile(".*login"))
    expect(page.get_by_text("Login to your account")).to_be_visible()


def test_tc5_register_existing_email(page: Page, test_user):

    """TC5: Регистрация с уже зарегистрированным email"""
    page.goto("https://automationexercise.com/")
    page.get_by_role("link", name="Signup / Login").click()
    expect(page.get_by_text("New User Signup!")).to_be_visible()

    page.locator("[data-qa='signup-name']").fill("Duplicate")
    page.locator("[data-qa='signup-email']").fill(test_user["email"])  # Существующий email
    page.locator("[data-qa='signup-button']").click()

    expect(page.get_by_text("Email Address already exist!")).to_be_visible()


def test_tc6_contact_us(page: Page, tmp_path):

    """TC6: Отправка формы обратной связи (включая загрузку файла)"""
    page.goto("https://automationexercise.com/")
    page.get_by_role("link", name="Contact us").click()
    expect(page.get_by_text("GET IN TOUCH")).to_be_visible()

    page.locator("[data-qa='name']").fill("Test User")
    page.locator("[data-qa='email']").fill("contact@test.com")
    page.locator("[data-qa='subject']").fill("Test Subject")
    page.locator("[data-qa='message']").fill("This is a test message.")

    # Загрузка файла
    file_path = tmp_path / "test.txt"
    file_path.write_text("test content")
    page.locator("input[name='upload_file']").set_input_files(str(file_path))

    # Обработка диалогового окна
    page.once("dialog", lambda dialog: dialog.accept())
    page.locator("[data-qa='submit-button']").click()

    expect(page.get_by_text("Success! Your details have been submitted successfully.")).to_be_visible()
    page.get_by_role("link", name="Home").click()
    expect(page).to_have_title(re.compile("Automation Exercise"))


def test_tc7_test_cases_page(page: Page):

    """TC7: Проверка перехода на страницу тест-кейсов"""
    page.goto("https://automationexercise.com/")
    page.get_by_role("link", name="Test Cases").click()
    expect(page).to_have_url(re.compile(".*test_cases"))
    # Проверка наличия заголовка страницы
    expect(page.locator("h2.title")).to_contain_text("Test Cases")


def test_tc8_all_products_detail(page: Page):

    """TC8: Просмотр списка продуктов и деталей первого продукта"""
    page.goto("https://automationexercise.com/")
    page.get_by_role("link", name="Products").click()
    expect(page).to_have_url(re.compile(".*products"))
    expect(page.get_by_text("ALL PRODUCTS")).to_be_visible()

    # Просмотр первого продукта
    page.locator(".choose .nav-link").first.click()
    expect(page.get_by_text("Blue Top")).to_be_visible()
    expect(page.locator(".product-information")).to_contain_text("Rs. 500")
    expect(page.locator(".product-information")).to_contain_text("Availability")
    expect(page.locator(".product-information")).to_contain_text("Condition")
    expect(page.locator(".product-information")).to_contain_text("Brand")


def test_tc9_search_product(page: Page):

    """TC9: Поиск продукта и проверка результатов"""
    page.goto("https://automationexercise.com/")
    page.get_by_role("link", name="Products").click()
    expect(page.get_by_text("ALL PRODUCTS")).to_be_visible()

    page.locator("#search_product").fill("Top")
    page.locator("#submit_search").click()
    expect(page.get_by_text("SEARCHED PRODUCTS")).to_be_visible()
    # Проверка наличия результатов поиска
    expect(page.locator(".product-image-wrapper").first).to_be_visible()
