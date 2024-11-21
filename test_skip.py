"""
Параметризуйте фикстуру несколькими вариантами размеров окна
Пропустите мобильный тест, если соотношение сторон десктопное (и наоборот)
"""
import pytest
from selene import browser, be
from selenium import webdriver


@pytest.fixture(params=[(1920, 1080), (1280, 720), (1366, 768), (384, 854), (375, 812), (810, 1080)],
                ids=['1920x1080', '1280x720', '1366x768', 'Galaxy S20+', 'iPhone 11 Pro', 'iPad'])
def custom_browser(request):
    options = webdriver.FirefoxOptions()
    options.page_load_strategy = 'eager'
    browser.config.driver_options = options
    browser.config.base_url = 'https://github.com'
    width, height = request.param
    browser.config.window_width = width
    browser.config.window_height = height

    browser_type = 'desktop' if int(width) > 1000 else 'mobile'

    yield browser_type


def test_github_desktop(custom_browser):
    if custom_browser == 'mobile':
        pytest.skip(reason='Разрешение экрана для мобильной версии')
    browser.open('/')
    browser.element('.HeaderMenu .HeaderMenu-link--sign-in').click()
    browser.element('#login form').should(be.visible)


def test_github_mobile(custom_browser):
    if custom_browser == 'desktop':
        pytest.skip(reason='Разрешение экрана для десктопной версии')
    browser.open('/')
    browser.element('a[aria-label=Homepage]+div a').click()
    browser.element('#login form').should(be.visible)
