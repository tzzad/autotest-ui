import logging
from symtable import Class
import pytest
from playwright.sync_api import sync_playwright, expect, playwright, Playwright, Page


def  test_system_user(open_system, create_promoevent):
    page = open_system
    logging.info("Ссылка открыта")
