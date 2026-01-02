import pytest
import logging
from playwright.sync_api import sync_playwright

@pytest.fixture(autouse=True)
def send_analytics_data():
    print("[AUTOUSE] Отправляем данные в сервис аналитики")

@pytest.fixture(scope="session")
def settings():
    print("[SESSION] Инициализируем настройки автотеста")

@pytest.fixture(scope="class")
def user():
    print("[CLASS] Создаем даннные пользователя 1 раз на тестовый класс")
@pytest.fixture(scope="function")
def browser():
    print("[FUNCTION] Открываем браузер на каждый автотест")


class TestUserFlow:
    def test_user_can_login(self, settings, browser, user):
        ...
    def test_user_can_create_course(self, settings, browser, user):
        ...

class TestAccountFlow:
    def test_user_account(self, settings, browser, user,):
        ...
