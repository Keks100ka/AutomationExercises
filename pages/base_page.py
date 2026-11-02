from playwright.sync_api import Page, expect
import re


class BasePage:
    """Базовый класс для всех Page Object. Содержит общие действия."""

    def __init__(self, page: Page, base_url: str = "https://automationexercise.com"):
        self.page = page
        self.base_url = base_url

    def open(self, path: str = "/"):
        """Открыть страницу по относительному пути."""
        self.page.goto(f"{self.base_url}{path}")
        self.page.wait_for_load_state("domcontentloaded")

    def expect_title(self, pattern: str):
        """Проверить заголовок страницы по regex."""
        expect(self.page).to_have_title(re.compile(pattern))

    def expect_url(self, pattern: str):
        """Проверить URL по regex."""
        expect(self.page).to_have_url(re.compile(pattern))

    def click(self, locator):
        """Клик с ожиданием видимости."""
        expect(locator).to_be_visible()
        locator.click()

    def fill(self, locator, value: str):
        """Заполнить поле с ожиданием видимости."""
        expect(locator).to_be_visible()
        locator.fill(value)

    def expect_visible(self, locator, timeout: int = 10000):
        """Проверить, что элемент виден."""
        expect(locator).to_be_visible(timeout=timeout)

    def expect_text(self, locator, text: str, timeout: int = 10000):
        """Проверить, что элемент содержит текст."""
        expect(locator).to_contain_text(text, timeout=timeout)