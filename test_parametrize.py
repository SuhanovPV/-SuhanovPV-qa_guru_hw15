"""
Переопределите параметр с помощью indirect параметризации на уровне теста
"""
import pytest
from selene import browser, be
from selenium import webdriver


@pytest.fixture(params=[(1920, 1080), (1280, 720), (1366, 768), (384, 854), (375, 812), (810, 1080)])
def custom_browser(request):
    options = webdriver.FirefoxOptions()
    options.page_load_strategy = 'eager'
    browser.config.driver_options = options
    browser.config.base_url = 'https://github.com'
    width, height = request.param
    browser.config.window_width = width
    browser.config.window_height = height


@pytest.mark.parametrize("custom_browser",
                         [(1920, 1080), (1280, 720), (1366, 768)],
                         ids=['1920x1080', '1280x720', '1366x768'],
                         indirect=True)
def test_github_desktop(custom_browser):
    browser.open('/')
    browser.element('.HeaderMenu .HeaderMenu-link--sign-in').click()
    browser.element('#login form').should(be.visible)


@pytest.mark.parametrize("custom_browser",
                         [(384, 854), (375, 812), (810, 1080)],
                         ids=['Galaxy S20+', 'iPhone 11 Pro', 'iPad'],
                         indirect=True)
def test_github_mobile(custom_browser):
    browser.open('/')
    browser.element('a[aria-label=Homepage]+div a').click()
    browser.element('#login form').should(be.visible)
