from contextlib import contextmanager

from selenium.webdriver.common.keys import Keys


class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.sites = {}

    def add(self, sitename, login_url, un_id, pw_id, do_enter=True):
        self.sites[sitename] = lambda driver, _: login(driver, login_url,
                                                       un_id, self.name,
                                                       pw_id, self.password,
                                                       do_enter)

    def generate_commands(self):
        return {"login/"+sitename:func for sitename, func in self.sites.items()}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return


def click_link_with_text(driver, text):
    for elem in driver.find_elements_by_tag_name("a"):
        if text in elem.text:
            elem.click()


def enter(element):
    element.send_keys(Keys.RETURN)


def login(driver, login_url, un_id, username, pw_id, password, do_enter=True):
    driver.get(login_url)
    driver.find_element_by_id(un_id).send_keys(username)
    pw_elem = driver.find_element_by_id(pw_id)
    pw_elem.send_keys(password)
    if do_enter:
        enter(pw_elem)
