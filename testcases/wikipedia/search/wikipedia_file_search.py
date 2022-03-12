import os
import time
from selenium import webdriver
from time import sleep
from selenium.webdriver import Keys
from wikipedia_config import WikipediaVariableConfig

chrome_driver = webdriver.Chrome()


def check_page_url_matches():
    """
        This method tests the wikipedia page title is matching to the expected.
    :return:
    """
    wikipedia_url = WikipediaVariableConfig.page_url

    chrome_driver.get(wikipedia_url)
    chrome_driver.maximize_window()

    title = WikipediaVariableConfig.title
    assert title == chrome_driver.title

    sleep(2)
    chrome_driver.close()


def searches():
    """
        checks source file exists
        loops through the source file
        returns the names from the source file
    :return:
    """
    source_file = WikipediaVariableConfig.input_file
    if not os.path.isfile(source_file):
        print("source_file is Missing", source_file)
    else:
        print("Source file found - Starting the execution of search Method")
    with open(source_file, 'r') as f:
        names = f.readlines()
        found_names = [name.replace("\n", "") for name in names if (name != "\n")]
        print(found_names, "\n")
    return found_names


def fetch_values(myvar):
    """
        This will find the given name from the source input file
        Checks the search page is opening
        Checks the search page contains teh first paragraph of text
        Returns the found text
    :param myvar:
    :return:
    """
    chrome_driver.get(WikipediaVariableConfig.page_url)
    element = chrome_driver.find_element_by_id("ooui-php-1")
    element.clear()
    element.send_keys(myvar)
    element.send_keys(Keys.RETURN)
    time.sleep(5)
    # identify element with title attribute and click()
    element = chrome_driver.find_element_by_xpath('//a[@title="' + myvar + '"]')
    element.click()
    print("Current page title: " + chrome_driver.title)
    xpath_paragraph_text_1 = '//*[@id ="mw-content-text"]/div[1]/p[2]' # First found paragraph text
    xpath_paragraph_text_2 = '//*[@id ="mw-content-text"]/div[1]/p[3]' # Second found paragraph text
    try:
        element = chrome_driver.find_element_by_xpath(xpath_paragraph_text_1).text
        if len(element) > 1:
            print(element)
            print("\n")
            return element
        else:
            element = chrome_driver.find_element_by_xpath(xpath_paragraph_text_2).text
            print(element)
            print("\n")
            return element
    except:
        pass
    finally:
        time.sleep(5)
        chrome_driver.close()


def write_response(found_names):
    """
        this function loops through each found name page
        writes the found first paragraph tp a response file.
    :param found_names:
    :return:
    """
    for f_name in found_names:
        data = fetch_values(f_name)
        with open('response.txt', 'a', encoding="utf-8") as f:
            f.write(data)
            f.write('\n')
            f.write('\n')


if __name__ == "__main__":
    check_page_url_matches()
    found_names = searches()
    write_response(found_names)
