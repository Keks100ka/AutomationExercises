import re
import time
import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.auth_page import AuthPage, AccountInfoPage
from pages.contact_page import ContactPage
from pages.test_cases_page import TCasesPage


# ---------- TC1 ----------
def test_tc1_register_user(page: Page):
    """TC1: Регистрация нового пользователя + удаление аккаунта."""
    home = HomePage(page).open()
    home.expect_title("Automation Exercise")
    home.go_to_signup_login()

    auth = AuthPage(page)
    auth.expect_visible(auth.new_user_signup_title)

    email = f"tc1_{int(time.time())}@test.com"
    auth.start_signup("TC1 User", email)

    info = AccountInfoPage(page)
    info.expect_visible(info.title)
    info.fill_form("Pass123", "TC1", "User").submit()

    info.expect_visible(info.account_created_msg)
    info.click_continue()

    home.expect_visible(home.logged_in_as)
    home.delete_account()
    info.expect_visible(info.account_deleted_msg)


# ---------- TC2 ----------
def test_tc2_login_correct(page: Page, test_user):
    """TC2: Вход с валидными данными."""
    home = HomePage(page).open()
    home.go_to_signup_login()

    auth = AuthPage(page)
    auth.expect_visible(auth.login_title)
    auth.login(test_user["email"], test_user["password"])

    expect(page.get_by_text(f"Logged in as {test_user['name']}")).to_be_visible()


# ---------- TC3 ----------
def test_tc3_login_incorrect(page: Page):
    """TC3: Вход с невалидными данными."""
    home = HomePage(page).open()
    home.go_to_signup_login()

    auth = AuthPage(page)
    auth.expect_visible(auth.login_title)
    auth.login("wr@example.com", "wrpass")

    auth.expect_visible(auth.login_error, timeout=15000)


# ---------- TC4 ----------
def test_tc4_logout(page: Page, test_user):
    """TC4: Выход из системы после входа."""
    home = HomePage(page).open()
    home.go_to_signup_login()

    auth = AuthPage(page)
    auth.login(test_user["email"], test_user["password"])
    expect(page.get_by_text("Logged in as")).to_be_visible()

    home.logout()
    auth.expect_visible(auth.login_title)
    home.expect_url(".*login")


# ---------- TC5 ----------
def test_tc5_register_existing_email(page: Page, test_user):
    """TC5: Регистрация с уже существующим email."""
    home = HomePage(page).open()
    home.go_to_signup_login()

    auth = AuthPage(page)
    auth.expect_visible(auth.new_user_signup_title)
    auth.start_signup("Duplicate", test_user["email"])

    auth.expect_visible(auth.email_exists_error, timeout=15000)


# ---------- TC6 ----------
def test_tc6_contact_us(page: Page, tmp_path):
    """TC6: Отправка формы Contact Us с файлом."""
    home = HomePage(page).open()
    home.go_to_contact_us()

    contact = ContactPage(page)
    contact.expect_visible(contact.get_in_touch_title)

    file_path = tmp_path / "test.txt"
    file_path.write_text("test content")

    contact.submit_form(
        "Test User", "contact@test.com", "Test Subject",
        "This is a test message.", str(file_path),
    )

    contact.expect_visible(contact.success_msg, timeout=15000)
    contact.expect_text(contact.success_msg,
                        "Success! Your details have been submitted successfully.")

    contact.click_home()
    home.expect_title("Automation Exercise")


# ---------- TC7 ----------
def test_tc7_test_cases_page(page: Page):
    """TC7: Переход на страницу Test Cases."""
    home = HomePage(page).open()
    home.go_to_test_cases()

    tc_page = TCasesPage(page)
    home.expect_url(".*test_cases")
    tc_page.expect_title_contains("Test Cases")


