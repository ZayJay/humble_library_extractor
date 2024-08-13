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

    # Cookie Popup
    wait_until_element_is_interactable(driver, By.ID, "onetrust-accept-btn-handler", 5)
    cookie_consent_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    click_when_interactable(driver, cookie_consent_button)

    # Sign-in
    username_input = driver.find_element(By.NAME, "username")
    enter_text_when_interactable(driver, username_input, "Zajac.Steven@gmail.com")

    password_input = driver.find_element(By.NAME, "password")
    with open(".creds") as f:
        password_text = f.read()
    enter_text_when_interactable(driver, password_input, password_text)

    submit_button = driver.find_element(By.CLASS_NAME, "flat-cta-button")
    click_when_interactable(driver, submit_button)

    # 2FA
    wait_until_element_is_interactable(driver, By.CLASS_NAME, "twofactor-form-view", 5)
    verification_code_input = driver.find_element(By.CLASS_NAME, "text-input")
    verification_code = input("Enter verification code:")
    enter_text_when_interactable(driver, verification_code_input, verification_code)

    button_verify = None
    buttons = driver.find_elements(By.TAG_NAME, "button")

    for button in buttons:
        if button.get_attribute("type") == "submit" and button.text == "VERIFY":
            button_verify = button

    if button_verify is not None:
        click_when_interactable(driver, button_verify)
    else:
        print("Could not find 'Verify' button!")

    # Purchases tab

    input("Press Enter to continue...")

    driver.close()


def wait_until_element_is_interactable(driver, strategy, value, timeout):

    wait = WebDriverWait(driver, timeout)
    wait.until(lambda d : driver.find_elements(strategy, value))


def click_when_interactable(driver, element):

    errors = [NoSuchElementException, ElementNotInteractableException]
    wait = WebDriverWait(driver, timeout=5, poll_frequency=1.5, ignored_exceptions=errors)
    wait.until(lambda d: element.click() or True)

def enter_text_when_interactable(driver, element, text):

    errors = [NoSuchElementException, ElementNotInteractableException]
    wait = WebDriverWait(driver, timeout=5, poll_frequency=1.5, ignored_exceptions=errors)
    wait.until(lambda d: element.send_keys(text) or True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_selenium()
