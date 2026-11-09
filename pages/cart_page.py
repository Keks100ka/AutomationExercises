from playwright.sync_api import Page

from pages.base_page import BasePage


class CartPage(BasePage):
    """Страница корзины и форма подписки в footer."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_table = page.locator("#cart_info_table")
        self.cart_rows = page.locator("#cart_info_table tbody tr")
        self.proceed_to_checkout_button = page.get_by_text("Proceed To Checkout", exact=True)
        self.subscription_title = page.get_by_role("heading", name="Subscription")
        self.subscription_email = page.locator("#susbscribe_email")
        self.subscribe_button = page.locator("#subscribe")
        self.subscription_success = page.get_by_text("You have been successfully subscribed!")
        self.remove_buttons = page.locator(".cart_quantity_delete")
        self.empty_cart = page.locator("#empty_cart")

    def open(self):
        super().open("/view_cart")
        return self

    def expect_displayed(self):
        self.expect_visible(self.cart_table)
        return self

    def subscribe(self, email: str):
        self.fill(self.subscription_email, email)
        self.click(self.subscribe_button)
        return self

    def proceed_to_checkout(self):
        self.click(self.proceed_to_checkout_button)
        return self

    def remove_product(self, index: int = 0):
        self.click(self.remove_buttons.nth(index))
        return self


class CheckoutPage(BasePage):
    """Checkout, payment and order confirmation controls."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.delivery_address = page.locator("#address_delivery")
        self.review_order = page.locator("#cart_info")
        self.register_login_link = page.get_by_text("Register / Login", exact=True)
        self.comment = page.locator("textarea[name='message']")
        self.place_order_button = page.get_by_text("Place Order", exact=True)
        self.name_on_card = page.locator("[data-qa='name-on-card']")
        self.card_number = page.locator("[data-qa='card-number']")
        self.cvc = page.locator("[data-qa='cvc']")
        self.expiry_month = page.locator("[data-qa='expiry-month']")
        self.expiry_year = page.locator("[data-qa='expiry-year']")
        self.pay_button = page.locator("[data-qa='pay-button']")
        self.order_success = page.get_by_text("Congratulations! Your order has been confirmed!")

    def expect_order_details(self):
        self.expect_visible(self.delivery_address)
        self.expect_visible(self.review_order)
        return self

    def place_order(self, comment: str = "Please deliver carefully"):
        self.fill(self.comment, comment)
        self.click(self.place_order_button)
        return self

    def pay(self):
        self.fill(self.name_on_card, "Test Card")
        self.fill(self.card_number, "4111111111111111")
        self.fill(self.cvc, "123")
        self.fill(self.expiry_month, "12")
        self.fill(self.expiry_year, "2030")
        self.click(self.pay_button)
        return self
