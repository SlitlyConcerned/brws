import os

from selenium.webdriver.common.keys import Keys

from brws import lib, run


def brws_get(driver, url):
    if "http" not in url:
        url = "https://" + url
    driver.get(url)


def brws_ddg(driver, query):
    driver.get(f"https://duckduckgo.com/{query}")


def brws_google(driver, query):
    driver.get(f"https://google.com/search?q={query}")


def brws_pgup(driver):
    body = driver.find_element_by_css_selector('body')
    body.send_keys(Keys.PAGE_UP)


def brws_pgdn(driver):
    body = driver.find_element_by_css_selector('body')
    body.send_keys(Keys.PAGE_DOWN)


def brws_click(driver, text):
    lib.click_link_with_text(driver, text)


def brws_signup(driver):
    lib.click_link_with_text(driver, "Sign up")


def brws_get_pid(driver):
    print(os.getpid())


default_commands = {
    "g": brws_get,
    "c": brws_click,
    "signup": brws_signup,
    "u": brws_pgup,
    "d": brws_pgdn,
    "ddg": brws_ddg,
    "google": brws_google,
    "get_pid": brws_get_pid,
}


def run_default(port, driver="Chrome"):
    run(driver, port, default_commands)
