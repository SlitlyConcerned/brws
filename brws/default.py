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


def brws_pgup(driver, _):
    body = driver.find_element_by_css_selector('body')
    body.send_keys(Keys.PAGE_UP)


def brws_pgdn(driver, _):
    body = driver.find_element_by_css_selector('body')
    body.send_keys(Keys.PAGE_DOWN)


def brws_history_go(driver, index):
    driver.executeScript("window.history.go(-1)");


def brws_go_back(driver, _):
    brws_history_go(driver, -1)


def brws_go_forward(driver, _):
    brws_history_go(driver, -1)


def brws_click(driver, text):
    lib.click_link_with_text(driver, text)


def brws_signup(driver, _):
    lib.click_link_with_text(driver, "Sign up")


def brws_signin(driver, _):
    lib.click_link_with_text(driver, "Sign in")


def brws_get_pid(driver, _):
    return str(os.getpid())


def brws_show_url(driver, _):
    return driver.current_url


default_commands = {
    "g": brws_get,
    "c": brws_click,
    "b": brws_go_back,
    "f": brws_go_forward,
    "signup": brws_signup,
    "signin": brws_signin,
    "u": brws_pgup,
    "d": brws_pgdn,
    "ddg": brws_ddg,
    "google": brws_google,
    "get_pid": brws_get_pid,
    "get_url": brws_show_url,
}


def run_default(port, driver="Chrome"):
    run(driver, port, default_commands)
