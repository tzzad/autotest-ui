from playwright.sync_api import Page

class BasePage:
    def __init__(self, page):
        self.page = page

    def visit(self, url: str):
        self.page.goto(url, wait_until="networkidle")

    def reload(self):
        self.page.reload(wait_until="networkidle")

    def get_by_test_id(self, param):
        pass