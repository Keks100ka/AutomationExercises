from playwright.sync_api import Page
from pages.base_page import BasePage


class HomePage(BasePage):
    """Главная страница automationexercise.com."""

    def __init__(self, page: Page):
        super().__init__(page)
        # Навигация
        self.signup_login_link = page.get_by_role("link", name="Signup / Login")
        self.products_link = page.get_by_role("link", name="Products")
        self.test_cases_link = page.get_by_role("link", name="Test Cases", exact=True).first
        self.contact_us_link = page.get_by_role("link", name="Contact us")
        self.logout_link = page.get_by_role("link", name="Logout")
        self.delete_account_link = page.get_by_role("link", name="Delete Account")
        # Индикатор входа
        self.logged_in_as = page.get_by_text("Logged in as")

    def open(self):
        super().open("/")
        return self

    def go_to_signup_login(self):
        self.click(self.signup_login_link)
        return self

    def go_to_products(self):
        self.click(self.products_link)
        return self

    def go_to_test_cases(self):
        self.click(self.test_cases_link)
        return self

    def go_to_contact_us(self):
        self.click(self.contact_us_link)
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def logout(self):
        self.click(self.logout_link)
        return self

    def delete_account(self):
        self.click(self.delete_account_link)
        return self