import time
import pytest
import requests
# for html and trace reports
from datetime import datetime
from pathlib import Path
from playwright.sync_api import BrowserContext, Page

BASE_URL = "https://automationexercise.com"
API_URL = f"{BASE_URL}/api"

# FOR HTML REPORTS (playwright show-trace) 
# ==========================
#  Folder for artifacts
REPORTS_DIR = Path("test-reports")
# Title for HTML report (in html report header)
REPORT_TITLE = "Playwright Test Report"
# Project name for HTML report (in html report dashboard)
PROJECT_NAME = "Drafts and Exercises ui tests"
# QA engineer name for HTML report (in html report dashboard)
QA_ENGINEER = "SKVS"
#===============================

# ==============================================================================
# FIXTURES AND OPTIMIZATION FOR UI TESTS
# ==============================================================================


@pytest.fixture(scope="session")
def test_user():
    email = f"pw_test_{int(time.time())}@example.com"
    password = "TestPass123"
    user_data = {
        "name": "PW Test User",
        "email": email,
        "password": password,
        "title": "Mr",
        "birth_date": "10",
        "birth_month": "5",
        "birth_year": "1990",
        "firstname": "PW",
        "lastname": "Test",
        "company": "TestCo",
        "address1": "123 Test St",
        "address2": "",
        "country": "United States",
        "zipcode": "12345",
        "state": "CA",
        "city": "LA",
        "mobile_number": "1234567890",
    }
    requests.post(f"{API_URL}/createAccount", data=user_data)
    yield {"email": email, "password": password, "name": user_data["name"]}
    requests.delete(f"{API_URL}/deleteAccount", data={"email": email, "password": password})


# 1. Block ads and remove Google Vignette from DOM (https level)
@pytest.fixture(autouse=True)
def block_ads(page):
    page.route(
        "**/*",
        lambda route: (
            route.abort()
            if any(
                d in route.request.url
                for d in ["googlesyndication", "doubleclick", "googleads", "adservice"]
            )
            else route.continue_()
        ),
    )
# 2. JavaScript for Google Vignette removal from screen (page level)
    page.add_init_script("""
        // Каждую секунду ищем элементы рекламы и удаляем их с экрана
        setInterval(() => {
            // Удаляем полноэкранные рекламные блоки Google
            const googleVignette = document.querySelector('ins.adsbygoogle, div[id^="google_ads"]');
            if (googleVignette) {
                googleVignette.remove();
            }
            // Возвращаем прокрутку странице, если реклама её заблокировала
            if (document.body && document.body.style.overflow === 'hidden') {
                document.body.style.overflow = 'auto';
            }
        }, 500);
    """)

#=========================================================
# HTML REPORTS HOOKS AND FIXTURES
#=========================================================
# Hooks for pytest-html report customization
def pytest_html_report_title(report):
    report.title = REPORT_TITLE

@pytest.hookimpl(tryfirst=True)
def pytest_metadata(metadata):
    # Add custom rows to the dashboard summary
    metadata["Project Name"] = PROJECT_NAME
    metadata["QA Engineer"] = QA_ENGINEER
    # Remove unnecessary environment variables from being exposed
    metadata.pop("JAVA_HOME", None)

# ==========================
#  Хук для перехвата падений и добавления скриншотов/ссылок в HTML-отчет
# ==========================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук отслеживает падения тестов и встраивает артефакты в pytest-html 4.0+."""
    outcome = yield call
    report = outcome.get_result()

    # Проверяем, что тест упал во время своего выполнения (call)
    if report.when == "call" and report.failed:
        item.failed_by_hook = True
        
        # Проверяем, активен ли плагин pytest-html
        pytest_html = item.config.pluginmanager.getplugin("html")
        page: Page = item.funcargs.get("page")
        if pytest_html and page:
            extras = getattr(report, "extras", [])
            clean_name = item.name.replace("[", "_").replace("]", "_")

            # 1. Снимаем скриншот и кодируем в Base64-строку для обхода бага в pytest-html
            try:
                import base64
                screenshot_bytes = page.screenshot(full_page=True)
                # Кодируем байты в base64 и преобразуем в строку через .decode("utf-8")
                b64_string = base64.b64encode(screenshot_bytes).decode("utf-8")
                # Передаем именно СТРОКУ. Теперь метод .encode() внутри плагина сработает без ошибок
                extras.append(pytest_html.extras.png(b64_string, name="Failure Screenshot"))
            except Exception:
                pass  # Если скриншот не удалось сделать, просто пропускаем этот шаг

            # 2. Добавляем ссылку на ZIP-архив трейса
            trace_filename = f"{clean_name}_failure_trace.zip"
            extras.append(pytest_html.extras.url(trace_filename, name="Playwright Trace ZIP"))

            report.extras = extras #Reassign extras to report so pytest-html can pick it up

# ==========================
#  Автоматическое управление трейсами Playwright
# ==========================
@pytest.fixture(autouse=True)
def manage_failure_traces(request, context: BrowserContext):
    """Фикстура включает трассировку и сохраняет архив, если тест упал."""
    # Запускаем сбор данных трейса перед тестом
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield  # Здесь выполняются шаги вашего теста

    # Код ниже срабатывает строго после завершения теста
    if getattr(request.node, "failed_by_hook", False):
        REPORTS_DIR.mkdir(exist_ok=True)
        clean_name = request.node.name.replace("[", "_").replace("]", "_")
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
        trace_path = REPORTS_DIR / f"{clean_name}_{current_time}.zip"
    
        try:
            # Сохраняем трейс только для упавшего теста
            context.tracing.stop(path=str(trace_path))
            return
        except Exception:
            pass

    # Если тест прошел успешно — просто глушим трейс, не сохраняя его на диск
    try:
        context.tracing.stop()
    except Exception:
        pass


# For html report generation, we can dynamically set the report filename based on the current timestamp
@pytest.hookimpl(tryfirst=True)  
def pytest_configure(config):
    """Хук динамически подставляет имя HTML-отчета только при реальном запуске тестов"""
    # ЕСЛИ это просто фоновый поиск тестов для "колбы" VS Code — выходим и ничего не создаем
    if config.getoption("collectonly", default=False):
        return
    # В противном случае (это реальный старт тестов) — создаем уникальный файл отчета
    # 1. Создаем папку для результатов, если её нет
    REPORTS_DIR.mkdir(exist_ok=True)
    # 2. Генерируем уникальное имя файла на основе текущей даты и времени
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
    report_filename = REPORTS_DIR / f"report_{current_time}.html"
    # 3. Принудительно передаем эти параметры в конфигурацию плагина pytest-html
    config.option.htmlpath = report_filename
    config.option.self_contained_html = True  # Делаем HTML-файл независимым