import re
import time
import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.auth_page import AccountInfoPage, AuthPage
from pages.cart_page import CartPage, CheckoutPage
from pages.products_page import ProductsPage, ProductDetailPage

# ---------- TC8 ----------
def test_tc8_all_products_detail(page: Page):
    """TC8: Все продукты и страница деталей первого."""
    home = HomePage(page).open()
    home.go_to_products()

    products = ProductsPage(page)
    products.expect_url(".*products")
    products.expect_visible(products.all_products_title)

    detail = products.view_first_product()
    detail.expect_product_name("Blue Top")
    detail.expect_contains("Rs. 500")
    detail.expect_contains("Availability")
    detail.expect_contains("Condition")
    detail.expect_contains("Brand")


# ---------- TC9 ----------
def test_tc9_search_product(page: Page):
    """TC9: Поиск продукта и проверка результатов."""
    home = HomePage(page).open()
    home.go_to_products()

    products = ProductsPage(page)
    products.expect_visible(products.all_products_title)

    products.search("Top")
    products.expect_visible(products.searched_products_title)
    expect(products.product_wrappers.first).to_be_visible()


def _add_first_product(page: Page):
    products = ProductsPage(page).open()
    products.add_product(0)
    return products


def _create_checkout_user(page: Page):
    auth = AuthPage(page)
    email = f"tc14_{time.time_ns()}@test.com"
    auth.start_signup("TC Checkout User", email)
    info = AccountInfoPage(page)
    info.fill_form("Pass123", "TC", "Checkout").submit()
    info.expect_visible(info.account_created_msg)
    info.click_continue()


def test_tc10_subscription_home(page: Page):
    """TC10: подписка на главной странице."""
    home = HomePage(page).open()
    home.subscription_title.scroll_into_view_if_needed()
    home.expect_visible(home.subscription_title)
    home.subscribe(f"tc10_{time.time_ns()}@test.com")
    home.expect_visible(home.subscription_success)


def test_tc11_subscription_cart(page: Page):
    """TC11: подписка со страницы корзины."""
    HomePage(page).open().go_to_cart()
    cart = CartPage(page)
    cart.subscription_title.scroll_into_view_if_needed()
    cart.expect_visible(cart.subscription_title)
    cart.subscribe(f"tc11_{time.time_ns()}@test.com")
    cart.expect_visible(cart.subscription_success)


def test_tc12_add_products_to_cart(page: Page):
    """TC12: добавление двух товаров и проверка строк корзины."""
    products = _add_first_product(page)
    products.continue_shopping().add_product(1).view_cart()
    cart = CartPage(page)
    cart.expect_displayed()
    expect(cart.cart_rows).to_have_count(2)
    expect(cart.cart_rows.nth(0).locator(".cart_price")).to_contain_text("Rs.")
    expect(cart.cart_rows.nth(0).locator(".cart_quantity button")).to_have_text("1")
    expect(cart.cart_rows.nth(0).locator(".cart_total")).to_contain_text("Rs.")


def test_tc13_product_quantity_in_cart(page: Page):
    """TC13: добавление товара с количеством 4."""
    detail = ProductsPage(page).open().view_first_product()
    detail.set_quantity(4).add_to_cart().view_cart()
    cart = CartPage(page)
    cart.expect_displayed()
    expect(cart.cart_rows.first.locator(".cart_quantity button")).to_have_text("4")


def test_tc14_place_order_register_while_checkout(page: Page):
    """TC14: регистрация пользователя в процессе checkout и заказ."""
    _add_first_product(page).view_cart()
    CartPage(page).proceed_to_checkout()
    checkout = CheckoutPage(page)
    checkout.register_login_link.click()
    _create_checkout_user(page)
    HomePage(page).go_to_cart()
    CartPage(page).proceed_to_checkout()
    checkout = CheckoutPage(page)
    checkout.expect_order_details().place_order().pay()
    checkout.expect_visible(checkout.order_success, timeout=15000)
    HomePage(page).delete_account()
    AccountInfoPage(page).expect_visible(AccountInfoPage(page).account_deleted_msg)


def test_tc15_place_order_register_before_checkout(page: Page):
    """TC15: регистрация до добавления товара и checkout."""
    HomePage(page).open().go_to_signup_login()
    auth = AuthPage(page)
    auth.start_signup("TC15 User", f"tc15_{time.time_ns()}@test.com")
    info = AccountInfoPage(page)
    info.fill_form("Pass123", "TC15", "User").submit()
    info.click_continue()
    _add_first_product(page).view_cart()
    CartPage(page).proceed_to_checkout()
    checkout = CheckoutPage(page)
    checkout.expect_order_details().place_order().pay()
    checkout.expect_visible(checkout.order_success, timeout=15000)
    HomePage(page).delete_account()


def test_tc16_place_order_login_before_checkout(page: Page, test_user):
    """TC16: вход существующего пользователя до checkout."""
    home = HomePage(page).open()
    home.go_to_signup_login()
    AuthPage(page).login(test_user["email"], test_user["password"])
    expect(home.logged_in_as).to_be_visible()
    _add_first_product(page).view_cart()
    CartPage(page).proceed_to_checkout()
    checkout = CheckoutPage(page)
    checkout.expect_order_details().place_order().pay()
    checkout.expect_visible(checkout.order_success, timeout=15000)
    home.delete_account()


def test_tc17_remove_product_from_cart(page: Page):
    """TC17: удаление товара из корзины."""
    _add_first_product(page).view_cart()
    cart = CartPage(page)
    cart.expect_displayed()
    expect(cart.cart_rows).to_have_count(1)
    cart.remove_product()
    cart.expect_visible(cart.empty_cart)
    expect(cart.remove_buttons).to_have_count(0)
