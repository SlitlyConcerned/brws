from selenium.webdriver.common.keys import Keys

from br import br


def brws_get(driver, url):
    driver.get(url)


def brws_ddg(driver, query):
    driver.get(f"https://duckduckgo.com/{query}")


def brws_google(driver, query):
    driver.get(f"https://google.com/search?q={query}")


def brws_pgup(driver):
    body = browser.find_element_by_css_selector('body')
    body.send_keys(Keys.PAGE_UP)


def brws_pgdn(driver):
    body = browser.find_element_by_css_selector('body')
    body.send_keys(Keys.PAGE_DOWN)


def brws_click(driver, term):
    for elem in driver.find_elements_by_tag_name("a"):
        if term in elem.text:
            elem.click()


default_commands = {
    "g": brws_get,
    "c": brws_click,
    "u": brws_pgup,
    "d": brws_pgdn,
    "ddg": brws_ddg,
    "google": brws_google,
}


def run_default(port, driver="Chrome"):
    brws(driver, port, default_commands)
