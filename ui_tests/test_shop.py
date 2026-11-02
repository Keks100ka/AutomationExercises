import re
import time
import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage
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
