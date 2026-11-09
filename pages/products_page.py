from playwright.sync_api import Page
from pages.base_page import BasePage


class ProductsPage(BasePage):
    """Страница списка продуктов."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.all_products_title = page.get_by_text("ALL PRODUCTS")
        self.searched_products_title = page.get_by_text("SEARCHED PRODUCTS")
        self.search_input = page.locator("#search_product")
        self.search_btn = page.locator("#submit_search")
        self.view_product_links = page.get_by_role("link", name="View Product")
        self.product_wrappers = page.locator(".product-image-wrapper")
        self.continue_shopping_button = page.get_by_role("button", name="Continue Shopping")
        self.view_cart_link = page.get_by_text("View Cart", exact=True)

    def open(self):
        super().open("/products")
        return self

    def view_first_product(self):
        self.click(self.view_product_links.first)
        return ProductDetailPage(self.page)

    def search(self, query: str):
        self.fill(self.search_input, query)
        self.click(self.search_btn)
        return self

    def add_product(self, index: int):
        product = self.product_wrappers.nth(index)
        product.hover()
        product.locator("a.add-to-cart").first.click()
        return self

    def continue_shopping(self):
        self.click(self.continue_shopping_button)
        return self

    def view_cart(self):
        self.click(self.view_cart_link)
        return self


class ProductDetailPage(BasePage):
    """Страница деталей продукта."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.product_info = page.locator(".product-information")
        self.product_name = page.locator(".product-information h2")
        self.quantity = page.locator("#quantity")
        self.add_to_cart_button = page.locator("button.cart")
        self.view_cart_link = page.get_by_text("View Cart", exact=True)

    def expect_product_name(self, name: str):
        self.expect_text(self.product_name, name)
        return self

    def expect_contains(self, text: str):
        self.expect_text(self.product_info, text)
        return self

    def set_quantity(self, quantity: int):
        self.fill(self.quantity, str(quantity))
        return self

    def add_to_cart(self):
        self.click(self.add_to_cart_button)
        return self

    def view_cart(self):
        self.click(self.view_cart_link)
        return self
