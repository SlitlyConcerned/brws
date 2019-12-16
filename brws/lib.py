def click_link_with_text(driver, text):
    for elem in driver.find_elements_by_tag_name("a"):
        if text in elem.text:
            elem.click()
