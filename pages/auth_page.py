from playwright.sync_api import Page
from pages.base_page import BasePage


class AuthPage(BasePage):
    """Страница Login / Signup."""

    def __init__(self, page: Page):
        super().__init__(page)
        # Блок нового пользователя
        self.new_user_signup_title = page.get_by_text("New User Signup!")
        self.signup_name = page.locator("[data-qa='signup-name']")
        self.signup_email = page.locator("[data-qa='signup-email']")
        self.signup_btn = page.locator("[data-qa='signup-button']")
        # Блок входа
        self.login_title = page.get_by_text("Login to your account")
        self.login_email = page.locator("[data-qa='login-email']")
        self.login_password = page.locator("[data-qa='login-password']")
        self.login_btn = page.locator("[data-qa='login-button']")
        # Сообщения
        self.email_exists_error = page.get_by_text("Email Address already exist!")
        self.login_error = page.get_by_text("Your email or password is incorrect!")

    def open(self):
        super().open("/login")
        return self

    def start_signup(self, name: str, email: str):
        self.fill(self.signup_name, name)
        self.fill(self.signup_email, email)
        self.click(self.signup_btn)
        return self

    def login(self, email: str, password: str):
        self.fill(self.login_email, email)
        self.fill(self.login_password, password)
        self.click(self.login_btn)
        return self


class AccountInfoPage(BasePage):
    """Страница ENTER ACCOUNT INFORMATION после начала регистрации."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.title = page.get_by_text("ENTER ACCOUNT INFORMATION")
        self.gender_mr = page.locator("#id_gender1")
        self.password = page.locator("#password")
        self.days = page.locator("#days")
        self.months = page.locator("#months")
        self.years = page.locator("#years")
        self.newsletter = page.locator("#newsletter")
        self.optin = page.locator("#optin")
        self.first_name = page.locator("#first_name")
        self.last_name = page.locator("#last_name")
        self.company = page.locator("#company")
        self.address1 = page.locator("#address1")
        self.address2 = page.locator("#address2")
        self.country = page.locator("#country")
        self.state = page.locator("#state")
        self.city = page.locator("#city")
        self.zipcode = page.locator("#zipcode")
        self.mobile = page.locator("#mobile_number")
        self.create_account_btn = page.get_by_role("button", name="Create Account")
        self.account_created_msg = page.get_by_text("ACCOUNT CREATED!")
        self.account_deleted_msg = page.get_by_text("ACCOUNT DELETED!")
        self.continue_btn = page.get_by_role("link", name="Continue")

    def fill_form(self, password: str, first_name: str = "Test", last_name: str = "User"):
        self.gender_mr.check()
        self.password.fill(password)
        self.days.select_option("10")
        self.months.select_option("5")
        self.years.select_option("1990")
        self.newsletter.check()
        self.optin.check()
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.company.fill("TestCo")
        self.address1.fill("123 St")
        self.address2.fill("Apt 1")
        self.country.select_option("United States")
        self.state.fill("CA")
        self.city.fill("LA")
        self.zipcode.fill("12345")
        self.mobile.fill("1234567890")
        return self

    def submit(self):
        self.click(self.create_account_btn)
        return self

    def click_continue(self):
        self.click(self.continue_btn)
        return self