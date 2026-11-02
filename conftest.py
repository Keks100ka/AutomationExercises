import time
import pytest
import requests

BASE_URL = "https://automationexercise.com"
API_URL = f"{BASE_URL}/api"


@pytest.fixture(scope="session")
def test_user():
    email = f"pw_test_{int(time.time())}@example.com"
    password = "TestPass123"
    user_data = {
        "name": "PW Test User", "email": email, "password": password,
        "title": "Mr", "birth_date": "10", "birth_month": "5", "birth_year": "1990",
        "firstname": "PW", "lastname": "Test", "company": "TestCo",
        "address1": "123 Test St", "address2": "", "country": "United States",
        "zipcode": "12345", "state": "CA", "city": "LA", "mobile_number": "1234567890",
    }
    requests.post(f"{API_URL}/createAccount", data=user_data)
    yield {"email": email, "password": password, "name": user_data["name"]}
    requests.delete(f"{API_URL}/deleteAccount",
                    data={"email": email, "password": password})


@pytest.fixture(autouse=True)
def block_ads(page):
    page.route("**/*", lambda route: route.abort() if any(
        d in route.request.url for d in
        ["googlesyndication", "doubleclick", "googleads", "adservice"]
    ) else route.continue_())