"""
Сделайте разные фикстуры для каждого теста, которые выставят размеры окна браузера
"""
import pytest
from selene import browser, be
from selenium import webdriver

@pytest.fixture(scope='session')
def set_browser():
    options = webdriver.FirefoxOptions()
    options.page_load_strategy = 'eager'
    browser.config.driver_options = options
    browser.config.base_url = 'https://github.com'

@pytest.fixture(params=[(384, 854), (375, 812), (810, 1080)], ids=['Galaxy S20+', 'iPhone 11 Pro', 'iPad'])
def mobile_version(set_browser, request):
    width, height = request.param
    browser.config.window_width = width
    browser.config.window_height = height

@pytest.fixture(params=[(1920, 1080), (1280, 720), (1366, 768)], ids=['1920x1080', '1280x720', '1366x768'])
def desktop_version(set_browser, request):
    width, height = request.param
    browser.config.window_width = width
    browser.config.window_height = height

def test_github_desktop(desktop_version):
    browser.open('/')
    browser.element('.HeaderMenu .HeaderMenu-link--sign-in').click()
    browser.element('#login form').should(be.visible)

def test_github_mobile(mobile_version):
    browser.open('/')
    browser.element('a[aria-label=Homepage]+div a').click()
    browser.element('#login form').should(be.visible)
