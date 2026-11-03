from playwright.sync_api import Page
from pages.base_page import BasePage


class ContactPage(BasePage):
    """Страница Contact Us."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.get_in_touch_title = page.get_by_text("GET IN TOUCH")
        self.name = page.locator("[data-qa='name']")
        self.email = page.locator("[data-qa='email']")
        self.subject = page.locator("[data-qa='subject']")
        self.message = page.locator("[data-qa='message']")
        self.upload = page.locator("input[name='upload_file']")
        self.submit_btn = page.locator("[data-qa='submit-button']")
        self.success_msg = page.locator("div.status.alert.alert-success")
        self.home_link = page.locator("#form-section a[href='/']")

    def open(self):
        super().open("/contact_us")
        return self

    def submit_form(self, name: str, email: str, subject: str, message: str, file_path: str):
        self.fill(self.name, name)
        self.fill(self.email, email)
        self.fill(self.subject, subject)
        self.fill(self.message, message)
        self.upload.set_input_files(file_path)

        # Обработка нативного alert
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.click(self.submit_btn)
        return self

    def click_home(self):
        self.click(self.home_link)
        return self
