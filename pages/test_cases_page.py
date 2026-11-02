from playwright.sync_api import Page
from pages.base_page import BasePage


class TCasesPage(BasePage):
    """Страница со списком тест-кейсов."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.title = page.locator("h2.title")

    def expect_title_contains(self, text: str = "Test Cases"):
        self.expect_text(self.title, text)
        return self