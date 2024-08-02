# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

def run_selenium():
    driver = webdriver.Firefox()
    driver.get('https://www.humblebundle.com/login')

    wait_until_element_is_interactable(driver, By.ID, "onetrust-accept-btn-handler", 5)
    cookie_consent_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    click_when_interactable(driver, cookie_consent_button)

    input("Press Enter to continue...")

    driver.close()

def wait_until_element_is_interactable(driver, strategy, value, timeout):

    wait = WebDriverWait(driver, timeout)
    wait.until(lambda d : driver.find_elements(strategy, value))

def click_when_interactable(driver, element):
    errors = [NoSuchElementException, ElementNotInteractableException]
    wait = WebDriverWait(driver, timeout=5, poll_frequency=1.5, ignored_exceptions=errors)
    wait.until(lambda d: element.click() or True)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_selenium()