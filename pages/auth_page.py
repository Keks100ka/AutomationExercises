from playwright.sync_api import Page, expect

class AuthPage:
    def __init__(self, page: Page):
        self.page = page
        self.signup_name = page.locator("[data-qa='signup-name']")
        self.signup_email = page.locator("[data-qa='signup-email']")
        self.signup_btn = page.locator("[data-qa='signup-button']")

    def start_signup(self, name, email):
        self.signup_name.fill(name)
        self.signup_email.fill(email)
        self.signup_btn.click()